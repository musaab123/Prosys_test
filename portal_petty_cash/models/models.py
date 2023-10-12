from datetime import datetime, timedelta
from odoo import models, fields, _, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_petty_person = fields.Boolean('Petty Cash (Portal)')





