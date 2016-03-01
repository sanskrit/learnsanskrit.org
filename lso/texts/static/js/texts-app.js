import React from 'react';
import ReactDOM from 'react-dom';

const P = React.PropTypes;

// Util
// ---------------------------------------------------------------------

function decodeURL(url) {
  const parts = url.split('+');
  if (parts.length === 1) {
    return { prefix: parts[0], slugs: [] };
  } else {
    return { prefix: parts[0], slugs: parts[1].split(',') };
  }
}

function encodeURL(data) {
  if (data.slugs.length) {
    return data.prefix + '+' + data.slugs.join(',');
  }
  return data.prefix;
}

function toggleSecondaryText(slug) {
  let pageState = decodeURL(window.location.pathname);
  const index = pageState.slugs.indexOf(slug);
  if (index === -1) {
    pageState.slugs.push(slug);
  } else {
    pageState.slugs.splice(index, 1);
  }
  const newURL = encodeURL(pageState);
  window.location.href = newURL;
}

// Schema
// ---------------------------------------------------------------------

const PaginationState = P.shape({
  query: P.string.isRequired,
  readable: P.string.isRequired,
});

const SegmentSchema = P.shape({
  id: P.number.isRequired,
  content: P.string.isRequired,
  slug: P.string.isRequired,
  text_id: P.number.isRequired,
});

const TextSchema = P.shape({
  id: P.number.isRequired,
  name: P.string.isRequired,
  slug: P.string.isRequired,
  xmlid_prefix: P.string.isRequired,
});

const CardState = P.shape({
  primary: SegmentSchema.isRequired,
});

// Components
// ---------------------------------------------------------------------

/** Shows the current query. */
const Header = (props) => {
  return <h1>{props.text}</h1>
};

/** Shows a segment by dangerously dumping its raw HTML into the document. */
const DangerousSegment = (props) => {
  return (<div dangerouslySetInnerHTML={{__html: props.content}} />);
};

const SecondaryTextInCard = (props) => {
  const segments = props.segments.map((s) => {
    return <DangerousSegment key={s.id} {...s} />
  });
  return (
    <div>
      <h4>{props.text.name}</h4>
      {segments}
    </div>
  );
};

/** Secondary texts of some type, i.e. translations or commentaries. */
const GenreForCard = (props) => {
  const children = props.texts.map((t) => {
    return <SecondaryTextInCard key={t.text.slug} {...t} />
  });
  if (children.length) {
    return (
      <div>
        <h3>{props.title}</h3>
        {children}
      </div>
    );
  }
  return <div />;
};

/** Shows all of the information related to some segment in the text. */
const Card = React.createClass({
  propTypes: {
    primary: SegmentSchema.isRequired,
  },
  render() {
    return (
      <div>
        <DangerousSegment {...this.props.primary} />
        <GenreForCard title="Commentaries" texts={this.props.commentaries} />
        <GenreForCard title="Translations" texts={this.props.translations} />
      </div>
    );
  }
});

/** Goes to the given url when clicked. */
const CardNavButton = (props) => {
  const url = props.query || '';
  return <a href={url}>{props.text}</a>;
};
CardNavButton.PropTypes = PaginationState.isRequired;

/** A text listed in the nav. When clicked, the page state is altered to
 * show/hide content from this text. */
const SecondaryTextListItem = React.createClass({
  propTypes: {
    text: TextSchema.isRequired,
    onClick: P.func.isRequired,
  },
  onClick(e) {
    e.preventDefault();
    this.props.onClick(this.props.text.slug);
  },
  render() {
    return (
      <li><a href="#" onClick={this.onClick}>{this.props.text.name}</a></li>
    );
  },
});

/** List of secondary texts in the nav. This is used to toggle texts. */
const SecondaryTextList = (props) => {
  const items = props.active.map((textID) => {
    const data = props.textMap[textID];
    return (
      <SecondaryTextListItem
        key={textID}
        text={data}
        onClick={props.onClick}
      />
    );
  });
  return (
    <div>
      <h3>{props.title}</h3>
      <ul>
        {items}
      </ul>
    </div>
  );
};

/** Everything that changes the page state. */
const Nav = React.createClass({
  render() {
    const prevURL = (this.props.prev) ? this.props.prev.query : '';
    return (
      <nav>
        <CardNavButton {...this.props.prev} text="&laquo;" />
        <CardNavButton {...this.props.next} text="&raquo;" />
        <SecondaryTextList
          title="Translations"
          active={this.props.all_translations}
          textMap={this.props.textMap}
          onClick={this.props.onClickText}
        />
        <SecondaryTextList
          title="Commentaries"
          active={this.props.all_commentaries}
          textMap={this.props.textMap}
          onClick={this.props.onClickText}
        />
      </nav>
    );
  }
});

/** The main app. */
const TextApp = React.createClass({
  propTypes: {
    active_secondary_texts: P.arrayOf(P.number).isRequired,
    commentary_ids: P.arrayOf(P.number).isRequired,
    translation_ids: P.arrayOf(P.number).isRequired,
    cards: P.arrayOf(CardState).isRequired,
    next: PaginationState,
    prev: PaginationState,
    readable_query: P.string.isRequired,
    secondary_texts: P.arrayOf(TextSchema).isRequired,
    text: TextSchema.isRequired,

    // Constructed client-side
    textMap: P.object.isRequired,
  },
  render() {
    // FIXME: better key.
    const cards = this.props.cards.map((data, i) => <Card key={i} {...data} />);
    return (
      <div>
        <Header text={this.props.readable_query} />
        {cards}
        <Nav
          all_commentaries={this.props.commentary_ids}
          all_translations={this.props.translation_ids}
          textMap={this.props.textMap}
          prev={this.props.prev}
          next={this.props.next}
          onClickText={toggleSecondaryText}
        />
      </div>
    );
  }
});

$(function() {
  const url = '/api' + window.location.pathname;
  $.getJSON(url, function(data) {
    const textMap = {};
    data.cards.forEach((card) => {
      data.secondary_texts.forEach((t) => {
        textMap[t.id] = t;
      });
      // Translate foreign keys so the downstream code is simpler.
      card.commentaries.forEach((x) => {
        x.text = textMap[x.text_id];
      });
      card.translations.forEach((x) => {
        x.text = textMap[x.text_id];
      });
    });
    console.log(data);
    ReactDOM.render(
      <TextApp {...data} textMap={textMap} />,
      document.getElementById('segment-view')
    );
  });
});

