# Copyright 2021 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    old_barcode = fields.Char(string='Old Barcode', related='product_variant_ids.old_barcode', readonly=False)


    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []

        if name:
            domain = ['|', '|', '|', ('name', operator, name), ('default_code', operator, name),
                    ('barcode', operator, name), ('old_barcode', operator, name)]

        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
    



    @api.onchange('old_barcode')
    def _onchange_old_barcode(self):
        if self.old_barcode:
            domain = [('active', '=', True), ('old_barcode', '=', self.old_barcode)]
            if self.id:
                domain.append(('id', '!=', self.id))
            duplicate_products = self.search(domain)
            if duplicate_products:
                raise UserError(
                    _(
                        "The old barcode provided for this product already exists in other active products."
                    )
                )

    # @api.constrains('barcode', 'old_barcode', 'active')
    # def _check_unique_barcode(self):
    #     for product in self:
    #         if product.active and (product.old_barcode):
    #             domain = [('active', '=', True)]
                
    #             if product.old_barcode:
    #                 domain.append('|')
    #                 domain.extend([
    #                     ('old_barcode', '=', product.old_barcode),
    #                 ])

    #             if product.id:
    #                 domain.append(('id', '!=', product.id))

    #             duplicate_products = self.search(domain)

    #             if duplicate_products:
    #                 raise UserError(
    #                     _(
    #                         "The old barcode provided for product '%s' already exists in other active products."
    #                     ) % product.name
    #                 )


    # @api.constrains('barcode', 'old_barcode', 'active')
    # def _check_unique_barcode(self):
    #     for product in self:
    #         if product.active and (product.old_barcode):
    #             domain = [('active', '=', True)]
                
    #             # if product.barcode:
    #             #     domain.extend([
    #             #         '|',
    #             #         ('barcode', '=', product.barcode),
    #             #         ('old_barcode', '=', product.barcode),
    #             #     ])
                    
    #             if product.old_barcode:
    #                 domain.append('|')
    #                 domain.extend([
    #                     ('old_barcode', '=', product.old_barcode),
    #                 ])

    #             if product.id:
    #                 domain.append(('id', '!=', product.id))

    #             duplicate_products = self.search(domain)

    #             if duplicate_products:
    #                 raise UserError(
    #                     _(
    #                         "The barcode or old barcode provided for product '%s' already exists in other active products."
    #                     ) % product.name
    #                 )

    # @api.constrains('barcode', 'old_barcode', 'active')
    # def _check_unique_barcode(self):
    #     for product in self:
    #         if product.active and (product.barcode or product.old_barcode):
    #             domain = [('active', '=', True)]
    #             if product.barcode:
    #                 domain.extend([
    #                     '|',
    #                     ('barcode', '=', product.barcode),
    #                     ('old_barcode', '=', product.barcode),
    #                 ])
    #             if product.old_barcode:
    #                 domain.append(('old_barcode', '=', product.old_barcode))

    #             if product.id:
    #                 domain.append(('id', '!=', product.id))

    #             duplicate_products = self.search(domain)

    #             if duplicate_products:
    #                 raise UserError(
    #                     _(
    #                         "The barcode or old barcode provided for product '%s' already exists in other active products."
    #                     ) % product.name
    #                 )

