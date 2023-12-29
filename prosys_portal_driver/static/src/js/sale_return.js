odoo.define('prosys_portal_driver.sale_return', function (require) {
    "use strict";
    var ajax = require('web.ajax');

// $("#sale_order_return_portal").on('submit', function (ev) {

//         var $link = $(ev.currentTarget);
//         var $input = $link.closest('.input-group').find("input");
//         var min = parseFloat($input.data("min") || 0);
//         var max = parseFloat($input.data("max") || Infinity);
//         var previousQty = parseFloat($input.val() || 0, 10);
//         var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
//         var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
//         if (newQty !== previousQty) {
//             $input.val(newQty).trigger('change');
//         }
//         return false;
//     })
//    Form submit function
    $('#sale_order_return_portal').on('submit', function(submission) {
        var val = []
        submission.preventDefault();
        $("tr.order_line").each(function() {
        var qty = parseFloat($(this).find(".quantity").val() || 0);
            if (qty !== 0){
                    val.push({ 'order_id' : $(this).find(".quantity").data("order-id"),
                        'line_id' : $(this).find(".quantity").data("line-id"),
                        'deli_qty' : $(this).find(".quantity").data("delivered_qty"),
                         'quantity' : $(this).find(".quantity").val(),
                         'product_id' : $(this).find(".quantity").data('product-id'),
                         });
                }
        });
        // if (val.length !== 0){
        //     ajax.jsonRpc('/portal/return_order', 'call', {
        //                 'vals':val,
        //                 'reason' : $(this).find("#return_reason").val()
        //     }).then(function(result){
        //         $('#returnModal').modal("toggle")
               
        //     });
        // }
        // else{
        //     alert("Please specify at least one return quantity");
        //     submission.preventDefault();
        // }

        if (val.length !== 0){
            ajax.jsonRpc('/portal/return_order', 'call', {
                        'vals':val,
                        'reason' : $(this).find("#return_reason").val()
            }).then(function(result){
                if (result == true){
                  window.location.href = '/my/about/page';

                }
                else{
                    window.location.href = '/my/about/page';

                }
            });
        }
        else{
            alert("Please specify at least one return quantity");
            submission.preventDefault();
        }
    });
});
