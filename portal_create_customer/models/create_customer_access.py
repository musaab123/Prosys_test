# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    create_customer_access = fields.Boolean('Create Customer (Portal)')


