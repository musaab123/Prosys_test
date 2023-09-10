# Part of Softhealer Technologies.
from odoo import models, fields

class HrEmployeeLocation(models.Model):
    _inherit = "hr.work.location"



    

    #inherited hr.attendance model and added new fields
    message_in = fields.Char('Check in message')
    message_out = fields.Char('Check out message')
    in_latitude = fields.Char("Latitude ")
    in_longitude = fields.Char("Longitude ")
    out_latitude = fields.Char("Latitude")
    out_longitude = fields.Char("Longitude")
    check_in_url = fields.Char("Open Check-in location in Google Maps")
    



class HrEmployee(models.Model):
    _inherit = "hr.employee"

    #inherited hr.attendance model and added new fields
    is_representer = fields.Boolean('Is Representer')
    # distance_test = fields.Float(string='Distance (km)')


  
