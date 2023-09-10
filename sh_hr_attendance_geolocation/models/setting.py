# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    distance_id = fields.Float(string='Distance',  config_parameter='sh_hr_attendance_geolocation_distance_id', default=200)
