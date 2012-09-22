(function() {
    var t = Sanscript.t;

    var Entries = Backbone.Collection.extend({
        model: Backbone.Model
    });

    var EntryView = Backbone.View.extend({
        initialize: function() {
            this.template = _.template($('#t-entry').html());
        },

        render: function() {
            var attr = this.model.attributes;
            this.$el.html(this.template({ entry: attr.entry,
                                          definitions: attr.definitions }));
            return this;
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
            'click #submit': 'query'
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

        query: function(e) {
            e.preventDefault();
            var self = this,
                q = this.form.$q.val(),
                from = this.form.$from.val(),
                slp_query = t(q, from, 'slp1');

            slp_query = slp_query.replace(/[,; ]/g, '+');
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
