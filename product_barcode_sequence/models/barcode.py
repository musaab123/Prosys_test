from odoo import models, fields, api,_, tools

from collections import defaultdict


class ProductTemplate(models.Model):
    _inherit = "product.template"


    barcode = fields.Char('Barcode', compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode',readonly=True)
    default_code = fields.Char('Internal Reference' ,compute='_compute_defult_code',readonly=True)

    # cat_barcode = fields.Char('Catogery',compute='_compute_cat_barcode', store=True,readonly=True)

    barcode_check = fields.Boolean('Barcode Check',default=False)
    original_barcode = fields.Char('Barcode')
    original_code = fields.Char('code')
    vendor_reference_number = fields.Char(string="Vendor Reference Number")

    cat_barcode = fields.Char(
        'Catogery Code', compute='_compute_default_code_test', store=True,
        help="International Article Number used for product identification.",readonly=True)
    
    
    @api.onchange('categ_id')
    @api.depends('categ_id')
    def _compute_default_code_test(self):
        for record in self:
            if record.categ_id and record.categ_id.code:
                record.cat_barcode = record.categ_id.code+str(record.categ_id.product_count+1)
            elif record.categ_id and record.categ_id.code:
                record.cat_barcode = record.categ_id.code
            else:
                record.cat_barcode = None


    @api.depends('product_variant_ids.barcode')
    def _compute_barcode(self):
        # self.barcode = False
        for template in self:
            if template.barcode_check == False:
                code = ""

                if not template.barcode:
                    if template.brand_id:
                        code += str(template.brand_id.code)
                        
                    if template.factory_id:
                        code += str(template.factory_id.code)
                    
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
                    # if template.categ_id:
                    #     code += str(template.categ_id.code)
                    
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
                # if template.categ_id:
                #     code += str(template.categ_id.code)
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


    @api.depends('product_variant_ids.default_code')
    def _compute_defult_code(self):
        # self.barcode = False
        for template in self:
            if template.barcode_check == False:
                code = ""

                if not template.barcode:
                    if template.brand_id:
                        code += str(template.brand_id.code)
                        
                    
                    
                    o_code = self.env['ir.sequence'].next_by_code('barcode.sequence')
                    template.default_code = str(code) + str(o_code)

                    template.barcode_check = True
                    template.original_code = o_code
                    # template.original_barcode = template.barcode
                    template.original_barcode = template.default_code
                else:
                   
                    if template.brand_id:
                        code += str(template.brand_id.code)
                   

                    template.default_code = str(code) + str(template.original_code)
                    template.original_barcode = template.default_code
            else:
                code = ""
               
                if template.brand_id:
                    code += str(template.brand_id.code)
               
                template.default_code = str(code) + str(template.original_code)

                # template.original_barcode = template.barcode
                template.original_barcode = template.default_code

            temp_barcode = template.original_barcode
            temp_id_barcode =  str(template.original_code)

            for varient in template.product_variant_ids:
                if varient.product_tmpl_id:
                    code = ""
                   
                    if varient.product_tmpl_id.original_barcode:
                        code += str(varient.product_tmpl_id.original_barcode)
                    if varient.product_template_variant_value_ids:
                        for line in varient.product_template_variant_value_ids:
                            
                            code += str(line.product_attribute_value_id.code)
                    
                   
                    # varient.barcode = code
                    varient.default_code = temp_id_barcode
                    # varient.product_tmpl_id.barcode = temp_barcode
                    varient.default_code = temp_id_barcode


    @api.depends('product_variant_ids.cat_barcode')
    def _compute_cat_barcode(self):
        # self.barcode = False
        for template in self:
            if template.barcode_check == False:
                code = ""

                if not template.barcode:
                    if template.categ_id:
                        code += str(template.categ_id.code)
                        
                    
                    
                    # o_code = self.env['ir.sequence'].next_by_code('barcode.sequence')
                    template.cat_barcode = str(code) 

                    template.barcode_check = True
                    # template.original_code = o_code
                    # template.original_barcode = template.barcode
                    template.original_barcode = template.cat_barcode
                else:
                   
                    if template.categ_id:
                        code += str(template.categ_id.code)
                   

                    template.cat_barcode = str(code) 
                    template.original_barcode = template.cat_barcode
            else:
                code = ""
               
                if template.categ_id:
                        code += str(template.categ_id.code)
               
                template.cat_barcode = str(code) 

                # template.original_barcode = template.barcode
                template.original_barcode = template.cat_barcode

            temp_barcode = template.original_barcode
            temp_id_barcode =  str(template.original_code)

            for varient in template.product_variant_ids:
                if varient.product_tmpl_id:
                    code = ""
                   
                    if varient.product_tmpl_id.original_barcode:
                        code += str(varient.product_tmpl_id.original_barcode)
                    if varient.product_template_variant_value_ids:
                        for line in varient.product_template_variant_value_ids:
                            
                            code += str(line.product_attribute_value_id.code)
                    
                   
                    # varient.barcode = code
                    varient.cat_barcode = temp_id_barcode
                    # varient.product_tmpl_id.barcode = temp_barcode
                    varient.cat_barcode = temp_id_barcode



   




            
            
            



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

    cat_barcode = fields.Char(
        'Internal Reference', compute='_compute_default_code_test', store=True,
        help="International Article Number used for product identification.",readonly=True)
    
    
    @api.onchange('categ_id')
    @api.depends('categ_id')
    def _compute_default_code_test(self):
        for record in self:
            if record.categ_id and record.categ_id.code:
                record.cat_barcode = record.categ_id.code+str(record.categ_id.product_count+1)
            elif record.categ_id and record.categ_id.code:
                record.cat_barcode = record.categ_id.code
            else:
                record.cat_barcode = None



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

    	