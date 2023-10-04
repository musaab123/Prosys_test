# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import models, fields, api


class ProductBrand(models.Model):
    _inherit = 'product.template'

    season_id = fields.Many2one('product.season', string='Season')

    # def _calculate_amount(self):
    #     hs_code_array = []
        
    #     for rec in self.season_id:  
    #         amount = 0
    #         quantity = 0
            
    #         for product in rec.product_ids:
    #             quantity += product.product_uom_qty
    #             amount += product.price_subtotal
            
    #         vals = {'hs_code': rec.name,  
    #                 'quantity': quantity,
    #                 'amount': amount}
            
    #         hs_code_array.append(vals)
    #     print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',hs_code_array)
    #     return hs_code_array

            


class BrandProduct(models.Model):
    _name = 'product.season'

    name = fields.Char(String="Name" ,translate=True)
    # qty_available = fields.integer(sring="avelable")




    @api.model
    def get_total_quantity(self, season_id):
        season = self.env['product.season'].search([('code', '=', season_id)], limit=1)
        if  season and season.product_ids:
            total_quantity = sum(product.qty_available for product in season.product_ids)
            return total_quantity
        return 0



    brand_image = fields.Binary()
    member_ids = fields.One2many('product.template', 'season_id')
    product_count = fields.Char(String='Product Count', compute='get_count_products', store=True)


    @api.depends('member_ids')
    def get_count_products(self):
        print('season')
        self.product_count = len(self.member_ids)


class BrandReportStock(models.Model):
    _inherit = 'stock.quant'

    # brand_id = fields.Many2one(related='product_id.brand_id',
    #                            string='Brand', store=True, readonly=True)
    
    season_id = fields.Many2one(related='product_id.season_id',
                               string='Season', store=True, readonly=True)
