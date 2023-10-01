# Copyright © 2018 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Purchase Product Labels',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/en/shop/category/odoo-product-labels-15',
    'license': 'LGPL-3',
    'summary': 'Print custom product barcode labels for purchase orders | Barcode product label printing from purchase order',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/s4a',
    'depends': [
        'garazd_product_label',
        'purchase',
    ],
    'data': [
        'wizard/print_product_label_views.xml',
    ],
    'price': 19.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
