# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Nikhil krishnan(odoo@cybrosys.com)
#    you can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Sale & Purchase Approval Workflow',
    'version': '16.0.1.0.1',
    'summary': """Add custom approval button to sale and purchase module.""",
    'description': """Add custom approval button to sale and purchase module""",
    'author': 'Prosys Techno Solutions',
    'company': 'Prosys Techno Solutions',
    'website': 'https://www.prosys.com',
    'category': 'Sale Purchase',
    'depends': ['sale', 'purchase'],
    'license': 'AGPL-3',
    'data': [
        'security/approval_group_view.xml',
        'views/sale_workflow_view.xml',
        'views/purchase_workflow_view.xml',
    ],
 
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
