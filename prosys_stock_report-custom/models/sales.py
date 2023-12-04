from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    category_id = fields.Many2many('res.partner.category', column1='partner_id',
                                    column2='category_id', string='Tags', required=True )

