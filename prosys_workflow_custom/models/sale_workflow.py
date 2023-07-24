from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'sale.order'

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
    
   


    def approval_one(self):
        self.state ='f_approve'
    
    def approval_tow(self):
        self.state='s_approve'
    
    def approval_three(self):
        self.state='th_approve'
        