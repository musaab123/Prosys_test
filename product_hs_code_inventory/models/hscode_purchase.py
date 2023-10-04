# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Amaya Aravind EV (<https://www.cybrosys.com>)
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

    hscode_id = fields.Many2one('product.hs', string='Hs Code')


class BrandProduct(models.Model):
    _name = 'product.hs'

    name = fields.Char(String="Name" ,translate=True)
    brand_image = fields.Binary()
    member_ids = fields.One2many('product.template', 'hscode_id')
    product_count = fields.Char(String='Product Count', compute='get_count_products', store=True)

    @api.depends('member_ids')
    def get_count_products(self):
        self.product_count = len(self.member_ids)


class PurchaseHsCodePivot(models.Model):
    _inherit = 'purchase.report'

    hscode_id = fields.Many2one('product.hs', string='Hs Code')

    def _select(self):
        res = super(PurchaseHsCodePivot, self)._select()
        query = res.split('t.categ_id as category_id,', 1)
        rese = query[0] + 't.categ_id as category_id,t.hscode_id as hscode_id,' + query[1]
        return rese

    def _group_by(self):
        res = super(PurchaseHsCodePivot, self)._group_by()
        query = res.split('t.categ_id,', 1)
        res = query[0] + 't.categ_id,t.hscode_id,' + query[1]
        return res
