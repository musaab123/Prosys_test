from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    def pay_by_petty(self):
        petty_cash_id = self.env['petty.cash'].search([('employee_id', '=', self.employee_id.id)])
        view = self.env.ref('petty_cash_extention.pay_by_petty_wizard_form')
        wizard = self.env['pay.by.petty.wizard'].create({
            'employee_id': self.employee_id.id
        })
        petty_cash_id = self.env['petty.cash'].search([('employee_id', '=', self.employee_id.id)])
        employee_partner_id = self.employee_id.address_home_id.commercial_partner_id.id
        if not employee_partner_id:
            raise UserError(_("No Home Address found for the employee %s, please configure one.") % (
                self.employee_id.name))

        return {
            'name': _('Add Payment By Petty Cash'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'pay.by.petty.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': wizard.id,
            'target': 'new',
            'context': {'default_amount': self.amount_residual, 'default_journal_id': petty_cash_id.journal_id.id}
        }

