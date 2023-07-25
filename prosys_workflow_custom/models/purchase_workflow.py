from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(
        selection_add=[
        ('f_approve', 'First Approve'),
        ('s_approve', 'secound Approve'),
        ('th_approve', 'third Approve'),

        ],
        ondelete={
            'f_approve': 'cascade',
            's_approve': 'cascade',
            'th_approve': 'cascade',

        },
        )
    
   
    # def button_approve_one(self):
    #     self.write({'state': 'f_approve'})
    #     return {}

    def button_approval_tow_action(self):
        self.state ='f_approve'
    
    def button_approval_tow(self):
        self.state='s_approve'
    
    def button_approval_three(self):
        self.state='th_approve'


    def button_confirm_purchase(self):
         self.state='purchase'

    