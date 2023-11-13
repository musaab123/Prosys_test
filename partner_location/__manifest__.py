{
    'name': 'Partner Geolocation And Sale Lines',
    'version': '16.0.1.0.0',
    'category': 'Contacts',
    'description': 'Partner Geolocation.',
    'summary': 'Partner Geolocation.',
    'author': 'Prosys Tech',
    'company': 'Prosys Tech',
    'maintainer': 'Prosys Tech ',
    'depends': ['base','base_geolocalize', 'account','crm_enterprise','crm','web_map','industry_fsm','project'],
    'data': [
        
        'security/ir.model.access.csv',
        'views/customer_location_view.xml',
        'views/project_task_inherit.xml',
        'views/google_map_view.xml',
        'views/sale_lines_view.xml',
        'views/edit_project_task.xml',
        'views/update_sale_lines.xml',
        'views/field_services_view.xml',


        
    ],
    'assets': {
        'web.assets_backend': [
            'partner_location/static/src/js/custom_inherit.js',
            'partner_location/static/src/js/user_location_custom.js',

        ],
    },
    'images': ['static/description/location.png'],

    'installable': True,
    'application': False,
}

