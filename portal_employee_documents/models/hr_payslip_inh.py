# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_employee_doc = fields.Boolean('Employee Document (Portal)')


