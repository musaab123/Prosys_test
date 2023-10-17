from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_update_invoice_collectors(self):
        list_ids = []
        for rec in self:
            list_ids.append(rec.id)

        return {
            'name': _("Set User"),
            'type': 'ir.actions.act_window',
            'res_model': 'change.collector.wizard',
            'view_mode': 'form,tree',
            'view_type': 'form',
            'context': {'default_collector_ids': list_ids},
            'target': 'new',
        }


class ChangeCollectorsWizard(models.TransientModel):
    _name = 'change.collector.wizard'

    user_id = fields.Many2one('res.users', string="User")

    def set_collector(self):

        list_ids = self.env.context.get('default_collector_ids')
        invoice_id = self.env['account.move']
        if self.env.context.get('default_collector_ids'):
            invoice_id = self.env['account.move'].search([('id', 'in', list_ids)])

        for rec in invoice_id:
            rec.write(
                {
                    'collecter_id': self.user_id.id,
                }
            )