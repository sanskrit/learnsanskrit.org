(function(ns) {
    ns.SettingsApp = Backbone.View.extend({
        initialize: function() {
            var template = $('#settings-form').html();
            this.$el.html(template);
            this.$sa1 = $('#sa1');
            this.$sa2 = $('#sa2');
            this.render();
        },
        events: {
            'change': 'gather'
        },
        gather: function() {
            var model = this.model;
            model.set('sa1', this.$sa1.val());
            model.set('sa2', this.$sa2.val());
            model.save();
        },

        render: function() {
            var model = this.model;
            this.$sa1.val(model.get('sa1'));
            this.$sa2.val(model.get('sa2'));
        }
    });
}(window));

$(function() {
    new SettingsApp({ el: $('#app'), model: LSO.settings });
});