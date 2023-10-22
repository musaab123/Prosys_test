from odoo import models, fields, api
from odoo.tools.misc import format_date, formatLang

     
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_customer_invoice = fields.Boolean('Customer Invoice (Portal)')