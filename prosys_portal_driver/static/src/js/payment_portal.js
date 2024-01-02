odoo.define('prosys_portal_driver.create_payment', function (require) {
    "use strict";
    var ajax = require('web.ajax');

    $('#sale_order_create_payment').on('submit', function(submission) {
        submission.preventDefault();
        var vals = {
             'partner_id' : $(this).find("#partner_payment").val(),
             'driver_id' : $(this).find("#driver_payment").val(),
             'amount' : $(this).find("#amount").val(),
             'ref' : $(this).find("#disabledSelect").val() + '#'+ $(this).find("#partner_memo").val(),


        }
        
                         

               
       
        if (vals.length !== 0){
            ajax.jsonRpc('/portal/create_payment', 'call', vals).then(function(result){
                if (result == true){
                  window.location.href = '/my/payment/successfuly';

                }
                else{
                    window.location.href = '/my/payment/successfuly';

                }
            });
        }
        else{
            alert("Please specify at least one return quantity");
            submission.preventDefault();
        }
    });

});
