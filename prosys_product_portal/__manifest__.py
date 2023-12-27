# -*- coding: utf-8 -*-

{
    'name': " Prosys Portal Add Procust",
    'version': '16.0.1.2',
    'summary': """
        Apply Portal Add Procust from portal.Easily access to Portal Add Procust and apply Portal Add Procust from portal.User can easily  from portal.""",
    'description': """
        =>Apply Portal Add Procust from portal.Easily access to expense and apply expense from portal.
        =>User can easily download Portal Add Procust from portals.
        =>Showninf old Portal Add Procust lines data.
    """,
    'category': 'point of sale/product',
    'author': 'Prosys',
    'company': 'PROSYS',
    'depends': ['sale','sale_stock','point_of_sale','product', 'portal'],
    'data': [
        'views/hr_emp.xml',
        'views/portal_product_templates.xml',
        'views/portal_product_templates_salesmen.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            '/prosys_product_portal/static/src/js/html5-qrcode.min.js',
            '/prosys_product_portal/static/src/js/quagga.min.js',
            '/prosys_product_portal/static/src/js/sales_portal.js',
            '/prosys_product_portal/static/src/js/product_add_tocard.js',
            '/prosys_product_portal/static/src/js/add_product.js',
            '/prosys_product_portal/static/src/js/scanner.js',

        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
