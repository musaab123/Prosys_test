from odoo import api,fields, models, _

class ResUsers(models.Model):
    _inherit = "res.users"

    employee_sequence = fields.Char(string='Salepersone Code')

