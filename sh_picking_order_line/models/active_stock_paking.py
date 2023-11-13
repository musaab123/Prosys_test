from odoo import fields, models, api, _

class AccountPicking(models.Model):
    _inherit = 'stock.picking'

    is_active_picking = fields.Boolean(string="Active", store=True ,default=False)


    

    def action_update_picking_is_active(self):
        list_ids = []
        for rec in self:
            list_ids.append(rec.id)

        return {
            'name': _("Set Active"),
            'type': 'ir.actions.act_window',
            'res_model': 'picking.active.wizard',
            'view_mode': 'form,tree',
            'view_type': 'form',
            'context': {'default_is_active_picking': list_ids},
            'target': 'new',
        }
    
    


class PickingActivateWizard(models.TransientModel):
    _name = 'picking.active.wizard'

    is_active_picking = fields.Boolean(default=False, tracking=True ,string="Active") 

    @api.model
    def default_get(self, fields):
        defaults = super(PickingActivateWizard, self).default_get(fields)
        defaults['is_active_picking'] = False
        return defaults

    def set_activate_picking(self):
        list_ids = self.env.context.get('default_is_active_picking')
        invoice_id = self.env['stock.picking']
        if self.env.context.get('default_is_active_picking'):
            invoice_id = self.env['stock.picking'].search([('id', 'in', list_ids)])

        for rec in invoice_id:
            rec.write(
                {
                    'is_active_picking': self.is_active_picking,
                }
            )



