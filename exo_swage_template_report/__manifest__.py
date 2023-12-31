
{
    "name": "Design reports for Exo",
    "version": "1.1",
    "category": "Generic Modules/sale",
    "description": """ Manage Reports for the management of purchases, 
            sales, accounting, stores, and extracting the stock 
            bond upon receipt and shipment

    """,
    "author": "Prosys",
    "website": "",
    "depends":['base','sale','purchase','account','prosys_po_so_data','product_brand_inventory','sale_discount_total','ent_hr_employee_updation'],
    "data": [

        'data/salepersone_view.xml',
        'reports/report.xml',
        'reports/swag_sale_order_template.xml',
        'reports/swag_purchase_order_template.xml',
        'reports/swag_invoice_custom_template.xml',
        'reports/swage_bill_custom_template.xml',
        'reports/sale_delivery_slip_custom.xml',
        'reports/purchase_delivery_slip_custom.xml',
        'views/res_company_view.xml',
        'views/sales_view.xml',
        'views/accounts_view.xml',
        'views/res_users_view.xml',

      



       
    
    ],
    "installable": True,
    "active": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

