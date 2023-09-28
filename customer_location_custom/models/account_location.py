# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, _, api


class AccountMove(models.Model):
    _inherit = 'account.move'


    latitude = fields.Float(string='Latitude', digits=(9, 6))
    longitude = fields.Float(string='Longitude', digits=(9, 6))
    google_map_link = fields.Char(string='Google Map Link')

   