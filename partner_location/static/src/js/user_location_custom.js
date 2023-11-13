odoo.define("partner_location.user_location_geolocation", function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var latitude = "";
    var longitude = "";

    
    var task_id = -1;

    $(document).on('click', '#get_user_location_task', function() {
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
                        task_id = parseInt(param.split(diam)[1]);
                    }
                } 
            );

            rpc.query({
                model: "project.task",
                method: "write",
                args: [[task_id], {"in_latitude":latitude,"in_longitude":longitude ,"google_map_link_id":"http://maps.google.com/maps?q="+latitude+ "," +longitude}],
            });
            
            document.getElementById("in_latitude").value= latitude;
            document.getElementById("in_longitude").value= longitude;

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
    




   