(function(LSO) {

    var SettingsModal = LSO.Modal.extend({
        initialize: function() {
            this.proto = LSO.Modal.prototype;

            // Fields to save in the settings object
            this.$fields = undefined;

            // True if the template has been fetched from the server.
            this.loaded = false;
        },

        events: {
            'click a.btn-close': 'hide',
            'change': 'gather'
        },

        /**
         * Show the modal. Fetch the template from the server, if necessary.
         */
        show: function() {
            var self = this;
            if (self.loaded) {
                self.proto.show.apply(self);
            } else {
                $.get('/settings', function(data) {
                    self.$el.html(data)
                        .hide()
                        .appendTo('body');
                    self.proto.show.apply(self);
                    self.loaded = true;
                    self.$fields = $('#sa1, #sa2, #input', self.$el);
                    self.render();
                });
            }
        },

        /**
         * Copy the field data into the model.
         */
        gather: function() {
            var model = this.model;
            this.$fields.each(function() {
                var $this = $(this);
                model.set($this.attr('name'), $this.val());
            });
            console.log(model.attributes);
            model.save();
        },

        /**
         * Copy the model data into the fields.
         */
        render: function() {
            var model = this.model;
            this.$fields.each(function() {
                var $this = $(this),
                    name = $this.attr('name');
                $this.val(model.get(name));
            });
        }
    });

    var App = LSO.Application = Backbone.View.extend({
        initialize: function() {
            this.settings = new SettingsModal({ model: this.model });
        },

        events: {
            'click a[href^=/settings]': 'viewSettings',
            'keyup': 'hideModals'
        },

        /**
         * Hide modals if the escape key is pressed.
         */
        hideModals: function(e) {
            if (e.keyCode == 27) {
                this.settings.hide();
            }
        },

        viewSettings: function(e) {
            e.preventDefault();
            this.settings.show();
        }
    });

}(LSO = window.LSO || {}));