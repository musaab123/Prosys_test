# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Midilaj (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api


class ProductBrand(models.Model):
    _inherit = 'product.template'

    season_id = fields.Many2one('product.season', string='Season')


class BrandProduct(models.Model):
    _name = 'product.season'

    name = fields.Char(String="Name" ,translate=True)

    brand_image = fields.Binary()
    member_ids = fields.One2many('product.template', 'season_id')
    product_count = fields.Char(String='Product Count',
                                compute='get_count_products', store=True)

    @api.depends('member_ids')
    def get_count_products(self):
        self.product_count = len(self.member_ids)


class BrandPivot(models.Model):
    _inherit = 'sale.report'

    season_id = fields.Many2one('product.season', string='Season')


    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['season_id'] = "t.season_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            t.season_id"""
        return res
