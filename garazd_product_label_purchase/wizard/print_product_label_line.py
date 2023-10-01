# Copyright © 2023 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import fields, models


class PrintProductLabelLine(models.TransientModel):
    _inherit = "print.product.label.line"

    purchase_id = fields.Many2one(comodel_name='purchase.order', readonly=True)
