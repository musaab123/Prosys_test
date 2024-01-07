from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare, float_round
import logging

_logger = logging.getLogger(__name__)


class CustomStockPicking(models.Model):
    _inherit = 'sale.order.line'
    test = fields.Char(string="fffff")