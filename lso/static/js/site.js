(function(LSO) {
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

    /**
     * Convert the given string to a valid ID.
     */
    LSO.toID = function(s) {
        return s.toLowerCase().replace(/[\s]/g, '-').replace(/[:;,.!()"]/g, '');
    };

    LSO.sa1 = function(text, from) {
        from = from || 'slp1';
        return Sanscript.t(text, from, LSO.settings.get('sa1'));
    };

    LSO.sa2 = function(text, from) {
        from = from || 'slp1';
        return Sanscript.t(text, from, LSO.settings.get('sa2'));
    };

    /**
     * Global site settings
     */
    var Settings = LSO.LocalData.extend({
        defaults: {
            sa1: 'devanagari',
            sa2: 'iast',
            input: 'hk'
        }
    });
    LSO.settings = new Settings({ id: 'settings' });

}(window.LSO = window.LSO || {}));