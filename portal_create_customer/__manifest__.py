# -*- coding: utf-8 -*-

{
    'name': "  Portal Create Customer",
    'version': '16.0.1.2',
    'summary': """
        Apply Create Customer from portal.Easily access to Create Customer and apply Create Customer from portal.User can easily  from portal.""",
    'description': """
        =>Apply Create Customer from portal.Easily access to expense and apply expense from portal.
        =>User can easily download Create Customer from portals.
        =>Showninf old Create Customer lines data.
    """,
    'category': 'Human Resources/Attendance',
    'author': 'Prosys',
    'company': 'PROSYS',
    'depends': ['base', 'portal', 'portal_hr_knk','posys_partner_extra_info','partner_location'],
    'data': [

        'views/create_customer_view.xml',
        'views/portal_create_customer_templates.xml',

        
    ],
    'assets': {
        'web.assets_backend': [
            '/portal_create_customer/static/src/**/*',
            '/portal_create_customer/static/src/xml/**/*',
            
        ],
        'web.assets_frontend': [
            '/portal_create_customer/static/src/js/attendance_portal.js',
            '/portal_create_customer/static/src/js/checkin_out.js',
            '/portal_create_customer/static/src/js/custom_inherit.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
