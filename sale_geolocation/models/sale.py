# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    latitude = fields.Char(readonly=True)
    longitude = fields.Char(readonly=True)
    gelocation_error_msg = fields.Char()

    def action_open_google_map(self):
        if not self.latitude or not self.longitude:
            raise UserError(_("Latitude or Longitude is missing!"))
        url = 'https://www.google.com/maps/search/?api=1&query=' + self.latitude + '%2C' + self.longitude
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            'target_type': 'public'
        }
