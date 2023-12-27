odoo.define('prosys_product_portal.portal_add_product', function (require) {
    "use strict";
    // var core = require('web.core');
    // var Dialog = require("web.Dialog");
    // var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    // var websiteRootData = require('website.root');
    // var utils = require('web.utils');
    // var field_utils = require('web.field_utils');
    // var _t = core._t;
    // var qweb = core.qweb;
    var latitude = "";
    var longitude = "";
    window.location_data = "";
    // const time = require('web.time');
    // var currentUser = session.uid;
    // var html5QrcodeScanner = new Html5QrcodeScanner(
    //     "reader", { fps: 10, qrbox: 250 });
            
    // function onScanSuccess(decodedText, decodedResult) {
    //     // Handle on success condition with the decoded text or result.
    //     console.log(`Scan result: ${decodedText}`, decodedResult);
    //     const resultDiv = document.getElementById("scanproduct");
    //     resultDiv.value = decodedResult;
    //     // ...
    //     html5QrcodeScanner.clear();
    //     // ^ this will stop the scanner (video feed) and clear the scan area.
    // }
    
    // html5QrcodeScanner.render(onScanSuccess);

    // function onScanSuccess(decodedText, decodedResult) {
    //     // Handle on success condition with the decoded text or result.
    //     console.log(`Scan result: ${decodedText}`, decodedResult);
    // }

    // var html5QrcodeScanner = new Html5QrcodeScanner(
    //     "reader", { fps: 10, qrbox: 250 });
    // function onScanSuccess(decodedText, decodedResult) {
    //     // Handle on success condition with the decoded text or result.
    //     const resultDiv = document.getElementById("barcode");
    //     resultDiv.value = decodedText;
    //     console.log(`Scan result: ${decodedText}`, decodedResult);
    //     // if (decodedResult){
    //     //     alert(decodedResult);
    //     // }
    // }

    // function onScanError(errorMessage) {
    //     // handle on error condition, with error message
    // }

    // var html5QrcodeScanner = new Html5QrcodeScanner(
    //     "reader", { fps: 500, qrbox: {width: 950, height: 950} });
    // html5QrcodeScanner.render(onScanSuccess, onScanError);
    
        // document.addEventListener("DOMContentLoaded", function() {
        //     const modal = document.getElementById("myModal");
        //     const scanButton = document.getElementById("scanButton");

        //     // Open the modal and initialize scanner when the button is clicked
        //     scanButton.addEventListener("click", function() {
        //         modal.style.display = "block";

        //         const html5QrcodeScanner = new Html5QrcodeScanner(
        //         "reader", { fps: 500, qrbox: { width: 950, height: 950 }, facingMode: "environment" }
        //         );

        //         html5QrcodeScanner.render(onScanSuccess, onScanError);
        //     });

        //     // Close the modal when the user clicks outside of it
        //     window.onclick = function(event) {
        //         if (event.target === modal) {
        //         modal.style.display = "none";
        //         }
        //     };
        // });

        //     function onScanSuccess(decodedText, decodedResult) {
        //     const resultDiv = document.getElementById("barcode");
        //     resultDiv.value = decodedText;
        //     console.log(`Scan result: ${decodedText}`, decodedResult);
        //     closeModal(); // Close the modal after successful scan
        //     }

        //     function onScanError(errorMessage) {
        //     // Handle scan error
        //     closeModal(); // Close the modal after error
        //     }

        //     function closeModal() {
        //     const modal = document.getElementById("myModal");
        //     modal.style.display = "none";
        //     }




    publicWidget.registry.portal_add_product = publicWidget.Widget.extend({
        
        selector: '.js_add_product',
        events: {
            // 'click #scanproduct': '_onClickScanProduct',
            'click #searchproduct': '_onClicksearchproduct',
            'click #salessearchproduct': '_onClicksalessearchproduct',
            'click #addpro-button': '_onClickaddprobutton',
            'click #addsalespro-button': '_onClickaddsalesprobutton',
            'click .delete_button': '_onClickdeletebutton',
            'click #Submitrequest': '_onClickSubmitrequest',
            'click #saverequest': '_onClicksaverequest',
            'click #increse': '_onClickincrese',
            'click #decrese': '_onClickdecrese',
            'click #increaseQuantity': '_onClickincreaseQuantity',
            'click #decreaseQuantity': '_onClickdecreaseQuantity',
            'click #increasevalQuantity': '_onClickincreasevalQuantity',
            'click #decreasevalQuantity': '_onClickdecreasevalQuantity',
            'click #UserSubmitrequest': '_onClickSubmituserrequest',
            'click #incresediscount': '_onClickincresediscount',
            'click #decresediscount': '_onClickdecresediscount',
            'click #increase_discount': '_onClickincreasediscountsa',
            'click #decrease_discount': '_onClickdecreasediscountsa',
            'change #quantity': '_onClickdquantity',
            'change .final_quantity': '_onClickdfinal_quantity',

            
            // 'click #scanreader': '_onclickreaderimg',
            

            
        },
        async start() {
            await this._super(...arguments);

            console.log('start');
        },

        // async _onclickreaderimg() {
        //     modal.style.display = "block";

        //     const html5QrcodeScanner = new Html5QrcodeScanner(
        //     "reader", { fps: 500, qrbox: { width: 950, height: 950 }, facingMode: "environment" }
        //     );

        //     html5QrcodeScanner.render(onScanSuccess, onScanError);
        // }
        async _onClickdquantity(){
            const quantity = document.getElementById('quantity');

            if (quantity.value < 0){
                quantity.value = 0;
            }
        },

        async _onClickdfinal_quantity(event){
            var button = event.target;

            if (button.value < 0){
                button.value = 0;
            }
        },

        async _onClickScanProduct() {
            alert("Image clicked!");
        },
        async _onClickincrese() {
            const quantity = document.getElementById('quantity');
            quantity.value = parseInt(quantity.value) + 1
        },
        async _onClickdecrese() {
            const quantity = document.getElementById('quantity');
            if (parseInt(quantity.value) != 1){
                quantity.value = parseInt(quantity.value) - 1
            }
        },
        async _onClickincreaseQuantity(event) {
            var button = event.target;
            var rowval = $(button).attr("rowval");
            
            var rowvalue = parseInt(rowval);
            const quantity = document.getElementById('final_quantity['+rowvalue+']');
            quantity.value = parseInt(quantity.value) + 1
        },
        async _onClickdecreaseQuantity(event) {
            var button = event.target;
            var rowval = $(button).attr("rowval");
            
            var rowvalue = parseInt(rowval);
            const quantity = document.getElementById('final_quantity['+rowvalue+']');
            if (parseInt(quantity.value) != 1){
                quantity.value = parseInt(quantity.value) - 1
            }


        },


        async _onClickincreasevalQuantity(event) {
            var button = event.target;
            var rowval = $(button).attr("rowval");
            
            var rowvalue = parseInt(rowval);
            const quantity = document.getElementById('final_quantity['+rowvalue+']');
            quantity.value = parseInt(quantity.value) + 1

            var subtotal = 0
            var dis_value = 0
            var total = 0


            const counter = $("input[name='counter']").val();
            const products_list = []
            for (let i = 1; i <= counter; i++) {
                var pro_result = {}
                const product_id = $("input[name='product_id["+i+"]']").val();
                console.log(product_id)
                if (product_id){
                    const final_quantity = $("input[name='final_quantity["+i+"]']").val();
                    const final_discount = $("input[name='final_discount["+i+"]']").val();
                    const priceval = $("input[name='priceval["+i+"]']").val();
                    subtotal += parseFloat(priceval) * parseFloat(final_quantity)
                    dis_value += (parseFloat(priceval) * parseFloat(final_quantity)) * (final_discount / 100)
                    pro_result['product_id'] = product_id
                    pro_result['product_uom_qty'] = final_quantity 
                    pro_result['discount'] = final_discount 
                    products_list.push(pro_result);
                }
            }
            
            const subtotalval = document.getElementById('subtotal');
            subtotalval.innerHTML = subtotal

            const distotal = document.getElementById('distotal');
            distotal.innerHTML = dis_value.toFixed(2)

            const totalval = document.getElementById('total');
            var tovals = subtotal - dis_value
            totalval.innerHTML = tovals.toFixed(2)
        },
        async _onClickdecreasevalQuantity(event) {
            var button = event.target;
            var rowval = $(button).attr("rowval");
            
            var rowvalue = parseInt(rowval);
            const quantity = document.getElementById('final_quantity['+rowvalue+']');
            if (parseInt(quantity.value) != 1){
                quantity.value = parseInt(quantity.value) - 1
            }
            
            var subtotal = 0
            var dis_value = 0
            var total = 0


            const counter = $("input[name='counter']").val();
            const products_list = []
            for (let i = 1; i <= counter; i++) {
                var pro_result = {}
                const product_id = $("input[name='product_id["+i+"]']").val();
                console.log(product_id)
                if (product_id){
                    const final_quantity = $("input[name='final_quantity["+i+"]']").val();
                    const final_discount = $("input[name='final_discount["+i+"]']").val();
                    const priceval = $("input[name='priceval["+i+"]']").val();
                    subtotal += parseFloat(priceval) * parseFloat(final_quantity)
                    dis_value += (parseFloat(priceval) * parseFloat(final_quantity)) * (final_discount / 100)
                    pro_result['product_id'] = product_id
                    pro_result['product_uom_qty'] = final_quantity 
                    pro_result['discount'] = final_discount 
                    products_list.push(pro_result);
                }
            }
            
            const subtotalval = document.getElementById('subtotal');
            subtotalval.innerHTML = subtotal

            const distotal = document.getElementById('distotal');
            distotal.innerHTML = dis_value.toFixed(2)

            const totalval = document.getElementById('total');
            var tovals = subtotal - dis_value
            totalval.innerHTML = tovals.toFixed(2)

            
        },

        // increase and decrease for discount input field
        async _onClickincresediscount() {
            const discount = document.getElementById('discount');
            discount.value = parseInt(discount.value) + 1
        },
        async _onClickdecresediscount() {
            const discount = document.getElementById('discount');
            if (parseInt(discount.value) != 1){
                discount.value = parseInt(discount.value) - 1
            }
        },
        async _onClickincreasediscountsa(event) {
            var button = event.target;
            var rowval = $(button).attr("rowval");
            
            var rowvalue = parseInt(rowval);
            const discount = document.getElementById('final_discount['+rowvalue+']');
            discount.value = parseInt(discount.value) + 1


            var subtotal = 0
            var dis_value = 0
            var total = 0


            const counter = $("input[name='counter']").val();
            const products_list = []
            for (let i = 1; i <= counter; i++) {
                var pro_result = {}
                const product_id = $("input[name='product_id["+i+"]']").val();
                console.log(product_id)
                if (product_id){
                    const final_quantity = $("input[name='final_quantity["+i+"]']").val();
                    const final_discount = $("input[name='final_discount["+i+"]']").val();
                    const priceval = $("input[name='priceval["+i+"]']").val();
                    subtotal += parseFloat(priceval) * parseFloat(final_quantity)
                    dis_value += (parseFloat(priceval) * parseFloat(final_quantity)) * (final_discount / 100)
                    pro_result['product_id'] = product_id
                    pro_result['product_uom_qty'] = final_quantity 
                    pro_result['discount'] = final_discount 
                    products_list.push(pro_result);
                }
            }
            
            const subtotalval = document.getElementById('subtotal');
            subtotalval.innerHTML = subtotal

            const distotal = document.getElementById('distotal');
            distotal.innerHTML = dis_value.toFixed(2)

            const totalval = document.getElementById('total');
            var tovals = subtotal - dis_value
            totalval.innerHTML = tovals.toFixed(2)
        },
        async _onClickdecreasediscountsa(event) {
            var button = event.target;
            var rowval = $(button).attr("rowval");
            
            var rowvalue = parseInt(rowval);
            const discount = document.getElementById('final_discount['+rowvalue+']');
            if (parseInt(discount.value) != 1){
                discount.value = parseInt(discount.value) - 1
            }

            var subtotal = 0
            var dis_value = 0
            var total = 0


            const counter = $("input[name='counter']").val();
            const products_list = []
            for (let i = 1; i <= counter; i++) {
                var pro_result = {}
                const product_id = $("input[name='product_id["+i+"]']").val();
                console.log(product_id)
                if (product_id){
                    const final_quantity = $("input[name='final_quantity["+i+"]']").val();
                    const final_discount = $("input[name='final_discount["+i+"]']").val();
                    const priceval = $("input[name='priceval["+i+"]']").val();
                    subtotal += parseFloat(priceval) * parseFloat(final_quantity)
                    dis_value += (parseFloat(priceval) * parseFloat(final_quantity)) * (final_discount / 100)
                    pro_result['product_id'] = product_id
                    pro_result['product_uom_qty'] = final_quantity 
                    pro_result['discount'] = final_discount 
                    products_list.push(pro_result);
                }
            }
            
            const subtotalval = document.getElementById('subtotal');
            subtotalval.innerHTML = subtotal

            const distotal = document.getElementById('distotal');
            distotal.innerHTML = dis_value.toFixed(2)

            const totalval = document.getElementById('total');
            var tovals = subtotal - dis_value
            totalval.innerHTML = tovals.toFixed(2)
        },

        // Public user screen searched product retrive
        async _onClicksearchproduct() {
            var result = {}
            var barcode = $("input[name='barcode']").val();
            result['barcode'] = barcode

            if (barcode == ''){
                alert("Please add barcode!!");
            }else{

                ajax.jsonRpc('/check/get_product_by_barcode', 'call', result).then( function(data){
                    var product = data['product']
                    var alert_msg = data['alert']
                    var company = data['company']



                    if (product){
                        const temp_product_div = document.getElementById('temp_product_div');
                        if (temp_product_div) {
                            temp_product_div.remove();
                        }
                        // Create the main container div with class "card" and other attributes
                        const mainContainerDiv = document.createElement('div');
                        mainContainerDiv.classList.add('card', 'border-0', 'p-4', 'gap-2', 'align-items-center');
                        mainContainerDiv.setAttribute('id', "temp_product_div");

                        // Create the row for the product card
                        const productCardRow = document.createElement('div');
                        productCardRow.classList.add('row', 'product-card','w-50');
                        productCardRow.style.borderBottom ="1px solid #E1E1E1";


                        // Create the column for the image
                        const imageColumn = document.createElement('div');
                        imageColumn.classList.add('col-md-5', 'col-sm-12');

                        // Create the image element
                        const imgElement = document.createElement('img');
                        imgElement.setAttribute('src', "data:image;base64," + product[0].image_1920 + "");
                        imgElement.setAttribute('title', "ProductImage");
                        imgElement.setAttribute('style', "width:96px;height:96px;object-fit: contain; border-radius:10px;");
                        imgElement.setAttribute('alt', "ProductImage");

                        // Append the image element to the image column
                        imageColumn.appendChild(imgElement);

                        // Create the column for product details
                        const productDetailsColumn = document.createElement('div');
                        productDetailsColumn.classList.add('col-md-7', 'col-sm-12', 'my-3', 'text-left');

                        // Create the row for the product name
                        const productNameRow = document.createElement('div');
                        productNameRow.classList.add('row');

                        // Create the span element for product name
                        const productNameSpan = document.createElement('span');
                        productNameSpan.setAttribute('id', 'pro_name_value');
                        productNameSpan.textContent = product[0].name;

                        // Append the product name span to the product name row
                        productNameRow.appendChild(productNameSpan);

                        // lllllllllllllllllllllllllllllllllllllllllllllllllll
                         // Create the row for quantity and price
                        const detailsRow = document.createElement('div');
                        detailsRow.classList.add('row', 'pt-4');

                        const priceColumn =document.createElement('div');
                        priceColumn.classList.add('col-md-6', 'col-sm-12');
                        priceColumn.style.textAlign = "right";

                        const quantityColumnParent = document.createElement('div');
                        quantityColumnParent.classList.add('col-md-6', 'col-sm-12');
                        // lllllllllllllllllllllllllllllllllllllllllllllllllll

                        // Create the row for the price
                        const priceRow = document.createElement('div');
                        priceRow.classList.add('row');

                        // Create the span element for price
                        const priceSpan = document.createElement('span');
                        priceSpan.setAttribute('id', 'price_value');
                        priceSpan.textContent = "$"+product[0].lst_price;

                        // Append the price span to the price row
                        priceRow.appendChild(priceSpan);
                        priceColumn.appendChild(priceRow);


                        // Create the row for quantity and buttons
                        const quantityButtonRow = document.createElement('div');
                        quantityButtonRow.classList.add('row');

                        // // Create the column for quantity
                        // const quantityColumn = document.createElement('div');
                        // quantityColumn.classList.add('col-md-6');

                        // // Create the span element for quantity
                        // const quantitySpan = document.createElement('span');
                        // quantitySpan.textContent = "Quantity :";

                        // // Append the quantity span to the quantity column
                        // quantityColumn.appendChild(quantitySpan);

                        // // Create the column for remove button
                        // const removeButtonColumn = document.createElement('div');
                        // removeButtonColumn.classList.add('col-md-2');

                        // // Create the span element for remove button
                        // const removeButtonSpan = document.createElement('span');
                        // removeButtonSpan.innerHTML = '<ion-icon class="tut" name="remove" id="decrese"></ion-icon>';

                        // // Append the remove button span to the remove button column
                        // removeButtonColumn.appendChild(removeButtonSpan);

                        // // Create the column for the quantity input
                        // const quantityInputColumn = document.createElement('div');
                        // quantityInputColumn.classList.add('col-md-2');

                        // // Create the input element for quantity
                        // const quantityInput = document.createElement('input');
                        // quantityInput.setAttribute('type', 'text');
                        // quantityInput.setAttribute('id', 'quantity');
                        // quantityInput.setAttribute('name', 'quantity');
                        // // quantityInput.setAttribute('readonly', 'readonly');
                        // quantityInput.style.width = '25px';
                        // quantityInput.value = '1';

                        // // Append the quantity input to the quantity input column
                        // quantityInputColumn.appendChild(quantityInput);

                        // // Create the column for add button
                        // const addButtonColumn = document.createElement('div');
                        // addButtonColumn.classList.add('col-md-2');

                        // // Create the span element for add button
                        // const addButtonSpan = document.createElement('span');
                        // addButtonSpan.innerHTML = '<ion-icon class="tut" name="add-outline" id="increse"></ion-icon>';

                        // // Append the add button span to the add button column
                        // addButtonColumn.appendChild(addButtonSpan);


                        // // Create parent <div> element
                        // const parentDiv = document.createElement("div");
                        // parentDiv.className = "row";

                        // Create <span> element for "Quantity"
                        const quantityproSpan = document.createElement("span");
                        // quantityproSpan.textContent = "Quantity : ";
                        quantityproSpan.style.height = "30px";
                        quantityproSpan.style.textAlign ="center";
                        
                        quantityproSpan.style.border = "1px solid #F3F3F4";
                        quantityproSpan.style.borderRadius = "15px";
                        // quantityaddInput.style.boxSizing = "border-box";
                        quantityproSpan.style.backgroundColor = "#F3F3F4";
                        quantityproSpan.style.outline = "none";

                        // Create "Decrease" button (ion-icon) with ID "decrese"
                        const decreaseqtyButton = document.createElement("ion-icon");
                        decreaseqtyButton.className = "tut md hydrated";
                        decreaseqtyButton.setAttribute("name", "remove");
                        decreaseqtyButton.setAttribute("id", "decrese");
                        decreaseqtyButton.setAttribute("role", "img");

                        // Create <input> element for quantity with ID "quantity"
                        const quantityaddInput = document.createElement("input");
                        quantityaddInput.setAttribute("type", "text");
                        quantityaddInput.setAttribute("id", "quantity");
                        quantityaddInput.setAttribute("name", "quantity");
                        quantityaddInput.setAttribute("value", 1);
                        quantityaddInput.style.width = "40px";
                        quantityaddInput.style.height = "28px";
                        quantityaddInput.style.textAlign ="center";
                        quantityaddInput.style.border = "0px solid black";
                        quantityaddInput.style.borderRadius = "15px";
                        quantityaddInput.style.backgroundColor = "#F3F3F4";
                        quantityaddInput.style.outline = "none";


                        // Create "Increase" button (ion-icon) with ID "increse"
                        const increaseqtyButton = document.createElement("ion-icon");
                        increaseqtyButton.className = "tut md hydrated";
                        increaseqtyButton.setAttribute("name", "add-outline");
                        increaseqtyButton.setAttribute("id", "increse");
                        increaseqtyButton.setAttribute("role", "img");

                        // Append elements to parent elements
                        quantityproSpan.appendChild(decreaseqtyButton);
                        quantityproSpan.appendChild(quantityaddInput);
                        quantityproSpan.appendChild(increaseqtyButton);
                        quantityButtonRow.appendChild(quantityproSpan);
                        quantityColumnParent.appendChild(quantityButtonRow);


                        // Append parent <div> element to the desired location in the DOM
                        // const container = document.getElementById("container-id"); // Replace with your container ID
                        // container.appendChild(parentDiv);


                        // Create the input element for product_id
                        const productIdInput = document.createElement('input');
                        productIdInput.setAttribute('type', 'text');
                        productIdInput.setAttribute('id', 'product_id');
                        productIdInput.setAttribute('name', 'product_id');
                        productIdInput.setAttribute('value', product[0].id);
                        productIdInput.style.display = 'none'; // To make it invisible


                        const productimageidIdInput = document.createElement('input');
                        productimageidIdInput.setAttribute('type', 'text');
                        productimageidIdInput.setAttribute('id', 'product_image_id');
                        productimageidIdInput.setAttribute('name', 'product_image_id');
                        productimageidIdInput.setAttribute('value', product[0].image_1920);
                        productimageidIdInput.style.display = 'none';

                        // Append all the elements to their respective parents
                        // quantityButtonRow.appendChild(quantityColumn);
                        // quantityButtonRow.appendChild(removeButtonColumn);
                        // quantityButtonRow.appendChild(quantityInputColumn);
                        // quantityButtonRow.appendChild(addButtonColumn);

                        // productDetailsColumn.appendChild(productNameRow);
                        // productDetailsColumn.appendChild(priceRow);
                        // productDetailsColumn.appendChild(quantityButtonRow);
                        // productDetailsColumn.appendChild(productIdInput);
                        // productDetailsColumn.appendChild(productimageidIdInput);

                        // productCardRow.appendChild(imageColumn);
                        // productCardRow.appendChild(productDetailsColumn);

                        // mainContainerDiv.appendChild(productCardRow);
                        detailsRow.appendChild(quantityColumnParent);
                        detailsRow.appendChild(priceColumn);

                        productDetailsColumn.appendChild(productNameRow);
                        productDetailsColumn.appendChild(detailsRow);
                        // productDetailsColumn.appendChild(quantityButtonRow);
                        productDetailsColumn.appendChild(productIdInput);
                        productDetailsColumn.appendChild(productimageidIdInput);

                        productCardRow.appendChild(imageColumn);
                        productCardRow.appendChild(productDetailsColumn);

                        mainContainerDiv.appendChild(productCardRow);
                        // const addproSpan = document.createElement('span');
                        // const addpro = document.createElement('ion-icon');
                        // addpro.setAttribute('class', 'tut');
                        // addpro.setAttribute('name', 'add-outline');
                        // addpro.setAttribute('id', 'addpro');
                        // mainContainerDiv.appendChild(addpro);

                        const addproButton = document.createElement('a'); // Create the button element
                        addproButton.setAttribute('id', 'addpro-button');
                        addproButton.setAttribute('style', 'color: #276e72;font-size: 30px;');
                        
                        // Set the id attribute for the button

                        const addproIcon = document.createElement('ion-icon'); // Create the ion-icon element
                        addproIcon.setAttribute('class', 'tut'); // Set the class attribute for the ion-icon
                        addproIcon.setAttribute('name', 'add-outline'); // Set the name attribute for the ion-icon
                        addproButton.style.color = "#FFF";
                        addproButton.style.textAlign = "center";
                        addproButton.style.width = "76px";
                        addproButton.style.height = "56px";
                        addproButton.style.backgroundColor = "#1FC069";
                        addproButton.style.padding = "10px";
                        addproButton.style.borderRadius = "8px";
                        addproButton.style.marginTop = "60px";

                        

                        // Append the addproIcon inside the addproButton
                        addproButton.appendChild(addproIcon);

                        // Append the addproButton to the mainContainerDiv
                        mainContainerDiv.appendChild(addproButton);

                        // Add the main container div to the div with id "divcontainer"
                        const cardContainer = document.getElementById('cardContainer');
                        cardContainer.appendChild(mainContainerDiv);

                        const companyInput = document.getElementById('company');
                        companyInput.value = company;

                        // const currencyInput = document.getElementById('currency');
                        // currencyInput.value = currency;
                    }else{
                        alert(alert_msg);
                    }

                    

                    
                    
                });
                var barcode_in = document.getElementById('barcode');
                barcode_in.value = '';
            }
        },


        // Salesmen screen searched product retrive
        async _onClicksalessearchproduct() {
            var result = {}
            var barcode = $("input[name='barcode']").val();
            result['barcode'] = barcode

            ajax.jsonRpc('/check/get_product_by_barcode', 'call', result).then( function(data){
                var product = data['product']
                var alert_msg = data['alert']
                var company = data['company']



                if (product){
                    const temp_product_div = document.getElementById('temp_product_div');
                    if (temp_product_div) {
                        temp_product_div.remove();
                    }
                    // Create the main container div with class "card" and other attributes
                    const mainContainerDiv = document.createElement('div');
                    mainContainerDiv.classList.add('card', 'border-0', 'p-4', 'gap-2', 'align-items-center');
                    mainContainerDiv.setAttribute('id', "temp_product_div");

                    // Create the row for the product card
                    const productCardRow = document.createElement('div');
                    productCardRow.classList.add('row', 'product-card');

                    // Create the column for the image
                    const imageColumn = document.createElement('div');
                    imageColumn.classList.add('col-md-6', 'col-sm-12');

                    // Create the image element
                    const imgElement = document.createElement('img');
                    imgElement.setAttribute('src', "data:image;base64," + product[0].image_1920 + "");
                    imgElement.setAttribute('title', "ProductImage");
                    imgElement.setAttribute('style', "width:96px;height:96px;object-fit: contain; border-radius:10px;");
                    imgElement.setAttribute('alt', "ProductImage");

                    // Append the image element to the image column
                    imageColumn.appendChild(imgElement);

                    // Create the column for product details
                    const productDetailsColumn = document.createElement('div');
                    productDetailsColumn.classList.add('col-md-6', 'col-sm-12', 'my-3', 'text-left');

                    // Create the row for the product name
                    const productNameRow = document.createElement('div');
                    productNameRow.classList.add('row');

                    // Create the span element for product name
                    const productNameSpan = document.createElement('span');
                    productNameSpan.setAttribute('id', 'pro_name_value');
                    productNameSpan.textContent = product[0].name;

                    // Append the product name span to the product name row
                    productNameRow.appendChild(productNameSpan);

                    // Create the row for the price
                    const priceRow = document.createElement('div');
                    priceRow.classList.add('row');

                    // Create the span element for price
                    const priceSpan = document.createElement('span');
                    priceSpan.setAttribute('id', 'price_value');
                    priceSpan.textContent = "Price :   "+product[0].lst_price;


                    const pricevalInput = document.createElement('input');
                    pricevalInput.setAttribute('type', 'text');
                    pricevalInput.setAttribute('id', "pricevals");
                    pricevalInput.setAttribute('name', "pricevals");
                    pricevalInput.setAttribute('value', product[0].lst_price);
                    pricevalInput.style.width = '25px';
                    pricevalInput.style.display = 'none';
                    
                    // Append the price span to the price row
                    priceRow.appendChild(priceSpan);
                    priceRow.appendChild(pricevalInput);

                    // Create the row for quantity and buttons
                    const quantityButtonRow = document.createElement('div');
                    quantityButtonRow.classList.add('row');

                    // Create the column for quantity
                    const quantityColumn = document.createElement('div');
                    quantityColumn.classList.add('col-md-6');

                    // Create the span element for quantity
                    const quantitySpan = document.createElement('span');
                    quantitySpan.textContent = "Quantity :";

                    // Append the quantity span to the quantity column
                    quantityColumn.appendChild(quantitySpan);

                    // Create the column for remove button
                    const removeButtonColumn = document.createElement('div');
                    removeButtonColumn.classList.add('col-md-2');

                    // Create the span element for remove button
                    const removeButtonSpan = document.createElement('span');
                    removeButtonSpan.innerHTML = '<ion-icon class="tut" name="remove" id="decrese"></ion-icon>';

                    // Append the remove button span to the remove button column
                    removeButtonColumn.appendChild(removeButtonSpan);

                    // Create the column for the quantity input
                    const quantityInputColumn = document.createElement('div');
                    quantityInputColumn.classList.add('col-md-2');

                    // Create the input element for quantity
                    const quantityInput = document.createElement('input');
                    quantityInput.setAttribute('type', 'text');
                    quantityInput.setAttribute('id', 'quantity');
                    quantityInput.setAttribute('name', 'quantity');
                    // quantityInput.setAttribute('readonly', 'readonly');
                    quantityInput.style.width = '25px';
                    quantityInput.value = '1';

                    // Append the quantity input to the quantity input column
                    quantityInputColumn.appendChild(quantityInput);

                    // Create the column for add button
                    const addButtonColumn = document.createElement('div');
                    addButtonColumn.classList.add('col-md-2');

                    // Create the span element for add button
                    const addButtonSpan = document.createElement('span');
                    addButtonSpan.innerHTML = '<ion-icon class="tut" name="add-outline" id="increse"></ion-icon>';

                    // Append the add button span to the add button column
                    addButtonColumn.appendChild(addButtonSpan);

                    // adding discount input
                    const discountButtonRow = document.createElement('div');
                    discountButtonRow.setAttribute('class','row mt-2');

                    // Create the column for discount
                    const discountColumn = document.createElement('div');
                    discountColumn.classList.add('col-md-6');

                    // Create the span element for discount
                    const discountSpan = document.createElement('span');
                    discountSpan.textContent = "Discount : ";

                    // Append the discount span to the discount column
                    discountColumn.appendChild(discountSpan);

                    // Create the column for remove button
                    const removediscountButtonColumn = document.createElement('div');
                    removediscountButtonColumn.classList.add('col-md-2');

                    // Create the span element for remove button
                    const removediscountButtonSpan = document.createElement('span');
                    removediscountButtonSpan.innerHTML = '<ion-icon class="tut" name="remove" id="decresediscount"></ion-icon>';

                    // Append the remove button span to the remove button column
                    removediscountButtonColumn.appendChild(removediscountButtonSpan);

                    // Create the column for the discount input
                    const discountInputColumn = document.createElement('div');
                    discountInputColumn.classList.add('col-md-2');

                    // Create the input element for discount
                    const discountInput = document.createElement('input');
                    discountInput.setAttribute('type', 'text');
                    discountInput.setAttribute('id', 'discount');
                    discountInput.setAttribute('name', 'discount');
                    discountInput.setAttribute('readonly', 'readonly');
                    discountInput.style.width = '25px';
                    discountInput.value = '0';
                    // Append the discount input to the discount input column
                    discountInputColumn.appendChild(discountInput);

                    // Create the column for add button
                    const adddiscountButtonColumn = document.createElement('div');
                    adddiscountButtonColumn.classList.add('col-md-2');

                    // Create the span element for add button
                    const adddiscountButtonSpan = document.createElement('span');
                    adddiscountButtonSpan.innerHTML = '<ion-icon class="tut" name="add-outline" id="incresediscount"></ion-icon>';

                    // Append the add button span to the add button column
                    adddiscountButtonColumn.appendChild(adddiscountButtonSpan);

                    // Create the input element for product_id
                    const productIdInput = document.createElement('input');
                    productIdInput.setAttribute('type', 'text');
                    productIdInput.setAttribute('id', 'product_id');
                    productIdInput.setAttribute('name', 'product_id');
                    productIdInput.setAttribute('value', product[0].id);
                    productIdInput.style.display = 'none'; // To make it invisible


                    const productimageidIdInput = document.createElement('input');
                    productimageidIdInput.setAttribute('type', 'text');
                    productimageidIdInput.setAttribute('id', 'product_image_id');
                    productimageidIdInput.setAttribute('name', 'product_image_id');
                    productimageidIdInput.setAttribute('value', product[0].image_1920);
                    productimageidIdInput.style.display = 'none';

                    // Append all the elements to their respective parents
                    quantityButtonRow.appendChild(quantityColumn);
                    quantityButtonRow.appendChild(removeButtonColumn);
                    quantityButtonRow.appendChild(quantityInputColumn);
                    quantityButtonRow.appendChild(addButtonColumn);


                    discountButtonRow.appendChild(discountColumn);
                    discountButtonRow.appendChild(removediscountButtonColumn);
                    discountButtonRow.appendChild(discountInputColumn);
                    discountButtonRow.appendChild(adddiscountButtonColumn);

                    productDetailsColumn.appendChild(productNameRow);
                    productDetailsColumn.appendChild(priceRow);
                    productDetailsColumn.appendChild(quantityButtonRow);
                    productDetailsColumn.appendChild(discountButtonRow);
                    productDetailsColumn.appendChild(productIdInput);
                    productDetailsColumn.appendChild(productimageidIdInput);

                    productCardRow.appendChild(imageColumn);
                    productCardRow.appendChild(productDetailsColumn);

                    mainContainerDiv.appendChild(productCardRow);
                    // const addproSpan = document.createElement('span');
                    // const addpro = document.createElement('ion-icon');
                    // addpro.setAttribute('class', 'tut');
                    // addpro.setAttribute('name', 'add-outline');
                    // addpro.setAttribute('id', 'addpro');
                    // mainContainerDiv.appendChild(addpro);

                    const addproButton = document.createElement('a'); // Create the button element
                    addproButton.setAttribute('id', 'addsalespro-button');
                    addproButton.setAttribute('style', 'color: #276e72;font-size: 30px;');
                    
                    // Set the id attribute for the button

                    const addproIcon = document.createElement('ion-icon'); // Create the ion-icon element
                    addproIcon.setAttribute('class', 'tut'); // Set the class attribute for the ion-icon
                    addproIcon.setAttribute('name', 'add-outline'); // Set the name attribute for the ion-icon

                    

                    // Append the addproIcon inside the addproButton
                    addproButton.appendChild(addproIcon);

                    // Append the addproButton to the mainContainerDiv
                    mainContainerDiv.appendChild(addproButton);

                    // Add the main container div to the div with id "divcontainer"
                    const cardContainer = document.getElementById('cardContainer');
                    cardContainer.appendChild(mainContainerDiv);

                    const companyInput = document.getElementById('company');
                    companyInput.value = company;

                    // const currencyInput = document.getElementById('currency');
                    // currencyInput.value = currency;
                }else{
                    alert(alert_msg);
                }

                

                
                
            });
        },


        // adding product for the public user part
        async _onClickaddprobutton() {


            const price_value = document.getElementById('price_value');
            var price_val = price_value.textContent

            const pro_name_value = document.getElementById('pro_name_value');
            var pro_name_val = pro_name_value.textContent

            const qty_value = document.getElementById('quantity');
            var qty_val = qty_value.value

            const counter_value = document.getElementById('counter');
            counter_value.value = parseInt(counter_value.value) + 1
            var counter_val = counter_value.value

            const product_value = document.getElementById('product_id');
            var product_val = product_value.value

            

            const product_image_id = document.getElementById('product_image_id');
            var product_img_id = product_image_id.value

            

            // Create the main container div
            const mainContainerDiv = document.createElement('div');
            mainContainerDiv.setAttribute('class', 'col-md-4 col-sm-12');
            mainContainerDiv.setAttribute('id', "product_div["+counter_val+"]");

            // Create the card div
            const cardDiv = document.createElement('div');
            cardDiv.setAttribute('class', 'card m-3 border-0 gap-2 align-items-center row');

            // Create the product card row
            const productCardRow = document.createElement('div');
            productCardRow.setAttribute('class', 'product-card row');
            productCardRow.setAttribute('style', 'border-bottom: 1px solid #CECFD2');

            // Create the product image column
            const productImageCol = document.createElement('div');
            productImageCol.setAttribute('class', 'col-md-5 col-sm-12');
            
            // productImageCol.setAttribute('style', 'text-align:center;');
            
            // const imageColumn = document.createElement('div');
            // imageColumn.classList.add('col-md-5', 'col-sm-12');

            // Create the product image element
            const productImage = document.createElement('img');
            productImage.setAttribute('src', "data:image;base64," + product_img_id + "");
            productImage.setAttribute('alt', 'product image');
            productImage.setAttribute('width', '96');
            productImage.setAttribute('height', '96');
            productImage.setAttribute('style', "object-fit: contain;border-radius:10px; position:relative;top: -13px;");

            // imageColumn.appendChild(productImage);   
    

            


            // Append the product image inside the product image column
            productImageCol.appendChild(productImage);

            // Create the product details column
            const productDetailsCol = document.createElement('div');
            productDetailsCol.setAttribute('class', 'col-md-7 col-sm-12');

            // Create the product name row
            const productNameRow = document.createElement('div');
            productNameRow.setAttribute('class', 'row');

            const productNameSpan = document.createElement('span');
            productNameSpan.setAttribute('class', 'col-md-10 col-sm-10');
            productNameSpan.textContent = pro_name_val;
            productNameRow.appendChild(productNameSpan);

            // for delete button
            const centercontainerRow = document.createElement('div');
            centercontainerRow.setAttribute('class', 'col-md-2 col-sm-2');
            const deleteButton = document.createElement('button');
            deleteButton.setAttribute('class', 'delete_button btn btn-outline-danger');
            deleteButton.setAttribute('style', ' position: relative;top: -10px;left: -21px;');

            deleteButton.setAttribute('rowval', counter_val);
            deleteButton.setAttribute('id', "del_product_div["+counter_val+"]");
            deleteButton.innerHTML = '<ion-icon class="tut md hydrated" name="trash-outline" role="img"></ion-icon>';

        
            // Append the delete button to the product details column
            centercontainerRow.appendChild(deleteButton);
            
            // Append delete button to the name row
            productNameRow.appendChild(centercontainerRow);

            // Add Row to wrap quantity and price
            const detailsRow = document.createElement('div');
            detailsRow.setAttribute('class', 'row');

            const priceColumn =document.createElement('div');
            priceColumn.setAttribute('class', 'col-md-6 col-sm-12');
            priceColumn.style.textAlign = "right";

            const quantityColumnParent = document.createElement('div');
            quantityColumnParent.setAttribute('class', 'col-md-6 col-sm-12');

            // Create the product price row
            const productPriceRow = document.createElement('div');
            productPriceRow.setAttribute('class', 'row');
            const productPriceSpan = document.createElement('span');
            productPriceSpan.textContent = price_val;
            productPriceRow.appendChild(productPriceSpan);

            priceColumn.appendChild(productPriceRow);

            

            // Create the product quantity row
            const productQuantityRow = document.createElement('div');
            // productQuantityRow.setAttribute('class', 'row test');
            const productQuantityLabel = document.createElement('span');
            productQuantityRow.style.height = "30px";
            productQuantityRow.style.textAlign ="center";
            
            productQuantityRow.style.border = "1px solid #F3F3F4";
            productQuantityRow.style.borderRadius = "15px";
            productQuantityRow.style.backgroundColor = "#F3F3F4";
            productQuantityRow.style.outline = "none";

            // productQuantityLabel.textContent = 'Quantity :';
            const productQuantityInput = document.createElement('input');
            productQuantityInput.setAttribute('class', 'final_quantity');
            // productQuantityInput.style.display = 'none';

            

           
           

            productQuantityInput.setAttribute('type', 'text');
            productQuantityInput.setAttribute('id', "final_quantity["+counter_val+"]");
            productQuantityInput.setAttribute('name', "final_quantity["+counter_val+"]");
            // productQuantityInput.setAttribute('readonly', 'readonly');
            // hear edit
            // quantityaddInput.style.width = "40px";
            // quantityaddInput.style.height = "28px";
            // quantityaddInput.style.textAlign ="center";
            
            // quantityaddInput.style.border = "0px solid black";
            // quantityaddInput.style.borderRadius = "15px";
            // // quantityaddInput.style.boxSizing = "border-box";
            // quantityaddInput.style.backgroundColor = "#F3F3F4";
            // quantityaddInput.style.outline = "none";
            // hear edit
            productQuantityInput.setAttribute('style', 'width:40px;height:28px;text-align: center;border:0px solid black;border-radius: 15px;background-color: #F3F3F4; outline: none;');
            productQuantityInput.setAttribute('value', qty_val);
            const increaseQuantityIcon = document.createElement('ion-icon');
            increaseQuantityIcon.setAttribute('class', 'tut');
            increaseQuantityIcon.setAttribute('id', 'increaseQuantity');
            increaseQuantityIcon.setAttribute('rowval', counter_val);
            increaseQuantityIcon.setAttribute('name', 'add-outline');
            const decreaseQuantityIcon = document.createElement('ion-icon');
            decreaseQuantityIcon.setAttribute('class', 'tut');
            decreaseQuantityIcon.setAttribute('id', 'decreaseQuantity');
            // decreaseQuantityIcon.setAttribute('style', 'width:100px;height:28px;text-align: center;border:2px solid black;border-radius: 15px;background-color: #F3F3F4; outline: none;');

            decreaseQuantityIcon.setAttribute('rowval', counter_val);
            decreaseQuantityIcon.setAttribute('name', 'remove');

            // Append the elements to the respective rows
            // productQuantityRow.appendChild(productQuantityLabel);            
            productQuantityRow.appendChild(decreaseQuantityIcon);
            productQuantityRow.appendChild(productQuantityInput);
            productQuantityRow.appendChild(increaseQuantityIcon);

            quantityColumnParent.appendChild(productQuantityRow);

            // Append the rows to the product details column
            productDetailsCol.appendChild(productNameRow);

            detailsRow.appendChild(quantityColumnParent);
            detailsRow.appendChild(priceColumn);
            // productDetailsCol.appendChild(productPriceRow);
            // productDetailsCol.appendChild(productQuantityRow);
            productDetailsCol.appendChild(detailsRow);

            // Append the product image column and product details column to the product card row
            productCardRow.appendChild(productImageCol);
            productCardRow.appendChild(productDetailsCol);


            const productIdInput = document.createElement('input');
            productIdInput.setAttribute('type', 'text');
            productIdInput.setAttribute('id', "product_id["+counter_val+"]");
            productIdInput.setAttribute('name', "product_id["+counter_val+"]");
            productIdInput.setAttribute('value', product_val);
            productIdInput.style.display = 'none';
            productCardRow.appendChild(productIdInput);

            
            // productCardRow.appendChild(centercontainerRow);






            // Append the product card row to the card div
            cardDiv.appendChild(productCardRow);

            // Append the card div to the main container div
            mainContainerDiv.appendChild(cardDiv);

            // Append the main container div to the body (or any other parent element you want)
            const cardContainer = document.getElementById('extirnal');
            cardContainer.appendChild(mainContainerDiv);
            // document.body.appendChild(mainContainerDiv);

            const temp_product_div = document.getElementById('temp_product_div');
            if (temp_product_div) {
                temp_product_div.remove();
            }

            const saverequest = document.getElementById('saverequest');
            saverequest.style.display = 'block';





                
        },


        // adding product for the sales user part
        async _onClickaddsalesprobutton() {


            const price_value = document.getElementById('price_value');
            var price_val = price_value.textContent

            const pro_name_value = document.getElementById('pro_name_value');
            var pro_name_val = pro_name_value.textContent

            const qty_value = document.getElementById('quantity');
            var qty_val = qty_value.value

            const dis_value = document.getElementById('discount');
            var dis_val = dis_value.value

            const pricevals = document.getElementById('pricevals');
            var price_vals = pricevals.value

            const counter_value = document.getElementById('counter');
            counter_value.value = parseInt(counter_value.value) + 1
            var counter_val = counter_value.value

            const product_value = document.getElementById('product_id');
            var product_val = product_value.value

            var subtotal = parseFloat(price_vals) * parseFloat(qty_val)
            var disvalue = subtotal * (parseFloat(dis_val) / 100)
            var total = subtotal - disvalue


            const subtotalval = document.getElementById('subtotal');
            subtotalval.innerHTML = subtotal

            const distotal = document.getElementById('distotal');
            distotal.innerHTML = disvalue.toFixed(2)

            const totalval = document.getElementById('total');
            totalval.innerHTML = total.toFixed(2)

            

            const product_image_id = document.getElementById('product_image_id');
            var product_img_id = product_image_id.value

            

            // Create the main container div
            const mainContainerDiv = document.createElement('div');
            mainContainerDiv.setAttribute('class', 'entinral');
            mainContainerDiv.setAttribute('id', "product_div["+counter_val+"]");

            // Create the card div
            const cardDiv = document.createElement('div');
            cardDiv.setAttribute('class', 'card border-0 p-4 gap-2 align-items-center');

            // Create the product card row
            const productCardRow = document.createElement('div');
            productCardRow.setAttribute('class', 'product-card');

            // Create the product image column
            const productImageCol = document.createElement('div');
            // productImageCol.setAttribute('class', 'col-md-6 col-sm-12');
            productImageCol.setAttribute('style', 'text-align:center;');

            // Create the product image element
            const productImage = document.createElement('img');
            productImage.setAttribute('src', "data:image;base64," + product_img_id + "");
            productImage.setAttribute('alt', 'product image');
            productImage.setAttribute('width', '96');
            productImage.setAttribute('height', '96');
            productImage.setAttribute('style', "object-fit: contain;border-radius:10px;");
            


            // Append the product image inside the product image column
            productImageCol.appendChild(productImage);

            // Create the product details column
            const productDetailsCol = document.createElement('div');
            productDetailsCol.setAttribute('class', 'mt-3 text-left');

            // Create the product name row
            const productNameRow = document.createElement('div');
            productNameRow.setAttribute('class', 'row');
            const productNameSpan = document.createElement('span');
            productNameSpan.textContent = pro_name_val;
            productNameRow.appendChild(productNameSpan);

            // Create the product price row
            const productPriceRow = document.createElement('div');
            productPriceRow.setAttribute('class', 'row');
            const productPriceSpan = document.createElement('span');
            productPriceSpan.textContent = price_vals;
            productPriceRow.appendChild(productPriceSpan);

            const pricevalInput = document.createElement('input');
            pricevalInput.setAttribute('type', 'text');
            pricevalInput.setAttribute('id', "priceval["+counter_val+"]");
            pricevalInput.setAttribute('name', "priceval["+counter_val+"]");
            pricevalInput.setAttribute('value', price_vals);
            pricevalInput.style.width = '25px';
            pricevalInput.style.display = 'none';

            // Append the quantity input to the quantity input column
            productPriceRow.appendChild(pricevalInput);

            // Create the product quantity row
            const productQuantityRow = document.createElement('div');
            // productQuantityRow.setAttribute('class', 'row test');
            const productQuantityLabel = document.createElement('span');
            productQuantityLabel.textContent = 'Quantity : ';
            const productQuantityInput = document.createElement('input');
            productQuantityInput.setAttribute('class', 'final_quantity');
            productQuantityInput.setAttribute('type', 'text');
            productQuantityInput.setAttribute('id', "final_quantity["+counter_val+"]");
            productQuantityInput.setAttribute('name', "final_quantity["+counter_val+"]");
            // productQuantityInput.setAttribute('readonly', 'readonly');
            productQuantityInput.setAttribute('style', 'width:45px;');
            productQuantityInput.setAttribute('value', qty_val);
            const increaseQuantityIcon = document.createElement('ion-icon');
            increaseQuantityIcon.setAttribute('class', 'tut');
            increaseQuantityIcon.setAttribute('id', 'increasevalQuantity');
            increaseQuantityIcon.setAttribute('rowval', counter_val);
            increaseQuantityIcon.setAttribute('name', 'add-outline');
            
            // ppppppppppppppppppppppppppppppppppppppppppppppppp
            // addproButton.style.color = "#FFF";
            // addproButton.style.textAlign = "center";
            // addproButton.style.width = "76px";
            // addproButton.style.height = "56px";
            // addproButton.style.backgroundColor = "#1FC069";
            // addproButton.style.padding = "10px";
            // addproButton.style.borderRadius = "8px";
            // addproButton.style.marginTop = "60px";
            // pppppppppppppppppppppppppppppppppppppppppppppppp
            const decreaseQuantityIcon = document.createElement('ion-icon');
            decreaseQuantityIcon.setAttribute('class', 'tut');
            decreaseQuantityIcon.setAttribute('id', 'decreasevalQuantity');
            decreaseQuantityIcon.setAttribute('rowval', counter_val);
            decreaseQuantityIcon.setAttribute('name', 'remove');

            // Create the product discount row
            const productdiscountRow = document.createElement('div');
            // productdiscountRow.setAttribute('class', 'row test');
            const productdiscountLabel = document.createElement('span');
            productdiscountLabel.textContent = 'Discount : ';
            const productdiscountInput = document.createElement('input');
            productdiscountInput.setAttribute('class', 'final_discount');
            productdiscountInput.setAttribute('type', 'text');
            productdiscountInput.setAttribute('id', "final_discount["+counter_val+"]");
            productdiscountInput.setAttribute('name', "final_discount["+counter_val+"]");
            productdiscountInput.setAttribute('readonly', 'readonly');
            productdiscountInput.setAttribute('style', 'width:45px;');
            productdiscountInput.setAttribute('value', dis_val);
            const increasediscountIcon = document.createElement('ion-icon');
            increasediscountIcon.setAttribute('class', 'tut');
            increasediscountIcon.setAttribute('id', 'increase_discount');
            increasediscountIcon.setAttribute('rowval', counter_val);
            increasediscountIcon.setAttribute('name', 'add-outline');
            const decreasediscountIcon = document.createElement('ion-icon');
            decreasediscountIcon.setAttribute('class', 'tut');
            decreasediscountIcon.setAttribute('id', 'decrease_discount');
            decreasediscountIcon.setAttribute('rowval', counter_val);
            decreasediscountIcon.setAttribute('name', 'remove');

            // Append the elements to the respective rows
            productQuantityRow.appendChild(productQuantityLabel);            
            productQuantityRow.appendChild(decreaseQuantityIcon);
            productQuantityRow.appendChild(productQuantityInput);
            productQuantityRow.appendChild(increaseQuantityIcon);

            productdiscountRow.appendChild(productdiscountLabel);            
            productdiscountRow.appendChild(decreasediscountIcon);
            productdiscountRow.appendChild(productdiscountInput);
            productdiscountRow.appendChild(increasediscountIcon);

            // Append the rows to the product details column
            productDetailsCol.appendChild(productNameRow);
            productDetailsCol.appendChild(productPriceRow);
            productDetailsCol.appendChild(productQuantityRow);
            productDetailsCol.appendChild(productdiscountRow);

            // Append the product image column and product details column to the product card row
            productCardRow.appendChild(productImageCol);
            productCardRow.appendChild(productDetailsCol);


            const productIdInput = document.createElement('input');
            productIdInput.setAttribute('type', 'text');
            productIdInput.setAttribute('id', "product_id["+counter_val+"]");
            productIdInput.setAttribute('name', "product_id["+counter_val+"]");
            productIdInput.setAttribute('value', product_val);
            productIdInput.style.display = 'none';
            productCardRow.appendChild(productIdInput);

            const centercontainerRow = document.createElement('div');
            centercontainerRow.setAttribute('class', 'center-container');
            const deleteButton = document.createElement('button');
            deleteButton.setAttribute('class', 'delete_button btn btn-outline-danger');
            deleteButton.setAttribute('style', ' position: relative;top: -10px;left: -21px;');


    
            deleteButton.setAttribute('rowval', counter_val);
            deleteButton.setAttribute('id', "del_product_div["+counter_val+"]");
            deleteButton.innerHTML = '<ion-icon class="tut md hydrated" name="trash-outline" role="img"></ion-icon>';

            // Append the delete button to the product details column
            centercontainerRow.appendChild(deleteButton);
            productCardRow.appendChild(centercontainerRow);






            // Append the product card row to the card div
            cardDiv.appendChild(productCardRow);

            // Append the card div to the main container div
            mainContainerDiv.appendChild(cardDiv);

            // Append the main container div to the body (or any other parent element you want)
            const cardContainer = document.getElementById('extirnal');
            cardContainer.appendChild(mainContainerDiv);
            // document.body.appendChild(mainContainerDiv);

            const temp_product_div = document.getElementById('temp_product_div');
            if (temp_product_div) {
                temp_product_div.remove();
            }

            const saverequest = document.getElementById('saverequest');
            saverequest.style.display = 'block';





                
        },

        
        async _onClickdeletebutton(event){
            var button = event.target;
            var rowval = $(button).attr("rowval");
            
            var rowvalue = parseInt(rowval);

            const temp_product_div = document.getElementById("product_div["+rowvalue+"]");
            if (temp_product_div) {
                temp_product_div.remove();
            }

            const cardContainer = document.getElementById("extirnal");
            if (cardContainer.children.length === 0) {
                const saverequest = document.getElementById("saverequest");
                saverequest.style.display = 'none';
                const detailsbtn = document.getElementById("detailsbtn");
                detailsbtn.style.display = 'none';
                const branchdiv = document.getElementById("branchdiv");
                branchdiv.style.display = 'none';
                const detailsdiv = document.getElementById("detailsdiv");
                detailsdiv.style.display = 'none';
            }
            
        },

        

        async _onClicksaverequest(){
            const details_form = document.getElementById("detailsdiv");
            details_form.style.display = 'block';
            const detailsbtn = document.getElementById("detailsbtn");
            detailsbtn.style.display = 'block';
            const branchdiv = document.getElementById("branchdiv");
            branchdiv.style.display = 'none';
        },

        async _onClickSubmitrequest(){
            var result = {}
            const location = $("input[name='location']").val();
            if (location){
                result['location'] = location 
            }else {
                result['location'] = false;
            }

            const phone = $("input[name='phone']").val();
            
            if (phone){
                result['phone'] = phone
            }else {
                alert('Please add phone number registered with company. and if you are new customer just add you number')
            }

            result['company'] = $("input[name='company']").val();

            // result['currency'] = $("input[name='currency']").val();

            const counter = $("input[name='counter']").val();
            const products_list = []
            for (let i = 1; i <= counter; i++) {
                var pro_result = {}
                const product_id = $("input[name='product_id["+i+"]']").val();
                console.log(product_id)
                if (product_id){
                    const final_quantity = $("input[name='final_quantity["+i+"]']").val();
                    console.log(final_quantity)
                    console.log(product_id)
                    pro_result['product_id'] = product_id
                    pro_result['product_uom_qty'] = final_quantity 
                    products_list.push(pro_result);
                }
            }
            result['products_list'] = products_list 

            ajax.jsonRpc('/check/submit_add_product', 'call', result).then( function(data){
                var alert_msg = data['alert'];

                if (alert_msg == 'show branch'){
                    var branchs = data['branchs'];
                    const branchdiv = document.getElementById("branchdiv");
                    branchdiv.style.display = 'block';


                    // Create the first child div
                    const childDiv1 = document.createElement('div');
                    childDiv1.classList.add('m-1');
                    // childDiv1.style.float = 'left';
                    const branchSpan = document.createElement('span');
                    branchSpan.classList.add('bransh');
                    branchSpan.textContent = 'Branch ';
                    branchSpan.style.fontWeight = 'bold';

                    childDiv1.appendChild(branchSpan);

                    // Create the second child div
                    const childDiv2 = document.createElement('div');
                    childDiv2.classList.add('m-1');

                    // Create radio buttons and labels
                    const locations = branchs;
                    locations.forEach(location => {
                    const label = document.createElement('label');
                    const input = document.createElement('input');
                    input.type = 'radio';
                    input.name = 'location';
                    
                    input.value = location;
                    label.setAttribute('style', "margin-left:85px");

                    const labelText = document.createTextNode(location.charAt(0).toUpperCase() + location.slice(1));
                    label.appendChild(input);
                    label.appendChild(labelText);

                    childDiv2.appendChild(label);
                    childDiv2.appendChild(document.createElement('br'));
                    });

                    // Append child divs to the main container
                    branchdiv.appendChild(childDiv1);
                    branchdiv.appendChild(childDiv2);



                }
                else{
                    var url = data['url'];
                    window.location.href = url;
                }
            });

            
        },

        async _onClickSubmituserrequest(){
            var result = {}
            const location = $("input[name='location']").val();
            if (location){
                result['location'] = location 
            }else {
                result['location'] = false;
            }

            const phone = $("input[name='phone']").val();
            
            if (phone){
                result['phone'] = phone
            }else {
                alert('Please add phone number registered with company. and if you are new customer just add you number')
            }

            result['company'] = $("input[name='company']").val();

            // result['currency'] = $("input[name='currency']").val();

            const counter = $("input[name='counter']").val();
            const products_list = []
            for (let i = 1; i <= counter; i++) {
                var pro_result = {}
                const product_id = $("input[name='product_id["+i+"]']").val();
                console.log(product_id)
                if (product_id){
                    const final_quantity = $("input[name='final_quantity["+i+"]']").val();
                    const final_discount = $("input[name='final_discount["+i+"]']").val();
                    console.log(final_quantity)
                    console.log(product_id)
                    pro_result['product_id'] = product_id
                    pro_result['product_uom_qty'] = final_quantity 
                    pro_result['discount'] = final_discount 
                    products_list.push(pro_result);
                }
            }
            result['products_list'] = products_list 

            ajax.jsonRpc('/check/submit_sale_add_product', 'call', result).then( function(data){
                var alert_msg = data['alert'];

                if (alert_msg == 'show branch'){
                    var branchs = data['branchs'];
                    const branchdiv = document.getElementById("branchdiv");
                    branchdiv.style.display = 'block';


                    // Create the first child div
                    const childDiv1 = document.createElement('div');
                    childDiv1.classList.add('m-1');
                    // childDiv1.style.float = 'left';
                    const branchSpan = document.createElement('span');
                    branchSpan.classList.add('bransh');
                    branchSpan.textContent = 'Branch ';
                    childDiv1.appendChild(branchSpan);

                    // Create the second child div
                    const childDiv2 = document.createElement('div');
                    childDiv2.classList.add('m-1');

                    // Create radio buttons and labels
                    const locations = branchs;
                    locations.forEach(location => {
                    const label = document.createElement('label');
                    const input = document.createElement('input');
                    input.type = 'radio';
                    input.name = 'location';
                    
                    input.value = location;
                    label.setAttribute('style', "margin-left:85px");

                    const labelText = document.createTextNode(location.charAt(0).toUpperCase() + location.slice(1));
                    label.appendChild(input);
                    label.appendChild(labelText);

                    childDiv2.appendChild(label);
                    childDiv2.appendChild(document.createElement('br'));
                    });

                    // Append child divs to the main container
                    branchdiv.appendChild(childDiv1);
                    branchdiv.appendChild(childDiv2);



                }
                else{
                    var url = data['url'];
                    window.location.href = url;
                }
            });

            
        },


        async _onClickAfterChechOutButton() {
            $("div.checkin").show();
            $("div.checkout").hide();
            $("div.after_checkout").hide();
            $("div.after_checkin").hide();
        },
       
    });
});
