# my_module/models/sale_order.py
from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.tools import config
import requests
import re



class ResPartner(models.Model):
    _inherit = "res.partner"
    
    google_map_link = fields.Char(string='Google Map Link', compute="calculate_map_link")
    partner_id = fields.Many2one('res.partner', string='Customer')

    @api.depends('partner_latitude','partner_longitude')
    def calculate_map_link(self):
        for rec in self:
            rec.google_map_link = "http://maps.google.com/maps?q="+str(rec.partner_latitude)+ "," +str(rec.partner_longitude)

    
    

  



    





  
