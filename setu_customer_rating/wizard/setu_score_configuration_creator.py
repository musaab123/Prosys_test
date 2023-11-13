from odoo import fields, models, api


class SetuScoreConfigurationCreator(models.TransientModel):
    _name = 'setu.score.configuration.creator'
    _description = 'Score Configuration Creator'

    message_success = fields.Boolean(
        string='Is Message Success?',
        required=False)

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False)

    def confirm(self):
        action = self.env.ref('setu_customer_rating.setu_score_configuration_creator_action').read()[0]
        action['view_id'] = (self.env.ref('setu_customer_rating.setu_score_configuration_creator_message_form_view').id,
                             'score_configuration_exists_form_warning')
        action['views'] = [
            (self.env.ref('setu_customer_rating.setu_score_configuration_creator_message_form_view').id, 'form')]
        action['res_id'] = self.id
        if self.env['setu.score.configuration'].search([('company_id', '=', self.company_id.id)]):
            return action
        self.env['setu.score.configuration'].create_rules(self.company_id)
        self.message_success = True
        return action
