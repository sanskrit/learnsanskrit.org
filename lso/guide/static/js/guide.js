(function() {
    var HintExample = Backbone.View.extend({
        initialize: function() {
            this.$p = $('p.en', this.el);
            this.raw = this.$p.text();
            this.answer = this.simplify(this.raw);
            this.done = false;
            this.render();
        },

        events: {
            'click button': 'finish',
            'keyup': 'render'
        },

        finish: function() {
            this.done = true;
            this.$p.text(this.raw);
        },

        render: function() {
            if (this.done) {

            } else if (this.$input) {
                var guess = this.simplify(this.$input.val());
                if (this.answer == guess) {
                    this.finish();
                    this.$el.addClass('complete');
                    this.$el.closest('ul').find('input').first().focus();
                }
            }
            else {
                this.$input = $('<input type="text"/>');
                this.$p.text('')
                    .append(this.$input)
                    .append($('<button>Give up?</button>'));
            }
            return this;
        },

        simplify: function(s) {
            return s.toLowerCase().replace(/[^a-z ]/g, '');
        }
    });

    var Lesson = Backbone.View.extend({

        initialize: function() {
            this.$content = $('#content');
            this.$sidebar = $('#sidebar').pin();
            this.model.bind('change', this.transliterate, this);
            this.rendered = false;
            this.render();
        },

        gatherHeadings: function() {
            var $links = $('<ul>').addClass('headings');
            $('h2', this.$content).each(function() {
                var $this = $(this),
                    id = LSO.toID($this.text()),
                    html = $this.html();
                $this.attr('id', id);
                $('<li>')
                    .wrapInner(
                        $('<a>').attr('href', '#' + id).html(html)
                    )
                    .appendTo($links);
            });
            if ($links.children().length) {
                $links.appendTo($('li.active', this.$sidebar));
            }
        },

        render: function() {
            this.transliterate();
            this.gatherHeadings();
            this.rendered = true;
        },

        transliterate: function() {
            var model = this.model,
                sa1, sa2;
            if (this.rendered) {
                sa1 = model.previous('sa1'),
                sa2 = model.previous('sa2');
            } else {
                sa1 = 'devanagari';
                sa2 = 'iast';
            }

            $('.sa1', this.$el).sanscript(sa1, model.get('sa1'));
            $('.sa2', this.$el).sanscript(sa2, model.get('sa2'));
        }
    });

    $(function() {
        $('li.hint', 'ul.examples').each(function() {
            new HintExample({ el: this });
        });

        new Lesson({ model: LSO.settings, el: $('#lesson') });
    });
}());