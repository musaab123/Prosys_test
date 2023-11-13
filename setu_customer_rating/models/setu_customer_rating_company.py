# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SetuCustomerRatingCompany(models.Model):
    _name = 'setu.customer.rating.company'
    _description = 'Customer Rating Company'
    _rec_name = 'company_id'

    company_id = fields.Many2one(comodel_name='res.company', string='Company', required=False)
    rating_ids = fields.One2many(comodel_name='setu.customer.rating', inverse_name='crc_id', string='Rating',
                                 required=False)
