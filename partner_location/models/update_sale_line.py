from odoo import fields, models, api, _
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_update_sale_lines(self):
        list_ids = []
        for rec in self:
            list_ids.append(rec.id)

        return {
            'name': _("Set Sale Line"),
            'type': 'ir.actions.act_window',
            'res_model': 'change.sale.wizard',
            'view_mode': 'form,tree',
            'view_type': 'form',
            'context': {'default_sale_lines': list_ids},
            'target': 'new',
        }


class ChangeSaleLineWizard(models.TransientModel):
    _name = 'change.sale.wizard'

    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')


    def set_sale_line(self):

        list_ids = self.env.context.get('default_sale_lines')
        invoice_id = self.env['res.partner']
        if self.env.context.get('default_sale_lines'):
            invoice_id = self.env['res.partner'].search([('id', 'in', list_ids)])

        for rec in invoice_id:
            rec.write(
                {
                    'sale_lines_id': self.sale_lines_id.id,
                }
            )