{
    # App information
    'name': 'Prosys Customer Ratings',
    'category': 'sale',
    'license': 'OPL-1',
    'version': '16.0',
    'sequence': 1,

    # Additional Information
    'description': """Customer rating is an application which helps businesses to give a score to every customer of business 
        based on their behavior of Purchase and payment regularity. Based on Customer score you can 
        segment customers to group which further helps to apply Marketing Strategy.
        Various parameters like average monthly sales, average monthly sales return, due of amount of invoices,
        quantity of due invoices, amount of invoices paid after due dates are considered which says that 
        customer ratings given is highly accurate to identify their behavior of purchase.""",

    'summary': """Customer rating is an application which helps businesses to give a score to every customer of business 
        based on their behavior of Purchase and payment regularity, customer score, ratings, sales score, pos customer rating, invoice, payment, pos order, sales return, sales history,  dashboard, """,

    # Author
    'website': 'https://www.prosys-sa.com',
    'support': 'https://www.prosys-sa.com',
    'author': 'ProSys Technology .',

    # Dependencies
    'depends': ['sale_management', 'stock'],

    # Views
    'data': [
        # Security
        'security/setu_customer_rating_security.xml',
        'security/ir.model.access.csv',

        # DB Functions
        'db_function/get_currency_rate.sql',
        'db_function/create_customer_score_records.sql',
        'db_function/set_customer_scores_no_pos.sql',
        'db_function/set_document_ids_no_pos.sql',
        'db_function/update_rating_data.sql',

        # Data
        'data/setu_score_configuration_data.xml',
        'data/setu_score_configuration_line_price_data.xml',
        'data/setu_score_configuration_line_percentage_data.xml',
        'data/setu_score_configuration_line_qty.xml',
        'data/ir_cron_get_setu_customer_score.xml',

        # Views
        'views/setu_score_configuration_views.xml',
        'views/setu_customer_rating_company_views.xml',
        'views/setu_customer_rating_views.xml',
        'views/setu_customer_score_views.xml',
        'views/res_partner_extended_views.xml',
        'views/setu_customer_rating_dashboard_views.xml',
        'views/setu_partner_rating_history_views.xml',

        # Wizards
        'wizard_views/res_config_settings_views.xml',
        'wizard_views/setu_score_configuration_creator_views.xml',

        # Reports
        'reports/setu_history_management_report.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'setu_customer_rating/static/src/js/get_rule.js',
            'setu_customer_rating/static/src/js/rating_dashboard.js'
        ],
        'web.assets_qweb': ['setu_customer_rating/static/src/xml/*']
    },

    'qweb': ['static/src/xml/main_dashboard.xml',
             'static/src/xml/get_rule.xml'
             ],
    'demo': [],
    'images': ['static/description/banner.gif'],
    'post_init_hook': 'create_rating_table',

    # Technical
    'price': 129,
    # 'price' : 103,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    # 'live_test_url': 'http://95.111.225.133:5929/web/login',
}
