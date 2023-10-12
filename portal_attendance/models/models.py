from datetime import datetime, timedelta
from odoo import models, fields, _, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_attendance_person = fields.Boolean('Attendance (Portal)')





