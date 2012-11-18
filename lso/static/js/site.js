(function(LSO) {
    if (localStorage) {
        var store = localStorage;
    } else {
        var store = {
            getItem: $.cookie,
            setItem: $.cookie,
            removeItem: $.cookie
        }
    }

    /**
     * localStorage with a cookie fallback
     */
    LSO.LocalData = Backbone.Model.extend({
        initialize: function() {
            this.fetch();
        },

        fetch: function() {
            this.set(JSON.parse(store.getItem(this.id)));
        },

        save: function(attributes) {
            this.set(attributes);
            store.setItem(this.id, JSON.stringify(this.toJSON()));
        },

        destroy: function(options) {
            store.removeItem(this.id);
        },

        isEmpty: function() {
            return (_.size(this.attributes) <= 1); // just 'id'
        }
    });
}(window.LSO = window.LSO || {}));