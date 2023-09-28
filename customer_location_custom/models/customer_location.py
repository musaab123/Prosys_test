# my_module/models/sale_order.py
from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    latitude = fields.Float(string='Latitude', digits=(9, 6))
    longitude = fields.Float(string='Longitude', digits=(9, 6))
    google_map_link = fields.Char(string='Google Map Link')

    @api.onchange('latitude', 'longitude')
    def _onchange_latitude_longitude(self):
        for order in self:
            if order.latitude and order.longitude:
                order.google_map_link = f'https://www.google.com/maps?q={order.latitude},{order.longitude}'
            else:
                order.google_map_link = ''


    
    def open_google_map(self):
        if not (self.latitude and self.longitude):
            raise UserError('Latitude and longitude are not available.')
        return {
            'type': 'ir.actions.act_url',
            'url': f'https://www.google.com/maps?q={self.latitude},{self.longitude}',
            'target': 'new',
        }


    def update_geolocation(self, latitude, longitude):
        self.ensure_one()
        self.write({'latitude': latitude, 'longitude': longitude})

    def action_confirm(self):
        for order in self:
            if not (order.latitude and order.longitude):
                # Fetch the user's geolocation based on your JavaScript implementation
                # You should pass latitude and longitude from the frontend to this method

                # Example: Replace these lines with the data from your JavaScript code
                latitude_from_frontend = 21.5216329
                longitude_from_frontend = 39.1746861

                if latitude_from_frontend and longitude_from_frontend:
                    order.write({'latitude': latitude_from_frontend, 'longitude': longitude_from_frontend})
                else:
                    raise UserError('Failed to fetch geolocation.')
        
        # Call the super method to complete the confirmation
        return super(SaleOrder, self).action_confirm()


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['latitude'] = self.latitude
        invoice_vals['longitude'] = self.longitude
        invoice_vals['google_map_link'] = self.google_map_link
        return invoice_vals


    





  
