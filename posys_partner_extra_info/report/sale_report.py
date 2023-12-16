# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleReport(models.Model):
    _inherit = 'sale.report'

    made_id = fields.Many2one('product.made', string='Made In')

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['made_id'] = "t.made_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            t.made_id"""
        return res
    
class PurchaseBrandPivot(models.Model):
    _inherit = 'purchase.report'

    made_id = fields.Many2one('product.made', string='Made In')

    def _select(self):
        res = super(PurchaseBrandPivot, self)._select()
        query = res.split('t.categ_id as category_id,', 1)
        rese = query[0] + 't.categ_id as category_id,t.made_id as made_id,' + query[1]
        return rese

    def _group_by(self):
        res = super(PurchaseBrandPivot, self)._group_by()
        query = res.split('t.categ_id,', 1)
        res = query[0] + 't.categ_id,t.made_id,' + query[1]
        return res

