from odoo import models, fields, api, tools

class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']
    distance_id = fields.Float(string='Distance',  config_parameter='partner_location_distance_id')
