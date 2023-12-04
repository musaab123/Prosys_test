from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class PayByPetty(models.TransientModel):
   _name = 'pay.by.petty.wizard'

   employee_id = fields.Many2one('hr.employee', string="Employee")
   petty_id = fields.Many2many('petty.cash', string='Petty Cash')
   journal_id = fields.Many2one('account.journal', string='Payment Method')
   payment_method_id = fields.Many2one('account.payment.method', string="Payment Type")
   amount = fields.Float('Payment Amount')
   balance = fields.Float('Balance', readonly=True)
   total_balance = fields.Float('Total Balance', readonly=True)
   currency_id = fields.Many2one('res.currency', string="Currency")
   company_id = fields.Many2one('res.company', string='Company',
                                default=lambda self: self.env.company)


   @api.onchange('employee_id')
   def _onchange_employee_id(self):
      self.petty_id = False
      if self.employee_id:
         pets = self.env['petty.cash'].search([('employee_id', '=', self.employee_id.id), ('balance', '>', 0.0)])
         petty_list = []
         for rec in pets:
            if rec.balance > 0.0:
               petty_list.append(rec.id)
         if pets:
            return {
               'domain': {'petty_id': [('id', 'in', petty_list)]}}

         else:
            return {
               'domain': {'petty_id': [('id', '=', [])]}}
      else:
         return {
            'domain': {'petty_id': [('id', '=', [])]}}

   @api.onchange('petty_id')
   def set_balances(self):
      print("yes Im in onchange", self.env.context.get('default_amount'), self.env.context.get('default_journal_id'))

      #set expense amount
      expense_sheet_id = self.env.context.get('active_id')
      if expense_sheet_id:
         sheet_id = self.env['hr.expense.sheet'].search([('id', '=', expense_sheet_id)])
         self.amount = sheet_id.amount_residual

      #set payment method and set balances
      if self.petty_id:
         self.journal_id = self.petty_id.journal_id
         self.balance = self.petty_id.balance
         self.total_balance = self.petty_id.balance

   def create_payment(self):
      if not self.employee_id:
         raise ValidationError(_('Employee field is required '))
      if not self.petty_id:
         raise ValidationError(_('Petty Cash is required '))
      if not self.payment_method_id:
         raise ValidationError(_('Payment Type is required '))
      if not self.amount:
         raise ValidationError(_('Amount is required '))

      sheet_id = self.env['hr.expense.sheet'].search([('id', '=', self.env.context.get('active_id'))])
      expense_id = self.env['hr.expense'].search([('sheet_id', '=', sheet_id.id)])
      payment_id = self.env['account.payment'].create({
         'partner_type': 'supplier',
         'payment_type': 'outbound',
         'partner_id': self.employee_id.user_id.partner_id.id,
         'amount': self.amount,
         'journal_id': self.petty_id.journal_id.id,
         'payment_method_line_id': self.payment_method_id.id,
         'currency_id': sheet_id.currency_id.id,
         'company_id': self.company_id.id,
      })

      payment_id.name = False
      payment_id.action_post()

      #reconcile expense with the payment
      account_move_lines_to_reconcile = self.env['account.move.line']
      for line in payment_id.invoice_line_ids + sheet_id.account_move_id.line_ids:
         if line.account_id.account_type == 'liability_payable' and line.reconciled == False:
            account_move_lines_to_reconcile |= line
      # print("LLLL", account_move_lines_to_reconcile)
      account_move_lines_to_reconcile.reconcile()

      if self.amount > self.petty_id.balance:
          raise ValidationError(_('You Cannot Exceed Employee Balance '))
      # for petty in self.petty_id:
      #    if self.amount > 0.0 and self.petty_id.balance > 0.0:
      #       if self.amount > self.petty_id.balance:
      #          self.create_payment(petty, petty.balance, expense_sheet)
      #          amount -= petty.balance
      #       else:
      #          self.create_payment(petty, amount, expense_sheet)
      #          amount = 0.0

      #change expense sheet states
      sheet_id.state = 'done'
      sheet_id.payment_state = 'paid'

      petty = self.env['petty.cash.line'].create({
         'name': sheet_id.name,
         'amount': payment_id.amount,
         'petty_id': self.petty_id.id,
      })

      print("print petty", petty)

      return True