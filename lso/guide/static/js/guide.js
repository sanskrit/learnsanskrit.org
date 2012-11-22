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
            'keyup': 'render'
        },

        render: function() {
            if (this.done) {

            } else if (this.$input) {
                var guess = this.simplify(this.$input.val());
                if (this.answer == guess) {
                    this.done = true;
                    this.$p.text(this.raw);
                    this.$input.remove();
                    this.$el.addClass('flash')
                        .delay(1000)
                        .queue(function(n) {
                            $(this).removeClass('flash');
                            next();
                        })
                        .addClass('complete');
                }
            }
            else {
                this.$input = $('<input type="text"/>');
                this.$p.html(this.$input);
            }
            return this;
        },

        simplify: function(s) {
            return s.toLowerCase().replace(/[^a-z ]/g, '');
        }
    });


    $(function() {
        $('li.hint', 'ul.examples').each(function() {
            new HintExample({ el: this });
        });
    });
}());