(function(LSO) {

    // Helper functions
    // ----------------

    function is_segment(url) {
        return url.match('^\/(.+)\/(.+)\/(.+)');
    }

    function is_text(url) {
        return url.match('/^\/(.+)\/(.+)\/$/g');
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

    // Segments
    // --------

    var tSegment = [
        '<section id="<%= xmlid %>" class="segment">',
        '    <a class="jump" href="#<%= xmlid %>">#</a>',
        '    <div class="primary"><%= content %></div>',
        '    <div class="translation">',
        '        <% _.each(corresp, function(c_text) { %>',
        '        <% _.each(c_text, function(c_seg) { %>',
        '        <%= c_seg.content %>',
        '        <% }); %>',
        '        <% }); %>',
        '    </div>',
        '</section>'
    ].join('');

    var Segments = Backbone.Collection.extend({
        model: Backbone.Model
    });

    var SegmentView = TemplateView.extend({
        template: _.template(tSegment)
    });

    // Page link
    // ---------

    var PageLink = Backbone.Model;

    var PageLinkView = ModelView.extend({
        render: function() {
            var $el = this.$el,
                a = this.model.attributes;

            var url, readable;
            if (a.query) {
                url = '/texts/' + a.text + '/' + a.query;
                if (a.related) {
                    url += '+' + a.related;
                }
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

    var Title = Backbone.Model;

    var TitleView = ModelView.extend({
        render: function() {
            this.$el.text(this.model.get('title'));
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
            this.title = new Title();

            new PageLinkView({ el: $('#prev-link'), model: this.prevLink });
            new PageLinkView({ el: $('#next-link'), model: this.nextLink });
            new TitleView({ el: $('#readable-query'), model: this.title });

            this.collection = new Segments();
            this.collection.on('all', this.render, this);

            this.$segments = $('#segments');
        },

        events: {
            'click a.jump': 'bookmark',
            'click a.child-link': 'get_children',
            'click a.page-link': 'get_page'
        },

        // Bookmark a given segment
        bookmark: function(e) {
            e.preventDefault();
            var $this = $(e.currentTarget),
                id = $this.attr('href').replace(/\./g, '\\.');
            $('#segment-view').stop().animate({
                scrollTop: $(id).position().top
            }, 500);
        },

        // Get child segments
        get_children: function(e) {
            console.log('get_children');
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
            this.collection.each(function(entry) {
                var view = new SegmentView({ model: entry }).render();
                data.push(view.$el.html());
            });
            this.$segments
                .hide()
                .html(data.join(''))
                .fadeIn(200);
        },

        // Fetch data from the server and store it in the appropriate models.
        query: function(query) {
            var self = this;
            $.getJSON('/api/texts/' + query, function(data) {

                var prev = data['prev'] || {query: null},
                    next = data['next'] || {query: null};
                prev['text'] = next['text'] = data['text']['slug'];
                prev['related'] = next['related'] = data['related'];

                self.title.set('title', data['readable_query']);
                self.prevLink.set(prev);
                self.nextLink.set(next);

                var segments = data['segments'],
                    corresp = data['corresp'] || {};
                segments = _.map(segments, function(x) {
                    x['corresp'] = corresp[x.slug] || {};
                    return x;
                });

                self.collection.reset(segments);
            });
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