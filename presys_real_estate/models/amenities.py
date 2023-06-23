from odoo import models, fields, api, _
import odoo.tools
import logging
logger= logging.getLogger(__name__)

class amenitiesTest(models.Model):
    _name = "amenities.test"

    amenities_id_first = fields.Char(string="Amenities ID")
    amenities_birth_day_first =fields.Date(string="Amenities birth day")
    amenities_id = fields.Many2one('res.partner' )
