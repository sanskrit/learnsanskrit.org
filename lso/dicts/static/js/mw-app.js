(function() {
    var t = Sanscript.t;

    var Entries = Backbone.Collection.extend({
        model: Backbone.Model
    });

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
            return this;
        },

        addLinks: function() {
            var view = this,
                entry = this.model.get('entry');
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

                $span.wrapInner(view.link_template({ text: text }));
            });
        }
    });

    var FormView = Backbone.View.extend({
        initialize: function() {
            var $el = this.$el;
            this.$q = $('#q', $el);
            this.$from = $('#from_script', $el);
            this.$to = $('#to_script', $el);
        }
    });

    window.App = Backbone.View.extend({
        initialize: function() {
            this.$entries = $('#mw-entries');

            var collection = this.collection = new Entries();
            this.form = new FormView({ el: $('form', this.$el) });

            this.collection.on('all', this.render, this);
        },

        events: {
            'click #submit': 'form_query',
            'click a.reflink': 'link_query',
        },

        render: function() {
            var $entries = this.$entries,
                to = this.form.$to.val(),
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
            var q = this.form.$q.val(),
                from = this.form.$from.val(),
                slp_query = t(q, from, 'slp1').replace(/\W/g, '+');

            this.query(slp_query);
        },

        link_query: function(e) {
            e.preventDefault();
            var $link = $(e.currentTarget);
            this.query($link.data('text'));
        },

        query: function(slp_query) {
            var self = this;
            $.getJSON('/api/mw/' + slp_query, function(data) {
                var terms = slp_query.split('+'),
                    sorted_data = [];
                for (var i = 0, t; t = terms[i]; i++) {
                    sorted_data.push({ entry: t, definitions: data[t] });
                }
                self.collection.reset(sorted_data);
            });
        }
    });
}());

$(function() {
    new App({ el: $('#mw') });
});
