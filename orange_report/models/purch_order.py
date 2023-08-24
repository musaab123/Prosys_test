from odoo import api,fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move.line'


    product_packaging_id = fields.Many2one(
            comodel_name='product.packaging',
            string="Packaging",
            store=True, readonly=False, precompute=True,
            domain="[('sales', '=', True), ('product_id','=',product_id)]",
            check_company=True)
    
    product_packaging_qty = fields.Float(
            string="Packaging Quantity",
            store=True, readonly=False, precompute=True)




class ResCompany(models.Model):
    _inherit = 'res.company'

    arabic_name = fields.Char('Arabic Name')
    arabic_street = fields.Char('Arabic Street')
    arabic_street2 = fields.Char('Arabic Street2')
    arabic_city = fields.Char('Arabic City')
    arabic_state = fields.Char('Arabic State')
    arabic_country = fields.Char('Arabic Country')
    arabic_zip = fields.Char('Arabic Zip')
    arabic_web = fields.Char('Arabic Website')
    arabic_company_dis = fields.Char('Arabic  Company description')