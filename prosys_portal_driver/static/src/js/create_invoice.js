odoo.define("prosys_portal_driver.create_invoice", function (require) {
  "use strict";
  var ajax = require("web.ajax");

  $(document).ready(function () {
    $("#create_invoice_button").on("click", function () {
      var vals = [];
      // submission.preventDefault();
      $("tr.order_line").each(function () {
        vals.push({ order_id: $(this).find(".quantity").data("order-id") });
        ajax
          .jsonRpc("/portal/create_invoice", "call", {
            vals: vals,
          })
          .then(function(result){
                if (result == true){
                  window.location.href = '/my/about/page';

                }
                else{
                    window.location.href = '/my/about/page';

                }
            });
      });
    });
  });
});
