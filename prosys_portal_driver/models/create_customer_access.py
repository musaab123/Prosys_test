# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    driver_sale_order_ids =fields.One2many('sale.order','driver_id')
    sale_order_count = fields.Integer(string="count" , compute="count_sale_orders")
    is_driver = fields.Boolean(string="Is Driver")

    def count_sale_orders(self):
        for rec in self:
            rec.sale_order_count = sum(rec.driver_sale_order_ids.ids)
