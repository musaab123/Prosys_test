# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.misc import format_date, formatLang


class AccountPayment(models.Model):

	_inherit="account.payment"
	
	collecter_id=fields.Many2one("res.users",string="Cash Collecters")

	collecter_ids=fields.Many2many(related="partner_id.collecter_ids")
     

     
      
    
        


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    collecter_id=fields.Many2one("res.users",string="Cash Collecters")

    collecter_ids=fields.Many2many(related="partner_id.collecter_ids")


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['collecter_id'] = self.collecter_id.id
        return invoice_vals




class ResPartner(models.Model):
	_inherit='res.partner'
	collecter_ids=fields.Many2many("res.users",string="Cash Collecters")


class AccountMove(models.Model):
	_inherit='account.move'

	paid_amount=fields.Float("Paid Amount",compute="cal_paid_amount")
	collecter_id=fields.Many2one("res.users",string="Cash Collecters")
	collecter_ids=fields.Many2many(related="partner_id.collecter_ids")
      
      
    


	@api.depends('amount_total_signed','amount_residual')
	def cal_paid_amount(self):
		for rec in self:
			rec.paid_amount=rec.amount_total_signed-rec.amount_residual
       	





class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        # action = super(AccountPaymentRegister, self).action_create_payments()
        payments = self._create_payments()

        for payment in payments:
            
            move_id = self.env["account.move"].search([('name' ,'=' ,payment.ref)])
            if type(payment.ref) != bool:
                if move_id.collecter_id:
                    payment.ref = payment.ref  +"-" + move_id.collecter_id.name
            else:
                payment.ref = move_id.collecter_id.name
            
        if self._context.get('dont_redirect_to_payments'):

            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        return action




class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_sales_person = fields.Boolean('Cash Collector (Portal)')



