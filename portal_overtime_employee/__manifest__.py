# -*- coding: utf-8 -*-

{
    'name': "Employee Overtime Portal",
    'version': '16.0.1.2',
    'summary': """
        Apply Employee Overtime from portal.Easily access to Employee Overtime and apply Employee Overtime from portal.User can easily  from portal.""",
    'description': """
        =>Apply Employee Overtime from portal.Easily access to expense and apply expense from portal.
        =>User can easily create expense from portals.
        =>Showninf old Employee Overtime lines data.
    """,
    'category': 'Human Resources/Employee Overtime',
    'author': 'Prosys',
    'company': 'PROSYS',
    'depends': ['hr', 'portal', 'portal_hr_knk','hr_payroll'],
    'data': [
        'views/portal_employee_overtime_templates.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            '/hr_payroll/static/src/**/*',
            '/hr_payroll/static/src/xml/**/*',
        ],
        'web.assets_frontend': [
            '/portal_overtime_employee/static/src/js/overtime_request.js',
            '/portal_overtime_employee/static/src/js/employee_overtime.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
