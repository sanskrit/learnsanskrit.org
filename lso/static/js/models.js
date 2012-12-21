(function(LSO) {
    /**
     * localStorage with a cookie fallback
     */
    var store;
    if (localStorage) {
        store = localStorage;
    } else {
        store = {
            getItem: $.cookie,
            setItem: $.cookie,
            removeItem: $.cookie
        };
    }

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

    /**
     * Global site settings
     */
    LSO.Settings = LSO.LocalData.extend({
        defaults: {
            sa1: 'devanagari',
            sa2: 'iast',
            input: 'hk'
        }
    });

}(LSO = window.LSO || {}));