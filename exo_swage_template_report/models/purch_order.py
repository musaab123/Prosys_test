from odoo import api,fields, models, _

class prosys_company(models.Model):
    
    _inherit = "purchase.order"
    date_creation = fields.Date('Created Date', invisable=True, default=fields.Date.today())

    move_type = fields.Selection(
        selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ],
        string='Type',
        required=True,
        readonly=True,
        tracking=True,
        change_default=True,
        index=True,
        default="entry",
    )


class SaleOrder(models.Model):
    _inherit = "sale.order"
    date_creation = fields.Date('Created Date', invisable=True, default=fields.Date.today())
    # sale_persone_code = fields.Char(string="Salesperson Code" ,compute = '_compute_saleperson_code',store=True)
    employee_office = fields.Char(string="Employee Office")
    employee_sequence = fields.Char(
        string='Salepersone Code', readonly=False, compute = '_compute_employee_seq',
        help="Employee joining date computed from the contract start date",
        )


    @api.depends('employee_sequence')
    def _compute_employee_seq(self):
        for record in self:
            code = ""
            o_code = self.env['ir.sequence'].next_by_code('seqemp.seqemp')
            print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv" ,o_code)
            record.employee_sequence = str(code) + str(o_code)



    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['employee_sequence'] = self.employee_sequence
        return invoice_vals




