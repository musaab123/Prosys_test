
{
    "name": "Entool Design reports",
    "version": "1.1",
    "category": "Generic Modules/sale",
    "description": """ Manage Reports for the management of purchases, 
            sales, accounting, stores, and extracting the stock 
            bond upon receipt and shipment

    """,
    "author": "Prosys",
    "website": "",
    "depends":['base','sale','account','sales_team','point_of_sale','l10n_gcc_invoice','stock'],
    "data": [

        # 'reports/report.xml',
        'reports/swag_sale_order_template.xml',
        'reports/pos_invoice_template_custom.xml',
        'reports/custom_header_footer.xml',


        
        # 'views/account_move_views.xml',

        'views/sale_team_bransh.xml',
        'views/res_company_view.xml',



    
    ],
    "installable": True,
    "active": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

