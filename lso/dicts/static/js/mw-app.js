(function() {
    var t = Sanscript.t,
        GREEK_URL = 'http://www.perseus.tufts.edu/hopper/morph?l=',
        CITE_URL = '/dict/mw/works-and-authors';

    var Entries = Backbone.Collection.extend({
        model: Backbone.Model
    });

    /**
     * Dictionary entry
     */
    var EntryView = Backbone.View.extend({
        initialize: function() {
            this.template = _.template($('#t-entry').html());
            this.link_template = _.template($('#t-reflink').html());
        },

        render: function() {
            var model = this.model;
            this.$el.html(this.template({ entry: model.get('entry'),
                                          definitions: model.get('definitions') }));
            this.addLinks();
            this.addTooltips();
            return this;
        },

        addLinks: function() {
            var entry = this.model.get('entry'),
                link_template = this.link_template;
            $('span.sa2', this.$el).each(function() {
                var $span = $(this),
                    text = $span.text().replace(/#/g, '');

                // Difficult cases
                if (text.match(/[ *°]/g)) {
                    return;
                }

                // Join with searched word
                if (text.charAt(0) == '-') {
                    text = entry + text;
                } else if (text.charAt(text.length-1) == '-') {
                    text = text + entry;
                }

                text = text.replace(/\W/g, '');

                $span.wrapInner(link_template({ text: text,
                    url: '/dict/mw/q-slp1/' }));
            });
            $('span.gk', this.$el).each(function() {
                var $span = $(this),
                    url = GREEK_URL + $span.text();
                $span.wrapInner($('<a/>').attr({href: url, target: '_blank'}));
            });
            $('cite', this.$el).each(function() {
                var $this = $(this),
                    code = $this.text().split(' ')[0].replace(/[^A-z0-9]/g, ''),
                    $link = $('<a/>').attr({
                        'class': 'mw-cite',
                        'href': CITE_URL + '#' + code,
                        target: 'citations' });
                $this.wrap($link);
            });
        },


        addTooltips: function() {
            $('abbr', this.$el).each(function() {
                var $elem = $(this),
                    abbr = $elem.text().replace(/[^A-z]/g, ''),
                    title = MW.app.abbr[abbr] || '(unknown)';
                $elem.attr('title', title);
                $elem.data("aoeu", 'bcde');
            });
        }
    });

    window.Routes = Backbone.Router.extend({
        routes: {
            'dict/mw/q-:from/:query': 'search',
        },

        search: function(from, q) {
            MW.app.query(Sanscript.t(q, from, 'slp1'));
        }
    });

    window.App = Backbone.View.extend({
        initialize: function() {
            var self = this;
            this.$entries = $('#mw-entries');

            // Normal abbreviations, like 'nom.'
            $.getJSON('/static/dict/data/mw-abbr.json', function(data) {
                self.abbr = data;
            });

            var collection = this.collection = new Entries();
            this.collection.on('all', this.render, this);
        },

        events: {
            'click #submit': 'form_query',
            'click a.reflink': 'link_query'
        },

        render: function() {
            var $entries = this.$entries,
                to = LSO.settings.get('sa1'),
                strings = ['##'];
            this.collection.each(function(entry) {
                var view = new EntryView({ model: entry }).render();
                strings.push(view.$el.html());
            });
            $entries
                .hide()
                .html(t(strings.join(''), 'slp1', to, {skip_html: true}))
                .fadeIn(200);
        },

        form_query: function(e) {
            e.preventDefault();
            var q = $('#q').val().replace(/\W/g, '+'),
                from = LSO.settings.get('input');

            var url = 'dict/mw/q-' + from + '/' + q;
            MW.routes.navigate(url, {trigger: true, replace: true});
        },

        link_query: function(e) {
            e.preventDefault();
            var url = 'dict/mw/q-slp1/' + $(e.currentTarget).data('text');
            MW.routes.navigate(url, {trigger: true});
        },

        query: function(slp_query) {
            var self = this;
            $.getJSON('/api/mw/' + slp_query, function(data) {
                var terms = slp_query.split('+'),
                    sorted_data = [];
                for (var i = 0, t; (t = terms[i]); i++) {
                    sorted_data.push({ entry: t, definitions: data[t] });
                }
                self.collection.reset(sorted_data);
            });
        }
    });
}());

$(function() {
    var MW = window.MW = {};
    MW.app = new App({ el: $('#mw') });
    MW.routes = new Routes();
    Backbone.history.start({ pushState: true });
});
