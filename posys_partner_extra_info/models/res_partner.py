from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
class ResPArtnerInherit(models.Model):
    _inherit = 'res.partner'

    categ_id = fields.Many2many('clint.activty', string='Clint Activty')



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # driver_id = fields.Char(string="Driver" ,store=True)
    driver_id = fields.Many2one('hr.employee', string="Driver", help='Select corresponding Employee')

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['driver_id'] = self.driver_id.id       
        return invoice_vals
    

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order','Sale Order')

   
    driver_id = fields.Many2one(related='sale_id.driver_id', readonly=False, store=True)


class AccountMove(models.Model):
    _inherit = 'account.move'

    # driver_id = fields.Char(string="Driver" ,store=True)
    driver_id = fields.Many2one('hr.employee', string="Driver", help='Select corresponding Employee')




class res_partner(models.Model):
    _inherit = 'res.partner'

    additional_code =fields.Char("Additional Code")
    buliding_number =fields.Char("Bulding Number")
    google_map_link = fields.Char(string='Google Map Link')











