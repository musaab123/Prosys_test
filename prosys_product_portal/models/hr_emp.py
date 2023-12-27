# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import models,fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_sales_person = fields.Boolean('Sales Request (Portal)')
