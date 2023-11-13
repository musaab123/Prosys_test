from odoo import fields, models, api


class SetuScoreConfigurationLinePercentage(models.Model):
    _name = 'setu.score.configuration.line.percentage'
    _description = 'Score Configuration Line Percentage'

    from_percentage = fields.Float(string="From Percentage")
    to_percentage = fields.Float(string="To Percentage")
    pre_score = fields.Integer(string="Pre Score")

    score_conf_id = fields.Many2one('setu.score.configuration', ondelete='cascade', copy=False)
    calculation_based_on = fields.Selection(related='score_conf_id.calculation_based_on', string="Calculation Based On")
