
{
    "name": "Design reports for Entool company",
    "version": "1.1",
    "category": "Generic Modules/sale",
    "description": """ Manage Reports for the management of purchases, 
            sales, accounting, stores, and extracting the stock 
            bond upon receipt and shipment

    """,
    "author": "Prosys",
    "website": "",
    "depends":['base','sale','account','sales_team','point_of_sale','l10n_gcc_invoice','stock','posys_partner_extra_info','partner_location'],
    "data": [

        'data/salepersone_view.xml',
        'reports/report.xml',
        'reports/swag_sale_order_template.xml',
        'reports/swag_invoice_custom_template.xml',
        'reports/sale_delivery_slip_custom.xml',
        'reports/slip_header.xml',


        
        'views/res_company_view.xml',
        'views/sales_view.xml',

      



       
    
    ],
    "installable": True,
    "active": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

