try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO

from odoo.exceptions import UserError
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    google_map_link = fields.Char(string='Google Map Link', compute="calculate_map_link")
    partner_id = fields.Many2one('res.partner', string='Customer')
    qr_location = fields.Char(string="Old Location")

    

    # @api.depends('qr_location')
    # def generate_qr(self):
    #     """Generate a QR code based on the partner's qr_location and store it in
    #     the 'qr' field of the partner record."""
    #     if qrcode and base64:
    #         if not self.qr_location:  
    #             qr = qrcode.QRCode(
    #                 version=1,
    #                 error_correction=qrcode.constants.ERROR_CORRECT_L,
    #                 box_size=10,
    #                 border=4,
    #             )
    #             qr.add_data(self.qr_location)
    #             qr.make(fit=True)
    #             img = qr.make_image()
    #             temp = BytesIO()
    #             img.save(temp, format="PNG")
    #             qr_image = base64.b64encode(temp.getvalue())
    #             self.write({'qr': qr_image})
    #             return self.env.ref(
    #                 'partner_location.print_qr').report_action(self, data={
    #                 'data': self.id, 'type': 'cust'})
    #         else:
    #             raise UserError(
    #                 _('Necessary Requirements To Run This Operation Is Not '
    #                 'Satisfied'))


    @api.depends('partner_latitude','partner_longitude')
    def calculate_map_link(self):
        for rec in self:
            rec.google_map_link = "http://maps.google.com/maps?q="+str(rec.partner_latitude)+ "," +str(rec.partner_longitude)



    
    

  



    





  
