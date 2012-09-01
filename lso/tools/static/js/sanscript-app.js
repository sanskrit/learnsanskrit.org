(function(App) {
    var transliterate = function() {
        var from = App.from.$el.val(),
            to = App.to.$el.val(),
            output = Sanscript.t(App.input.$el.val(), from, to);
        App.output.$el.val(output);
    }

    var SelectView = Backbone.View.extend({
        events: {
            'change': 't'
        },

        t: transliterate
    });
    var TextView = Backbone.View.extend({

    });
    App.init = function() {
        this.$el = $('form');
        this.from = new SelectView({ el: $('#from_script') });
        this.to = new SelectView({ el: $('#to_script') });
        this.input = new TextView({ el: $('#input') });
        this.output = new TextView({ el: $('#output') });

        $('#submit, #output').click(function(e) {
            e.preventDefault();
            transliterate();
        });
    }
}(window.App = window.App || {}));

$(function() {
    App.init();
});
