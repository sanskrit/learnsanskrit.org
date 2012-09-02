(function(App) {
    var run = function() {
        var options = App.options,
            from = options.from,
            to = options.to,
            output = Sanscript.t(App.input.$el.val(), from, to);
        App.output.$el.val(output);
    };

    $.fn.swapVal = function($b) {
        var $a = $(this), temp = $a.val();
        $a.val($b.val());
        $b.val(temp);
    }

    var swap = function(e) {
        e.preventDefault();
        App.input.$el.swapVal(App.output.$el);
        App.$to.swapVal(App.$from);
        return false;
    };

    var PanelView = Backbone.View.extend({
        initialize: function() {
            this.$check = $(':checkbox', this.$el);
            this.$select = $('select', this.$el);
            this.gather();
        },
        events: {
            'change': 'gather'
        },

        gather: function(e) {
            var data = App.options = this.data = this.data || {};

            this.$check.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.is(':checked');
            });
            this.$select.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.val();
            });

            data['from'] = data['from_script']
            data['to'] = data['to_script']
            if (e && $(e.target).attr('name') !== 'live-type') {
                run();
            }
        }
    });

    var InputView = Backbone.View.extend({
        events: {
            'keyup': function() {
                if (App.options['live-type']) {
                    run();
                }
            }
        }
    });

    var OutputView = Backbone.View.extend({
        events: {
            'click': run
        }
    });

    App.init = function() {
        this.input = new InputView({ el: $('#input') });
        this.output = new OutputView({ el: $('#output') });
        this.panel = new PanelView({ el: $('form') });

        this.$from = $('#from_script');
        this.$to = $('#to_script');

        $('#submit').click(function(e) {
            run();
            e.preventDefault();
        });
        $('#swap').click(swap);
    }
}(window.App = window.App || {}));

$(function() {
    App.init();

    $('a', '#sanscript').click(function(e) {
        var $this = $(this),
            href = $this.attr('href');
        if (href && href[0] === '#') {
            $(href).spotlight(200);
            e.preventDefault();
        }
    });
});
