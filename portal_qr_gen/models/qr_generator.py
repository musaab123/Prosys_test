from odoo import models, fields, api,_, tools
from datetime import datetime, timedelta
from collections import defaultdict
import random
import string
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO


class Company(models.Model):
    _inherit = "res.company"

    qr_limited_time = fields.Integer('QR Limited Time Per Min',default=30)

    @api.onchange('qr_limited_time')
    def onchange_qr_limited_time(self):
        # Update Corn job interval number
        cron_job = self.env.ref('portal_qr_gen.ir_cron_qr_generate')

        cron_job.write({
            'interval_number': self.qr_limited_time,
        })
    

class QRGenerator(models.Model):
    _name = "qr.generator.model"


    creation_time = fields.Datetime('Creation Time')
    url = fields.Char('Products Screen URL')
    unique_code = fields.Char('Unique Code')
    qr_image = fields.Binary('QR')

    # cron job action function for creating urls and delete in invalid url's
    def _autocheck_create_qr(self):
        records = self.env['qr.generator.model'].search([])
        if records:
            for rec in records:
                current_datetime = datetime.now()
                creation_time = rec.creation_time + timedelta(minutes=self.env.company.qr_limited_time)
                if creation_time <= current_datetime:
                    unique_num = str(rec.id + 1)
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    url = str(base_url) + '/add/products/'
                    characters = string.ascii_letters + string.digits
                    random_string = ''.join(random.choices(characters, k=25))
                    random_string = unique_num + random_string
                    url += random_string
                    # qr generator
                    qr = qrcode.QRCode(
                        version=3,
                        error_correction=qrcode.constants.ERROR_CORRECT_M,
                        box_size=4,
                        border=4,
                    )
                    qr.add_data(url)
                    qr.make(fit=True)
                    img = qr.make_image()
                    temp = BytesIO()
                    img.save(temp, format="PNG")
                    qr_image = base64.b64encode(temp.getvalue())
                    vals = {
                        'creation_time':datetime.now(),
                        'url':url,
                        'unique_code':random_string,
                        'qr_image':qr_image,
                    }
                    self.env['qr.generator.model'].create(vals)

                    #  delete the current record
                    rec.unlink()
        else:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = str(base_url) + '/add/products/'
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choices(characters, k=25))
            random_string = '1' + random_string
            url += random_string
            # qr generator
            qr = qrcode.QRCode(
                version=3,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=4,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            vals = {
                'creation_time':datetime.now(),
                'url':url,
                'unique_code':random_string,
                'qr_image':qr_image,
            }
            self.env['qr.generator.model'].create(vals)
