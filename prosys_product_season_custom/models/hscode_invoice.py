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

from odoo import models, fields, api, tools


class ProductBrand(models.Model):
    _inherit = 'product.template'

    season_id = fields.Many2one('product.season', string='Season')


class BrandProduct(models.Model):
    _name = 'product.season'

    name = fields.Char(String="Name")
    brand_image = fields.Binary()
    member_ids = fields.One2many('product.template', 'season_id')
    product_count = fields.Char(String='Product Count', compute='get_count_products', store=True)
    code = fields.Char(String="Code")

    @api.depends('member_ids')
    def get_count_products(self):
        self.product_count = len(self.member_ids)


class SeasonPivotInvoicing(models.Model):
    _inherit = "account.invoice.report"

    season_id = fields.Many2one('product.season', string='Season')

    def _select(self):
        res = super(SeasonPivotInvoicing, self)._select()
        query = res.split('template.categ_id                                           AS product_categ_id,', 1)
        res = query[0] + 'template.categ_id as product_categ_id,template.season_id as season_id,' + query[1]
        return res
   
   
    def _group_by(self):
        res = super(SeasonPivotInvoicing, self)._group_by()
        query = res.split('template.categ_id,', 1)
        res = query[0] + 'template.categ_id,template.season_id,' + query[1]
        return res
