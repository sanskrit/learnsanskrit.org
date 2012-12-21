(function(LSO) {
    /**
     * Modal window
     */
    LSO.Modal = Backbone.View.extend({
        initialize: function() {
            this.duration = 50;
            this.$el.hide();
        },

        events: {
            'click a.btn-close': 'hide'
        },

        show: function() {
            var self = this,
                duration = 150;
            self.$el.spotlightOn(duration).fadeIn(duration);
            $('#spotlight').one('click', function() {
                self.hide();
            });
        },

        hide: function() {
            var duration = 150;
            this.$el.spotlightOff(duration).fadeOut(duration);
        }
    });
}(LSO = window.LSO || {}));