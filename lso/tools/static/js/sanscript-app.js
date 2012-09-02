(function(App) {
    var run = function() {
        var from = App.from.$el.val(),
            to = App.to.$el.val(),
            output = Sanscript.t(App.input.$el.val(), from, to);
        App.output.$el.val(output);
        return false;
    };

    $.fn.swapVal = function($b) {
        var $a = $(this), temp = $a.val();
        $a.val($b.val());
        $b.val(temp);
    }

    var swap = function() {
        App.from.$el.swapVal(App.to.$el);
        App.input.$el.swapVal(App.output.$el);
        return false;
    };

    var SelectView = Backbone.View.extend({
        events: {
            'change': 't'
        },

        t: run
    });
    var TextView = Backbone.View.extend({

    });
    App.init = function() {
        this.$el = $('form');
        this.from = new SelectView({ el: $('#from_script') });
        this.to = new SelectView({ el: $('#to_script') });
        this.input = new TextView({ el: $('#input').blur(run) });
        this.output = new TextView({ el: $('#output') });

        $('#submit').click(run);
        $('#swap').click(swap);
    }
}(window.App = window.App || {}));

$(function() {
    App.init();

    $('a', '#sanscript').click(function(e) {
        var $this = $(this),
            href = $this.attr('href');
        if (href && href[0] === '#') {
            $(href).spotlight();
            e.preventDefault();
        }
    });
});
