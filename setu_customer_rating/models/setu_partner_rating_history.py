# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SetuPartnerRatingHistory(models.Model):
    _name = 'setu.partner.rating.history'
    _description = 'Partner Rating History'

    date_changed = fields.Datetime(string='Date Change', required=False)

    previous_customer_rating_id = fields.Many2one(comodel_name='setu.customer.rating',
                                                  string='Previous Customer Rating', required=False)
    current_customer_rating_id = fields.Many2one(comodel_name='setu.customer.rating', string='Current Customer Rating',
                                                 required=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=False)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', required=False)
