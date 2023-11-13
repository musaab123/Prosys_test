# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SetuScoreConfigurationLinePrice(models.Model):
    _name = 'setu.score.configuration.line.price'
    _description = 'Score Configuration Line Price'

    from_price = fields.Float(string="From Price", required=True)
    to_price = fields.Float(string="To Price", required=True)
    pre_score = fields.Integer(string="Pre Score", required=True)

    score_conf_id = fields.Many2one('setu.score.configuration', string="Score Configuration", ondelete='cascade',
                                    copy=False)
    calculation_based_on = fields.Selection(related='score_conf_id.calculation_based_on', string="Calculation Based On")
