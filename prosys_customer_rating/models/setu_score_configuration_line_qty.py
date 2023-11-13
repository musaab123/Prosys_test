# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SetuScoreConfigurationLineQTY(models.Model):
    _name = 'setu.score.configuration.line.qty'
    _description = 'Score Configuration Line QTY'

    from_quantity = fields.Float(string="From Quantity")
    to_quantity = fields.Float(string="To Quantity")
    pre_score = fields.Integer(string="Pre Score")

    score_conf_id = fields.Many2one('setu.score.configuration', ondelete='cascade', copy=False)
    calculation_based_on = fields.Selection(related='score_conf_id.calculation_based_on', string="Calculation Based On")
