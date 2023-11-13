# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_score_days = fields.Integer(string='Customer Score Based On Past X Days',
                                         config_parameter='prosys_customer_rating.customer_score_days')
    past_days_for_invoice = fields.Integer(string='Unpaid Invoices Of Past X Days',
                                           config_parameter='prosys_customer_rating.past_days_for_invoice')
