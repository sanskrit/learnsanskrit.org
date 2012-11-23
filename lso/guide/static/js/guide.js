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

    var gatherHeadings = function() {
        var $links = $('<ul>').addClass('headings');
        $('h2', '#content').each(function() {
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
        $links.appendTo($('li.active', '#sidebar'));
    };

    $(function() {
        $('li.hint', 'ul.examples').each(function() {
            new HintExample({ el: this });
        });
        $('#sidebar').pin();
        gatherHeadings();
    });
}());