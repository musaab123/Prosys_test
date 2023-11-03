# my_module/models/sale_order.py
from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    google_map_link = fields.Char(string='Google Map Link')

    

        


  



    





  
