# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Picking Order Line Views",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "category": "Warehouse",
    "summary": """
Show Incoming Order Lines, Display Outgoing Order Lines Module,
Add Filter In Internal Transfer, Group By IO,
Show Outgoing Order Lines App, Display  Delivery Order Lines,
Show Shipment Line Views Odoo
""",
    "description": """
This module useful to show incoming/outgoing order lines products
using the filter & group by option. You can easily
add custom filters/groups of incoming order/outgoing order lines.
Easy to work with incoming/outgoing order lines directly using the list view,
form view, kanban view, search view, pivot view, graph view, calendar view.
Picking Order Line Views Odoo
Show Incoming Order Lines, Display Outgoing Order Lines Module,
Add Filter In Internal Transfer, Group By IO, Show Outgoing Order Lines,
Display  Delivery Order Lines, Show Shipment Line Views Odoo
Show Incoming Order Lines, Display Outgoing Order Lines Module,
Add Filter In Internal Transfer, Group By IO, Show Outgoing Order Lines App,
Display  Delivery Order Lines, Show Shipment Line Views Odoo
""",
    "version": "16.0.1",
    "depends": ["stock","project","evo_portal_task"],
    "application": True,
    "data": [
            'security/ir.model.access.csv',
            "views/stock_views.xml",
            "views/add_project_task.xml",
            "views/change_active_state.xml",
            "views/picking_task_line.xml",
            "views/update_active_state.xml",
            'i18n/custom_project_task_description.xml',


            



            

            ],

    # 'assets': {
    #     'web.assets_backend': [
    #         '/sh_picking_order_line/static/src/**/*',
    #         '/sh_picking_order_line/static/src/xml/**/*',
    #     ],
    #     'web.assets_frontend': [
    #         '/sh_picking_order_line/static/src/js/custom_actions.js',
    #     ],
    # },

    "images": ["static/description/background.png"],
    "live_test_url": "https://youtu.be/rjRJwKiBzZ4",
    "auto_install": False,
    "installable": True,
    "price": 18,
    "currency": "EUR"
}
