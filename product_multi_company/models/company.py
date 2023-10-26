from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    company_id = fields.Many2one(
        string='Company',
        readonly=True,
    )

    # def init(self):
    #     super(ProductTemplate, self).init()
    #     # Make the company_id field invisible
    #     self.fields_get(['company_id'])['company_id']['invisible'] = True
