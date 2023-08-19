
{
    "name": "Design reports for swale",
    "version": "1.1",
    "category": "Generic Modules/sale",
    "description": """ Manage Reports for the management of purchases, 
            sales, accounting, stores, and extracting the stock 
            bond upon receipt and shipment

    """,
    "author": "Prosys",
    "website": "",
    "depends":['sale','purchase','prosys_po_so_data','product_barcode_sequence','product_hs_code_inventory','product_factory_inventory','product_brand_inventory'],
    "data": [

        # 'security/group_company_employee.xml',
        'reports/report.xml',
        'reports/swag_sale_order_template.xml',
        'reports/swag_purchase_order_template.xml',
        'reports/swag_invoice_custom_template.xml'
       
    
    ],
    "installable": True,
    "active": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

