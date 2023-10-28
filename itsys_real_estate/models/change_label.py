from odoo import api, fields, models 

class ResPartner(models.Model):
    _inherit = 'res.partner'

    district =fields.Char("District")

    build_number =fields.Char(" Build Number")
    branch_number =fields.Char(" Build Number")
    email_code =fields.Char(" Build Number")

