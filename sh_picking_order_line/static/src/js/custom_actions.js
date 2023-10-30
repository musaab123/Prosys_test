odoo.define('sh_picking_order_line.custom_actions', function (require) {
    "use strict";

    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');

    ListView.include({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            var self = this;

            // Add a click event handler to the list view
            this.on("list_view_loaded", this, function () {
                this.$el.on('click', 'tr', function (ev) {
                    var $row = $(ev.currentTarget);
                    var recordID = $row.data('id');
                    self.trigger_up('perform_model_rpc', {
                        method: 'write',
                        model: self.model,
                        args: [recordID, {is_active: true}],
                        on_success: function () {
                            // Refresh the list view to reflect the changes
                            self.reload();
                        },
                    });
                });
            });
        },
    });

    viewRegistry.add('list', ListView);
});
