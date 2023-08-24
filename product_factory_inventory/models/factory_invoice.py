# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Midilaj (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api, tools

class FactoryPivotInvoicing(models.Model):
    _inherit = "account.invoice.report"

    factory_id = fields.Many2one('factory.master', string='Factory')

    # def _select(self):
    #     res = super(FactoryPivotInvoicing, self)._select()
    #     query = res.split('template.categ_id AS product_categ_id,', 1)
    #     res = query[0] + 'template.categ_id as product_categ_id,template.factory_id as factory_id,' + query[1]
    #     return res

    def _group_by(self):
        res = super(FactoryPivotInvoicing, self)._group_by()
        query = res.split('template.categ_id,', 1)
        res = query[0] + 'template.categ_id,template.factory_id,' + query[1]
        return res
