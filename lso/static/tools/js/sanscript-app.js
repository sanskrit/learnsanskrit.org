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

        // Build model from DOM defaults
        gather: function() {
            var data = {};
            this.$check.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.is(':checked');
            });
            this.$select.each(function() {
                var $this = $(this);
                data[$this.attr('name')] = $this.val();
            });
            this.model.save(data);
        },

        render: function() {
            // Make view conform to model
            var settings = this.model.toJSON();
            _.each(settings, function(v, k) {
                var $s = $('#' + k);
                if ($s.is(':checkbox')) {
                    $s.prop('checked', v);
                } else {
                    $s.val(v);
                }
            });

            // Update examples
            var $samp = this.$samp,
                from = settings.from_script,
                to = settings.to_script;
            this.$kbd.each(function(i) {
                var $this = $(this),
                    raw = $this.data('raw');
                $this.text( t(raw, 'hk', from, {skip_sgml: true}) ),
                $samp.eq(i).text( t(raw, 'hk', to, settings) );
            });
        }
    });

    var MapView = Backbone.View.extend({
        initialize: function() {
            var template = ('<span class="sa1"><%= to %></span> ' +
                            '<span class="sa2"><%= from %></span>');
            this.template = _.template(template);
            this.model.bind('change', this.render, this);
        },
        render: function() {
            var self = this,
                model = this.model;
            this.$('li').each(function() {
                var $this = $(this),
                    raw = $this.data('raw').toString(),
                    to = t(raw, 'itrans', model.get('to_script')),
                    from = t(raw, 'itrans', model.get('from_script'));
                $this.html(self.template({ to: to, from: from }));
            });
            return this;
        }
    });

    window.App = Backbone.View.extend({
        initialize: function() {
            this.$input = $('#input');
            this.$output = $('#output');

            var model = this.model = new LSO.LocalData({ id: 'sanscript' });
            this.panel = new PanelView({ el: $('form'), model: model });
            this.map = new MapView({ el: $('#t-map'), model: model });

            $('section', 'div.tabs').on('click', 'a', function(e) {
                var selector = $(this).data('spotlight');
                if (selector) {
                    $(selector).spotlight(200);
                    e.preventDefault();
                }
            });

            if (model.isEmpty()) {
                this.panel.gather();
            }

            model.bind('change', this.render, this);

            this.map.render();
            this.panel.render();
        },

        events: {
            // TODO: keyup is slow. But keydown and keypress fire before the
            // new character is added. This can be fixed, but not without a bit
            // more time.
            'keyup #input': 'render',
            'click #submit': 'run_then_select',
            'click #output': 'run_then_select',
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

        run_then_select: function(e) {
            this.run(e);
            this.$output.select();
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
        }
    });
}());

$(function() {
    new App({ el: $('#sanscript') });
    // Remove autoscroll for same-page links
    $(document).off('click', 'a[href*="#"]');
});
