
odoo.define('customer_location_custom.sale_order_geolocation', function (require) {
    'use strict';

    var core = require('web.core');
    var WebClient = require('web.WebClient');
    var _t = core._t;

    WebClient.include({
        show_application: function () {
            var self = this;
            if (self.action_manager.action && self.action_manager.action.res_model === 'sale.order') {
                // Check if the user has granted geolocation permission
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function (position) {
                        var latitude = position.coords.latitude;
                        var longitude = position.coords.longitude;
                        self.do_action({
                            type: 'ir.actions.client',
                            tag: 'reload',
                            name: _t('Reload Sale Order Form'),
                        });
                        self._rpc({
                            model: 'sale.order',
                            method: 'update_geolocation',
                            args: [[self.action_manager.action.res_id], latitude, longitude],
                        });
                    });
                }
            }
            return this._super.apply(this, arguments);
        },
    });
});



