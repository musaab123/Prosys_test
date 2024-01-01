from odoo import api,fields, models, _
import base64
from num2words import num2words

class prosys_company(models.Model):
    
    _inherit = "sale.order"




class ResCompany(models.Model):
    _inherit = 'res.company'

    arabic_name = fields.Char('Arabic Name')
    # arabic_street = fields.Char('Arabic Street')
    # arabic_street2 = fields.Char('Arabic Street2')
    # arabic_city = fields.Char('Arabic City')
    # arabic_state = fields.Char('Arabic State')
    # arabic_country = fields.Char('Arabic Country')
    # arabic_zip = fields.Char('Arabic Zip')
    # arabic_web = fields.Char('Arabic Website')
    # arabic_company_dis = fields.Char('Arabic  Company description')

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    arabic_address = fields.Char(string="Arabic Adress")
    english_address = fields.Char(string ="Arabic English")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    driver_note = fields.Html( string="Terms and conditions")

class CrmTeam(models.Model):
    _inherit = 'stock.picking'

    team_id = fields.Many2one(
        comodel_name='crm.team',
        string="Sales Team",
       )

class AccountMove(models.Model):
    _inherit = 'account.move'

    def amount_word(self, amount):
        language = self.partner_id.lang or 'en'
        language_id = self.env['res.lang'].search([('code', '=', 'ar_AA')])
        if language_id:
            language = language_id.iso_code
        amount_str = str('{:2f}'.format(amount))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]
        before_amount_words = num2words(int(before_point_value), lang=language)
        after_amount_words = num2words(int(after_point_value), lang=language)
        amount = before_amount_words + ' ' + after_amount_words
        return amount

    def amount_total_words(self, amount):
        words_amount = self.currency_id.amount_to_text(amount)
        return words_amount
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def amount_word(self, amount):
        language = self.partner_id.lang or 'en'
        language_id = self.env['res.lang'].search([('code', '=', 'ar_AA')])
        if language_id:
            language = language_id.iso_code
        amount_str = str('{:2f}'.format(amount))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]
        before_amount_words = num2words(int(before_point_value), lang=language)
        after_amount_words = num2words(int(after_point_value), lang=language)
        amount = before_amount_words + ' ' + after_amount_words
        return amount

    def amount_total_words(self, amount):
        words_amount = self.currency_id.amount_to_text(amount)
        return words_amount

    



    





    
