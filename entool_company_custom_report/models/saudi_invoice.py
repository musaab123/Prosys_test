# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
import base64
from num2words import num2words
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    user_sequence = fields.Char(string="Salepersone Code" ,store=True)
    employee_office = fields.Many2one('hr.employee','Employee Office')

    invoice_date_supply = fields.Datetime('Date Of Supply')
    date_creation = fields.Date('Created Date', invisable=True, default=fields.Date.today())


    def action_invoice_tax_report(self, type):
        self.ensure_one()
        if type == 'tax_invoice':
            template = self.env.ref('saudi_einvoice_knk.email_template_edi_invoice_tax_etir', raise_if_not_found=False)
        elif type == 'simplified_tax_invoice':
            template = self.env.ref('saudi_einvoice_knk.email_template_edi_invoice_etir', raise_if_not_found=False)
        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            active_ids=[self.id],
            default_res_model='account.move',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def get_product_arabic_name(self, pid):
        IrTranslation = self.env['ir.translation']
        domain = [
            ('name', '=', 'product.product,name'), ('state', '=', 'translated')]
        translation = IrTranslation.search(domain+[('res_id', '=', pid)])
        if translation:
            return translation.value
        else:
            product = self.env['product.product'].browse(int(pid))
            translation = IrTranslation.search(domain + [('res_id', '=', product.product_tmpl_id.id)])
            if translation:
                return translation.value
        return ''

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

    @api.model
    def get_qr_code(self):
        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array
        for record in self:
            qr_code_str = ''
            seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
            company_vat_enc = get_qr_encoding(2, record.company_id.vat or '')
            # date_order = fields.Datetime.from_string(record.create_date)
            if record.invoice_date_supply:
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'), record.invoice_date_supply)
            else:
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'), record.create_date)
            timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
            invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
            total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(record.amount_total - record.amount_untaxed)))

            str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
            qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            return qr_code_str


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
    date_creation = fields.Date('Created Date', invisable=True, default=fields.Date.today())






class CrmTeam(models.Model):
    _inherit = 'crm.team'

    
    driver_note = fields.Html( string="Terms and conditions")

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
   

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    qr_location = fields.Char(string="location")


   
    qr_location = fields.Char(string="location")

    @api.model
    def generate_qr(self):
        def get_qr_encoding(field):
            return field.encode('UTF-8')

        for record in self:
            partner_location_enc = get_qr_encoding(record.partner_id.qr_location)
            qr_code_str = partner_location_enc.decode('ISO-8859-1') 
            return qr_code_str


    # @api.model
    # def generate_qr(self):
    #     def get_qr_encoding(tag, field):
    #         company_name_byte_array = field.encode('UTF-8')
    #         print("company_name_byte_array1",company_name_byte_array)          

    #         company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
    #         print("company_name_tag_encoding2",company_name_tag_encoding)          

    #         company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
    #         print("company_name_length_encoding",company_name_length_encoding)          

    #         return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array
    #     for record in self:
    #         qr_code_str = ''
    #         partner_location_enc = get_qr_encoding(1, record.partner_id.qr_location) 
    #         print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",partner_location_enc)          
    #         qr_code_str = partner_location_enc
    #         print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",qr_code_str)          

    #         return qr_code_str
        