(function(App) {
    var t = Sanscript.t;

    var run = function() {
        var options = App.options,
            from = options.from_script,
            to = options.to_script,
            output = t(App.input.$el.val(), from, to, options);
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

        App.panel.gather();
        App.panel.updateExamples();
    };

    var PanelView = Backbone.View.extend({
        initialize: function() {
            var $el = this.$el;
            this.$check = $(':checkbox', $el);
            this.$select = $('select', $el);
            this.$kbd = $('kbd', $el);
            this.$samp = $('samp', $el);
            this.gather();
        },
        events: {
            'change': 'update'
        },

        update: function(e) {
            this.gather();
            if (e && $(e.target).attr('name') !== 'live-type') {
                run();
            }
            this.updateExamples();
        },

        // Store all options in App.options.
        gather: function() {
            var data = App.options = this.data = this.data || {};

            this.$check.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.is(':checked');
            });
            this.$select.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.val();
            });
        },

        // Update panel examples
        updateExamples: function() {
            var options = App.options,
                from = options.from_script,
                to = options.to_script;
            var $kbd = this.$kbd,
                $samp = this.$samp;
            $kbd.each(function(i) {
                var $this = $(this),
                    raw = $this.data('raw'),
                    input = t(raw, 'hk', from, {'skip_sgml': true}),
                    output = t(raw, 'hk', to, options);
                $this.text(input);
                $samp.eq(i).text(output);
            });
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
        var $form = $('form'),
            $options = $('#options', $form);
        this.input = new InputView({ el: $('#input') });
        this.output = new OutputView({ el: $('#output') });
        this.panel = new PanelView({ el: $form });

        this.$from = $('#from_script');
        this.$to = $('#to_script');

        $('#submit').click(function(e) {
            run();
            e.preventDefault();
        });
        $('#swap').click(swap);

        $options.hide();
        $('a[href=#options]', $form).toggle(
            function(e) {
                e.preventDefault();
                $options.fadeIn();
                $(this).data('text', $(this).text());
                $(this).text('Too many options?');
            },
            function(e) {
                e.preventDefault();
                $options.fadeOut();
                $(this).text($(this).data('text'));
            }
        );
    }
}(window.App = window.App || {}));

$(function() {
    App.init();
    $('div.tabs').tabs();

    $('a', 'div.directions').click(function(e) {
        var $this = $(this),
            href = $this.attr('href');
        if (href && href[0] === '#') {
            $(href).spotlight(200);
            e.preventDefault();
        }
    });
});
