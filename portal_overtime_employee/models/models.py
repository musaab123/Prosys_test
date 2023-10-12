from datetime import datetime, timedelta
from odoo import models, fields, _, api

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    is_overtime_employee = fields.Boolean('Overtime (Portal)')





