# -*- coding: utf-8 -*-

import math

from odoo import fields, models, api

priority = [('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5')]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_score = fields.Integer(string="Score", company_dependent=True)
    customer_rating_avg = fields.Selection(selection=priority, string="Rating Average", compute='_compute_rating_stats')

    customer_rating_id = fields.Many2one('setu.customer.rating', string="Customer Rating", company_dependent=True)
    customer_score_id = fields.Many2one('setu.customer.score', string="Customer Score", company_dependent=True)

    def _compute_rating_stats(self):
        for p in self:
            p_score = p.customer_score_id.total_score or 0
            p.customer_rating_avg = str(math.ceil(p_score * 5 / 100))

    def view_to_customer_score(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window',
                'res_model': 'setu.customer.score',
                'view_mode': 'form',
                'res_id': self.customer_score_id.id,
                'target': 'current'}

    def open_partner_rating_history(self):
        action = self.env.ref('prosys_customer_rating.setu_partner_rating_history_action').read()[0]
        action.update({'domain': [('partner_id', '=', self.id)]})
        return action
