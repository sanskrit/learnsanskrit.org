(function() {
    var t = Sanscript.t;

    var Settings = Backbone.Model;

    var PanelView = Backbone.View.extend({
        initialize: function() {
            var $el = this.$el;
            this.$from = $('#from_script');
            this.$to = $('#to_script');
            this.$check = $(':checkbox', $el);
            this.$select = $('select', $el);
            this.$kbd = $('kbd', $el);
            this.$samp = $('samp', $el);

            var $options = $('#options').hide();

            $('a[href=#options]').toggle(
                function(e) {
                    e.preventDefault();
                    $options.slideDown(200);
                    $(this).data('text', $(this).text());
                    $(this).text('Too many options?');
                },
                function(e) {
                    e.preventDefault();
                    $options.slideUp(200);
                    $(this).text($(this).data('text'));
                }
            );
            this.model.bind('change', this.render, this);
        },

        events: {
            'change': 'gather'
        },

        gather: function() {
            var data = {}
            this.$check.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.is(':checked');
            });
            this.$select.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.val();
            });
            this.model.set(data);
        },

        render: function() {
            var settings = this.model.attributes,
                from = settings.from_script,
                to = settings.to_script;
            var $kbd = this.$kbd,
                $samp = this.$samp;
            $kbd.each(function(i) {
                var $this = $(this),
                    raw = $this.data('raw'),
                    input = t(raw, 'hk', from, {skip_sgml: true}),
                    output = t(raw, 'hk', to, settings);
                $this.text(input);
                $samp.eq(i).text(output);
            });
        }
    });

    var MapView = Backbone.View.extend({
        initialize: function() {
            var template = ('<span class="sa1"><%= to %></span> '
                            + '<span class="sa2"><%= from %></span>');
            this.template = _.template(template);
            this.model.bind('change', this.render, this);
        },
        render: function() {
            var self = this,
                settings = this.model.attributes;
            this.$('li').each(function() {
                var $this = $(this),
                    raw = $this.data('raw').toString(),
                    to = t(raw, 'itrans', settings.to_script),
                    from = t(raw, 'itrans', settings.from_script);
                $this.html(self.template({ to: to, from: from }));
            });
            return this;
        }
    });

    window.App = Backbone.View.extend({
        initialize: function() {
            this.$input = $('#input');
            this.$output = $('#output');

            var model = this.model = new Settings;

            this.panel = new PanelView({ el: $('form'), model: model });
            this.map = new MapView({ el: $('#t-map'), model: model });

            $('section', 'div.tabs').on('click', 'a', function(e) {
                var selector = $(this).data('spotlight');
                if (selector) {
                    $(selector).spotlight(200);
                    e.preventDefault();
                }
            });

            this.model.bind('change', this.render, this);
            this.panel.gather();
        },

        events: {
            'keyup #input': 'render',
            'click #submit': 'run',
            'click #output': 'run',
            'click #swap': 'swap',
            'click #swap-link': 'swap',
        },

        render: function() {
            if (this.model.get('live-type')) {
                this.run();
            }
        },

        run: function(e) {
            var settings = this.model.attributes,
                from = settings.from_script,
                to = settings.to_script,
                output = t(this.$input.val(), from, to, settings);
            this.$output.val(output);
            if (e) {
                e.preventDefault();
            }
        },

        swap: function(e) {
            e.preventDefault();

            var $input = this.$input,
                $output = this.$output,
                $from = this.panel.$from,
                $to = this.panel.$to,
                temp;

            temp = $input.val();
            $input.val($output.val());
            $output.val(temp);

            temp = $from.val();
            $from.val($to.val());
            $to.val(temp);

            this.panel.gather();
        },
    });
}());

$(function() {
    new App({ el: $('#sanscript') });
});
