# -*- coding: utf-8 -*-

{
    'name': "Loan Portal",
    'version': '16.0.1.2',
    'summary': """
        Apply loans from portal.Easily access to loans and apply loans from portal.User can easily  from portal.""",
    'description': """
        =>Apply loans from portal.Easily access to expense and apply expense from portal.
        =>User can easily create expense from portals.
        =>Showninf old loans lines data.
    """,
    'category': 'Human Resources/Attendance',
    'author': 'Prosys',
    'company': 'PROSYS',
    'depends': ['hr_expense', 'portal', 'portal_hr_knk','sh_hr_attendance_geolocation','dev_hr_loan'],
    'data': [
        'views/portal_expense_templates.xml',
        
        
    ],
    'assets': {
        'web.assets_backend': [
            '/dev_hr_loan/static/src/**/*',
            '/dev_hr_loan/static/src/xml/**/*',
        ],
        'web.assets_frontend': [
            '/portal_loan/static/src/js/attendance_portal.js',
            '/portal_loan/static/src/js/checkin_out.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
