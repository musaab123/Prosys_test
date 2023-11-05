odoo.define("posys_partner_extra_info.my_location_geolocation", function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var latitude = "";
    var longitude = "";

    
    var partner_id = -1;

    $(document).on('click', '#get_partner_location', function() {
        navigator.geolocation.getCurrentPosition(setCurrentPosition, positionError, {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0,
        });

        function setCurrentPosition(position) {
            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
            var diam = '=';
            document.URL.split("#")[1].split("&").forEach(
                function(param){
                    if(param.search("id=") == 0 ){
                        partner_id = parseInt(param.split(diam)[1]);
                    }
                } 
            );

            rpc.query({
                model: "res.partner",
                method: "write",
                args: [[partner_id], {"partner_latitude":latitude,"partner_longitude":longitude ,"google_map_link":"http://maps.google.com/maps?q="+latitude+ "," +longitude}],
            });

            document.getElementById("partner_latitude").value= latitude;
            document.getElementById("partner_longitude").value= longitude;
            document.getElementById("google_map_link").value= "http://maps.google.com/maps?q="+latitude+ "," +longitude;

        }

        function positionError(error) {
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    console.error("User denied the request for Geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    console.error("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    console.error("The request to get user location timed out.");
                    break;
                case error.UNKNOWN_ERROR:
                    console.error("An unknown error occurred.");
                    break;
            }
        }

    });
    
    });
    
