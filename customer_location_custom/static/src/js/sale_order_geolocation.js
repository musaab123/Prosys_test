odoo.define('customer_location_custom.sale_order_geolocation', function (require) {
    'use strict';

    var core = require('web.core');
    var FormController = require('web.FormController');

    FormController.include({
        _onButtonClicked: function (event) {
            var self = this;
            if (event.data.attrs.name === 'action_confirm') {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function (position) {
                        var latitude = position.coords.latitude;
                        var longitude = position.coords.longitude;
                        self._rpc({
                            model: self.modelName,
                            method: 'update_geolocation',
                            args: [[self.handle, self.res_id], latitude, longitude],
                        }).then(function () {
                            self.trigger_up('reload');
                            self.trigger_up('history_back');
                        });
                    });
                }
            } else {
                this._super.apply(this, arguments);
            }
        },
    });
});


