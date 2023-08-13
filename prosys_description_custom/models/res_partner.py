from odoo import models, fields, api, _
import odoo.tools

class sale_order(models.Model):
    _inherit = 'product.hs'

    description = fields.Char(string='Description')
  