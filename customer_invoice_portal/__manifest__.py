# -*- coding: utf-8 -*-

{
    'name': "customer invoice custom",
    'version': '16.0.1.2',
    'summary': """
        Apply customer invoice custom from portal.Easily access to customer invoice custom and apply customer invoice custom from portal.User can easily  from portal.""",
    'description': """
        =>Apply customer invoice custom from portal.Easily access to expense and apply expense from portal.
        =>User can easily create expense from portals.
        =>Showninf old customer invoice custom lines data.
    """,
    'category': 'Accounting/Colloctor Payment',
    'author': 'Prosys',
    'company': 'PROSYS',
    'depends': ['base','account', 'website','collector_payment_portal','hr'],
    'data': [
        # 'data/iron.xml',
        'views/portal_account_payment_templates.xml',
        'views/permition_view.xml',

       
        
    ],
    'assets': {
        'web.assets_backend': [
            '/customer_invoice_portal/static/src/**/*',
            '/customer_invoice_portal/static/src/xml/**/*',
        ],
        'web.assets_frontend': [
            '/customer_invoice_portal/static/src/js/attendance_portal.js',
            '/customer_invoice_portal/static/src/js/checkin_out.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
