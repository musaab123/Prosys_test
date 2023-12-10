
{
    "name": "Design reports for sales, purchases and accounts",
    "version": "1.1",
    "category": "Generic Modules/sale",
    "description": """ Manage Reports for the management of purchases, 
            sales, accounting, stores, and extracting the stock 
            bond upon receipt and shipment

    """,
    "author": "Prosys",
    "website": "",
    "depends":['sale' ,'sale_management','account','stock','purchase','partner_po_so_info_16','stock_Packagings_info'],
    "data": [

        # 'security/ir.model.access.csv',
        'security/group_company_employee.xml',

        'reports/sale_header_custom.xml',
        'reports/sale_order_ksa_company.xml',
        'reports/sale_invoice_china_company.xml',
        'reports/purchase_order_china_company.xml',
        'reports/Invoice_services_to_supplier_customer_china_company.xml',
        'reports/delevry_slip_custom.xml',
        'reports/utility_invoice_sale_china_company.xml',
        'reports/report.xml',
        'reports/purchase_invoice_china_company.xml',
        'reports/stock_delivery_slip_china_company.xml',
        'reports/stock_delivery_slip_vindor_china_company.xml',
        'reports/stock_delivery_slip_customer_china_company.xml',
        'reports/utility_invoice_purchase_china_company.xml',
        'reports/invoice_service_to_supplier_vindor_china_company.xml',
        'reports/ksa_utility_vindor_company.xml',
        'reports/ksa_invoice_to_supplier_vindor.xml',

        'reports/sale_order_china_company.xml',
        'reports/ksa_header_footer_custom.xml',
        'reports/ksa_invoice_sale_custom.xml',
        'reports/ksa_purchase_order_template.xml',
        'reports/ksa_invoice_purchase_custom.xml',
        'reports/ksa_invoice_service_to_supplier.xml',
        'reports/ksa_invoice_utility.xml',
        'reports/ksa_delevry_slip_purchase.xml',
        'reports/ksa_delevery_slip_sale.xml',
        'views/res_company_view.xml',
        # 'views/stock_test.xml',


        
        

    
    ],
    "installable": True,
    "active": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

