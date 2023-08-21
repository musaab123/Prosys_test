from odoo import models, fields, api,_, tools

from collections import defaultdict


class ProductTemplate(models.Model):
    _inherit = "product.template"


    barcode = fields.Char('Barcode', compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode',readonly=True)
    # default_code = fields.Char('Internal Reference', compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode',readonly=True)
    default_code = fields.Char('Internal Reference' ,readonly=True)

    barcode_check = fields.Boolean('Barcode Check',default=False)
    original_barcode = fields.Char('Barcode')
    original_code = fields.Char('code')

    vendor_reference_number = fields.Char(string="Vendor Reference Number")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     print('\n\n\n\n\n\n\n\n\n\n')
    #     print(vals_list)
    #     print('\n\n\n\n\n\n\n\n\n\n')
    #     for vals in vals_list:
    #         vals['barcode'] = self.env['ir.sequence'].next_by_code('barcode.sequence')
    #     print('\n\n\n\n\n\n\n\n\n\n')
    #     print(vals_list)
    #     print('\n\n\n\n\n\n\n\n\n\n')
    #     products = super(ProductTemplate, self.with_context(create_product_product=True)).create(vals_list)
    #     print('\n\n\n\n\n\n\n\n\n\n')
    #     print(products)
    #     print(products.barcode)
    #     print('\n\n\n\n\n\n\n\n\n\n')
        
    #     # if not products.barcode :
    #     #     print('\n\n\n\n\n\n\n\n\n\n')
    #     #     print(products)
    #     #     print(self.env['ir.sequence'].next_by_code('barcode.sequence'))
    #     #     print('\n\n\n\n\n\n\n\n\n\n')
    #     #     products.barcode = self.env['ir.sequence'].next_by_code('barcode.sequence')
    #     # # `_get_variant_id_for_combination` depends on existing variants
    #     # self.clear_caches()
    #     return products

    @api.depends('product_variant_ids.barcode')
    def _compute_barcode(self):
        # self.barcode = False
        for template in self:
            if template.barcode_check == False:
                code = ""
                if not template.barcode:
                    if template.factory_id:
                        code += str(template.factory_id.code)
                    if template.brand_id:
                        code += str(template.brand_id.code)
                    # if template.hscode_id:
                    #     code += str(template.hscode_id.code)
                    if template.categ_id:
                        code += str(template.categ_id.code)
                    o_code = self.env['ir.sequence'].next_by_code('barcode.sequence')
                    template.barcode = str(code) + str(o_code)
                    # template.default_code = str(code) + str(o_code)

                    template.barcode_check = True
                    template.original_code = o_code
                    template.original_barcode = template.barcode
                    # template.original_barcode = template.default_code
                else:
                    if template.factory_id:
                        code += str(template.factory_id.code)
                    if template.brand_id:
                        code += str(template.brand_id.code)
                    # if template.hscode_id:
                    #     code += str(template.hscode_id.code)
                    if template.categ_id:
                        code += str(template.categ_id.code)
                    
                    template.barcode = str(code) + str(template.original_code)
                    template.original_barcode = template.barcode

                    # template.default_code = str(code) + str(template.original_code)
                    # template.original_barcode = template.default_code
            else:
                code = ""
               
                if template.brand_id:
                    code += str(template.brand_id.code)
                if template.factory_id:
                    code += str(template.factory_id.code)
                # if template.hscode_id:
                #     code += str(template.hscode_id.code)
                if template.categ_id:
                    code += str(template.categ_id.code)
                template.barcode = str(code) + str(template.original_code)
                # template.default_code = str(code) + str(template.original_code)

                template.original_barcode = template.barcode
                # template.original_barcode = template.default_code

            temp_barcode = template.original_barcode
            temp_id_barcode =  str(template.original_code)

            for varient in template.product_variant_ids:
                if varient.product_tmpl_id:
                    code = ""
                    # if varient.product_tmpl_id.factory_id:
                    #     code += str(varient.product_tmpl_id.factory_id.code)
                    # if varient.product_tmpl_id.brand_id:
                    #     code += str(varient.product_tmpl_id.brand_id.code)
                    if varient.product_tmpl_id.original_barcode:
                        code += str(varient.product_tmpl_id.original_barcode)
                    if varient.product_template_variant_value_ids:
                        for line in varient.product_template_variant_value_ids:
                            
                            code += str(line.product_attribute_value_id.code)
                    
                   
                    varient.barcode = code
                    # varient.default_code = temp_id_barcode
                    varient.product_tmpl_id.barcode = temp_barcode
                    # varient.default_code = temp_id_barcode

            
            
            



class Product(models.Model):
    _inherit = "product.product"

    barcode = fields.Char(
        'Barcode', copy=False, index='btree_not_null',
        help="International Article Number used for product identification.",readonly=True)
    
    # default_code = fields.Char(
    #     'Internal Reference', copy=False, index='btree_not_null',
    #     help="International Article Number used for product identification.",readonly=True)
    default_code = fields.Char(
        'Internal Reference', compute='_compute_default_code', store=True,
        help="International Article Number used for product identification.",readonly=True)
    
    
    @api.onchange('categ_id')
    @api.depends('categ_id')
    def _compute_default_code(self):
        for record in self:
            if record.categ_id and record.categ_id.code:
                record.default_code = record.categ_id.code+str(record.categ_id.product_count+1)
            elif record.categ_id and record.categ_id.code:
                record.default_code = record.categ_id.code
            else:
                record.default_code = None

 

    # @api.depends('barcode')
    # def _compute_barcode(self):
    #     # self.barcode = False
    #     for template in self:
    #         if template.barcode_check == False:
    #             if not template.barcode:
    #                 template.barcode = self.env['ir.sequence'].next_by_code('barcode.sequence')
    #                 template.barcode_check = True
    #                 template.original_barcode = template.barcode
    #             else:
    #                 template.barcode = template.barcode
    #         else:
    #             template.barcode = template.barcode
    #         temp_barcode = template.original_barcode
    #         for varient in template:
    #             # print("oooooooooooooooooooooooooooooooooooooooooooooooo",varient)
    #             if varient.product_tmpl_id:
    #                 print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",varient.product_tmpl_id.id)
    #                 code = ""
    #                 print("fffffffffffffffffffffffffffffffffffff",varient.product_tmpl_id.factory_id.name)
    #                 if varient.product_tmpl_id.factory_id:
    #                     code += str(varient.product_tmpl_id.factory_id.code)
    #                 if varient.product_tmpl_id.brand_id:
    #                     code += str(varient.product_tmpl_id.brand_id.code)
    #                     print("cccccccccccccccccccccccccccccccccccccc",code)
    #                 varient.barcode = code
    #                 varient.product_tmpl_id.barcode = temp_barcode







    @api.constrains('barcode')
    def _check_barcode_uniqueness(self):
        """ With GS1 nomenclature, products and packagings use the same pattern. Therefore, we need
        to ensure the uniqueness between products' barcodes and packagings' ones"""
        all_barcode = [b for b in self.mapped('barcode') if b]
        domain = [('barcode', 'in', all_barcode)]
        matched_products = self.sudo().search(domain, order='id')
        if len(matched_products) > len(all_barcode):  # It means that you find more than `self` -> there are duplicates
            products_by_barcode = defaultdict(list)
            for product in matched_products:
                products_by_barcode[product.barcode].append(product)

            duplicates_as_str = "\n".join(
                _("- Barcode \"%s\" already assigned to product(s): %s", barcode, ", ".join(p.display_name for p in products))
                for barcode, products in products_by_barcode.items() if len(products) > 1
            )
            # raise ValidationError(_("Barcode(s) already assigned:\n\n%s", duplicates_as_str))

        if self.env['product.packaging'].search(domain, order="id", limit=1):
            raise ValidationError(_("A packaging already uses the barcode"))

class ProductAttributes(models.Model):
    _inherit = "product.attribute.value"

    code = fields.Char("Code")

    	