# -*- coding: utf-8 -*-

{
    'name': "Colloctor Payment Portal",
    'version': '16.0.1.2',
    'summary': """
        Apply Colloctor Payment from portal.Easily access to Colloctor Payment and apply Colloctor Payment from portal.User can easily  from portal.""",
    'description': """
        =>Apply Colloctor Payment from portal.Easily access to expense and apply expense from portal.
        =>User can easily create expense from portals.
        =>Showninf old Colloctor Payment lines data.
    """,
    'category': 'Accounting/Colloctor Payment',
    'author': 'Prosys',
    'company': 'PROSYS',
    'depends': ['base','account', 'portal', 'sale','payment','hr', 'website','payment'],
    'data': [
        # 'data/iron.xml',
        'security/ir.model.access.csv',
        'reports/conductors.xml',
        'reports/conductor_header_footer.xml',
        'views/views.xml',
        'views/account_move_view.xml',
        'views/templates.xml',
        'views/portal_account_payment_templates.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            '/collector_payment_portal/static/src/**/*',
            '/collector_payment_portal/static/src/xml/**/*',
        ],
        'web.assets_frontend': [
            '/collector_payment_portal/static/src/js/attendance_portal.js',
            '/collector_payment_portal/static/src/js/checkin_out.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
