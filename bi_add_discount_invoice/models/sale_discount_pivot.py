# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    discount_amt = fields.Float('Discount Final Amount')


    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['discount_amt'] = "s.discount_amt"
        return res
