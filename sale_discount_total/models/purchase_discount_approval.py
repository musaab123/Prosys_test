from odoo import api, fields, models


class purchase_discount(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_confirm(self):
        discnt = 0.0
        no_line = 0.0
        if self.company_id.so_double_validation == 'two_step':
            for line in self.order_line:
                no_line += 1
                discnt += line.discount
            discnt = (discnt / no_line)
            if self.company_id.so_double_validation_limit and discnt > self.company_id.so_double_validation_limit:
                self.state = 'to approve'
                return True
        super(purchase_discount, self).button_confirm()

    def action_approve(self):
        super(purchase_discount, self).button_confirm()
        return True


class Company(models.Model):
    _inherit = 'res.company'

    so_double_validation = fields.Selection([
        ('one_step', 'Confirm sale orders in one step'),
        ('two_step', 'Get 2 levels of approvals to confirm a sale order')
    ], string="Levels of Approvals", default='one_step',
        help="Provide a double validation mechanism for sales discount")

    so_double_validation_limit = fields.Float(
        string="Percentage of Discount that requires double validation'",
        help="Minimum discount percentage for which a double validation is "
             "required")


class ResDiscountSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Sale Discount Approval", default=lambda
        self: self.env.user.company_id.so_double_validation == 'two_step')

    so_double_validation = fields.Selection(
        related='company_id.so_double_validation',
        string="Levels of Approvals *", readonly=False)
    so_double_validation_limit = fields.Float(
        string="Discount limit requires approval in %",
        related='company_id.so_double_validation_limit', readonly=False)

    def set_values(self):
        super(ResDiscountSettings, self).set_values()
        self.so_double_validation = 'two_step' if self.so_order_approval else 'one_step'
