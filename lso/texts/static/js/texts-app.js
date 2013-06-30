(function(LSO) {

    // Helper functions
    // ----------------

    function is_segment(url) {
        return url.match('^\/(.+)\/(.+)\/(.+)');
    }

    function is_text(url) {
        return url.match('/^\/(.+)\/(.+)\/$/g');
    }

    function url_child_segments_api(child_slug, parent_ids) {
        return '/api/texts-child/' + child_slug + '/' + parent_ids.join(',');
    }

    function url_query_api(query) {
        return '/api/texts/' + query;
    }

    function url_segment(text, query, related) {
        url = '/texts/' + text + '/' + query;
        if (related && related.length) {
            url += '+' + related.join(',');
        }
        return url;
    }

    function url_text(text) {
        return '/texts/' + text;
    }

    // Helper classes
    // --------------

    var TemplateView = Backbone.View.extend({
        render: function() {
            this.$el.html(this.template(this.model.attributes));
            return this;
        }
    });

    var ModelView = Backbone.View.extend({
        initialize: function() {
            this.model.on('change', this.render, this);
        }
    });

    // State
    // -----
    // A high-lever represenation of the current page. This contains
    // the current query, the active related texts, and the slug of the
    // current text.
    var State = Backbone.Model;


    // Segments
    // --------

    var tSegment = [
        '<section id="<%= xmlid %>" class="segment">',
        '    <a class="jump" href="<%= slug %>">#</a>',
        '    <div class="primary"><%= content %></div>',
        '    <div class="translations">',
        '        <% _.each(corresp, function(c_segs, c_slug) { %>',
        '        <% _.each(c_segs, function(c_seg) { %>',
        '        <div class="translation trans-<%= c_slug %>"><%= c_seg.content %></div>',
        '        <% }); %>',
        '        <% }); %>',
        '    </div>',
        '</section>'
    ].join('');

    var Segment = Backbone.Model;

    var Segments = Backbone.Collection.extend({
        model: Segment
    });

    var SegmentView = TemplateView.extend({
        template: _.template(tSegment)
    });

    // Child links
    // -----------

    var ChildLink = Backbone.Model;

    var ChildLinks = Backbone.Collection.extend({
        model: ChildLink,

        // Get a list of active slugs
        actives: function() {
            var activeList = this.where({ active: true });
            return _.map(activeList, function(x) {
                return x.get('slug');
            });
        }
    });

    var ChildLinksView = Backbone.View.extend({

        initialize: function() {
            var collection = this.collection = new ChildLinks();

            // Initialize from source
            $('a.child-link').each(function() {
                var $this = $(this),
                    datum = {
                        id: $this.data('id'),
                        slug: $this.data('slug'),
                        active: $this.hasClass('active')
                    };
                collection.add(datum);
                console.log(collection.models);
            });
        },

        events: {
            'click a.child-link': 'get_child_segments',
            'mouseover a.child-link': 'hi_child_segments_on',
            'mouseout a.child-link': 'hi_child_segments_off'
        },

        get_child_segments: function(e) {
            e.preventDefault();
            var $link = $(e.currentTarget),
                slug = $link.data('slug'),
                selector = '.trans-' + slug;

            if ($link.hasClass('active')) {
                $link.data('queried', true);
            }
            $link.toggleClass('active');
            if ($link.data('queried')) {
                $(selector).removeClass('hi').fadeToggle();
            } else {
                LSO.textApp.query_child_segments(slug);
                $link.data('queried', true);
            }

            // Update model
            var m = this.collection.findWhere({ 'slug': slug });
            m.set('active', !m.get('active'));
        },

        hi_child_segments: function(e, leaving) {
            var slug = $(e.currentTarget).data('slug'),
                selector = '.trans-' + slug;
            $(selector).toggleClass('hi', leaving);
        },

        hi_child_segments_on: function(e) {
            this.hi_child_segments(e, true);
        },

        hi_child_segments_off: function(e) {
            this.hi_child_segments(e, false);
        }
    });

    // Page links
    // ----------

    var PageLink = Backbone.Model;

    var PageLinkView = ModelView.extend({
        render: function() {
            var $el = this.$el,
                a = this.model.attributes;

            var url, readable;
            if (a.query) {
                url = url_segment(a.text, a.query, a.related);
                readable = a.readable;
            } else {
                url = '/texts/' + a.text;
                readable = '(title page)';
            }
            $el.attr('href', url);
            $el.text(readable);
            return this;
        }
    });

    // Title
    // -----

    var TitleView = ModelView.extend({
        render: function() {
            var title = this.model.get('readable');
            document.title = title;
            this.$el.text(title);
            return this;
        }
    });

    // Router
    // ------

    window.TextRouter = Backbone.Router.extend({
        routes: {
            'texts/*query': 'page'
        },

        page: function(query) {
            LSO.textApp.query(query);
        }
    });

    // Application
    // -----------

    window.TextApp = Backbone.View.extend({
        initialize: function() {
            this.prevLink = new PageLink();
            this.nextLink = new PageLink();
            this.state = new State();

            var childLinksView = new ChildLinksView({ el: $('#child-links') });
            this.childLinks = childLinksView.collection;
            this.childLinks.on('change', this.update_related, this);

            this.prevLinkView = new PageLinkView({
                el: $('#prev-link'),
                model: this.prevLink
            });
            this.nextLinkView = new PageLinkView({
                el: $('#next-link'),
                model: this.nextLink
            });
            this.titleView = new TitleView({
                el: $('#readable-query'),
                model: this.state
            });

            this.segments = new Segments();
            this.segments.on('all', this.render, this);

            this.$segments = $('#segments');
        },

        events: {
            'click a.jump': 'bookmark',
            'click a.page-link': 'get_page'
        },

        // View a single segment by itself
        bookmark: function(e) {
            e.preventDefault();
        },

        // Get a page of segments
        get_page: function(e) {
            var url = $(e.currentTarget).attr('href');
            if (is_segment(url)) {
                e.preventDefault();
                LSO.textRouter.navigate(url, {'trigger': true});
            }
        },

        render: function() {
            var data = [];
            this.segments.each(function(model) {
                var view = new SegmentView({ model: model }).render();
                data.push(view.$el.html());
            });
            this.$segments
                .hide()
                .html(data.join(''))
                .fadeIn(200);
        },

        // Fetch data from the server and store it in the appropriate models.
        query: function(query) {
            var self = this,
                url = url_query_api(query);
            $.getJSON(url, function(data) {

                var prev = data['prev'] || {query: null},
                    next = data['next'] || {query: null};
                prev['text'] = next['text'] = data['text']['slug'];
                prev['related'] = next['related'] = data['related'];

                self.state.set({
                    text: data['text'],
                    query: data['query'],
                    related: data['related'],
                    readable: data['readable_query']
                });
                self.prevLink.set(prev);
                self.nextLink.set(next);

                var segments = data['segments'],
                    corresp = data['corresp'] || {};
                segments = _.map(segments, function(x) {
                    x['corresp'] = corresp[x.slug] || {};
                    return x;
                });

                self.segments.reset(segments);
            });
        },

        // Fetch child segments from the server and store them appropriately.
        query_child_segments: function(slug) {
            var parent_ids = this.segments.map(function(s) {
                return s.get('id');
            }),
                url = url_child_segments_api(slug, parent_ids);

            var self = this;
            $.getJSON(url, function(data) {
                var segments2 = self.segments.map(function(s) {
                    var corresp = s.get('corresp');
                    _.extend(corresp, data[s.id]);
                    return s;
                });
                self.segments.reset(segments2);
            });
        },

        update_related: function() {
            var related = this.childLinks.actives();
            this.state.set('related', related);
            this.prevLink.set('related', related);
            this.nextLink.set('related', related);

            var a = this.state.attributes;
            var url = url_segment(a.text.slug, a.query, a.related);
            LSO.textRouter.navigate(url);
        }
    });

}(LSO = window.LSO || {}));

$(function() {
    // Remove autoscroll for same-page links
    $(document).off('click', 'a[href^="#"]');

    LSO.textApp = new TextApp({ el: $('article') });
    LSO.textRouter = new TextRouter();
    Backbone.history.start({ pushState: true });
});