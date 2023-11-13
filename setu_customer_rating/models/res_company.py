# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    banner_message = fields.Char(default='Click on Evaluate Now to execute process for customer rating.')
    customer_rating_calculated = fields.Boolean(default=True)
