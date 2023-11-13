# -*- coding: utf-8 -*-
{
    'name': "Portal User Project Management Access",
    'summary': """portal user, project management access, project, access""",
    'description': """portal user project management access
                    """,
    'author': "Evozard",
    'website': "http://evozard.com/",    
    'category': 'Other',
    'version': '16.0.0.1',
    'sequence': 15,
    'depends': ['project','hr','hr_timesheet', 'portal', 'website','crm','documents'],
    'license': "AGPL-3",
    'price': 49.99,
    'currency': 'USD',
    'data': [
        'view/project_portal_tempalte.xml',
        'view/task_view.xml',
        'view/project_task_view.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application':True,
}
