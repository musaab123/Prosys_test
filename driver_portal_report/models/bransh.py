from odoo import api,fields, models, _

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


    





    
