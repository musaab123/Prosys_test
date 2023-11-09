odoo.define('partner_location.geolocation', function (require) {
    "use strict";

        var core = require('web.core');
        var FormController = require('web.FormController');
    
        var _t = core._t;
    
        FormController.include({
            _onButtonGetLocation: function () {
                var self = this;
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function (position) {
                        var latitude = position.coords.latitude;
                        var longitude = position.coords.longitude;
                        self._rpc({
                            model: 'res.partner',
                            method: 'action_get_location',
                            args: [self.state.res_id, latitude, longitude],
                        }).then(function (result) {
                            self.reload();
                        });
                    }, function (error) {
                        console.error(_t("Geolocation error: " + error.message));
                    });
                } else {
                    console.error(_t("Geolocation is not supported by this browser."));
                }
            },
        });
    });
    