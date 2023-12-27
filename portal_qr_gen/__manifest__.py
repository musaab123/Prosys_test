# -*- coding: utf-8 -*-

{
    'name': "Portal QR Generator and Screen",
    'version': '16.0.1.1',
    'summary': """
        Portal QR Generator and Screen view for the QR.""",
    'description': """
        Portal QR Generator and Screen view for the QR.
    """,
    'category': 'Portal',
    'author': 'ZIAD MONIM',
    'company': 'PROSYS',
    'depends': ['base','portal'],
    'data': [
        'data/qr_check.xml',
        'views/qr_generator.xml',
        'views/qr_portal_screen.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            # '/hr_attendance/static/src/**/*',
            # '/hr_attendance/static/src/xml/**/*',
        ],
        'web.assets_frontend': [
            '/portal_qr_gen/static/src/css/style.css',
            # '/portal_attendance/static/src/js/checkin_out.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
