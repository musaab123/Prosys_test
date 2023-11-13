# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api, _


class StockMove(models.Model):
    _inherit = "stock.move"

    sh_pol_picking_order_line_picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type", related="picking_id.picking_type_id", ondelete='set null', store=True, string="Picking Type")

    sh_pol_picking_order_line_picking_type_code = fields.Selection(
        related="picking_id.picking_type_id.code", store=True, string="Picking Operation")

    is_active = fields.Boolean(string="Active", store=True ,default=False)

    image = fields.Image(string="", compute='_compute_image')

    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920

    def action_transfer(self):
        if self.picking_id:
            return {"type": "ir.actions.act_window", "name": "Transfer", "view_mode": "form", "res_model": "stock.picking", "res_id": self.picking_id.id}
        return False
    
    def action_update_invoice_is_active(self):
        list_ids = []
        for rec in self:
            list_ids.append(rec.id)

        return {
            'name': _("Set Active"),
            'type': 'ir.actions.act_window',
            'res_model': 'change.active.wizard',
            'view_mode': 'form,tree',
            'view_type': 'form',
            'context': {'default_is_active': list_ids},
            'target': 'new',
        }
    
class ChangeActivateWizard(models.TransientModel):
    _name = 'change.active.wizard'

    is_active = fields.Boolean(default=False, tracking=True ,string="Active") 

    @api.model
    def default_get(self, fields):
        defaults = super(ChangeActivateWizard, self).default_get(fields)
        defaults['is_active'] = False
        return defaults

    def set_activate(self):
        list_ids = self.env.context.get('default_is_active')
        invoice_id = self.env['stock.move']
        if self.env.context.get('default_is_active'):
            invoice_id = self.env['stock.move'].search([('id', 'in', list_ids)])

        for rec in invoice_id:
            rec.write(
                {
                    'is_active': self.is_active,
                }
            )


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sh_pol_picking_order_line_picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type", related="picking_id.picking_type_id", ondelete='set null', store=True, string="Picking Type")

    sh_pol_picking_order_line_picking_type_code = fields.Selection(
        related="picking_id.picking_type_id.code", store=True, string="Picking Operation")
    sh_pol_picking_order_line_origin = fields.Char(
        related="picking_id.origin", store=True)

    image = fields.Image(string="Image", compute='_compute_image')

    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920

    def action_stock_move_line(self):
        return {"type": "ir.actions.act_window", "name": "Transfer", "view_mode": "form", "res_model": "stock.move.line", "res_id": self.id}
