/*/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useBus, useService } from '@web/core/utils/hooks';
patch(FormController.prototype, "sale_geolocation/static/src/js/form_controller.js", {
    async saveButtonClicked(params = {}) {
        await this._super(params);
        var self = this;
        if(this.model && this.model.root && this.model.root.resModel == 'sale.order' && this.model.root.resId){
            var latitude = '';
                var longitude = '';
                var gelocation_error_msg = '';
                navigator.geolocation.getCurrentPosition(
                    function(pos) {
                        var crd = pos.coords;
                        latitude = crd.latitude;
                        longitude = crd.longitude;
                        self.model.orm.call(
                            self.model.root.resModel,
                            'write',
                            [[self.model.root.resId], { latitude: latitude, longitude: longitude }],
                            { context: self.user.context}
                        );
                    },
                    function(error) {
                        switch (error.code) {
                            case error.PERMISSION_DENIED:
                                gelocation_error_msg = "User denied the request for Geolocation."
                            case error.POSITION_UNAVAILABLE:
                                gelocation_error_msg = "Location information is unavailable.";
                            case error.TIMEOUT:
                                gelocation_error_msg = "The request to get user location timed out."
                            case error.UNKNOWN_ERROR:
                                gelocation_error_msg = "An unknown error occurred."
                        }
                        self.model.orm.call(
                            self.model.root.resModel,
                            'write',
                            [[self.model.root.resId], { gelocation_error_msg: gelocation_error_msg}],
                            { context: self.user.context}
                        );
                    }, {
                        enableHighAccuracy: true,
                        timeout: 5000,
                        maximumAge: 0
                    }
                );
        }
    }

});