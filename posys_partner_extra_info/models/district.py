from odoo import models, fields, api, tools


class District(models.Model):
    _name = 'district.district'

    name = fields.Char(String="District" ,translate=True)
    code = fields.Char(String="Code" ,translate=True)






   

