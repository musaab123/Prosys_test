from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    def action_update_product_company(self):
        print("Default Company IDs:", self.ids)
        list_ids = []
        for rec in self:
            list_ids.append(rec.id)
        return {
            'name': _("Set Company"),
            'type': 'ir.actions.act_window',
            'res_model': 'change.companies.wizard',
            'view_mode': 'form,tree',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_company_ids': self.ids},
        }



class ChangeCompanysWizard(models.TransientModel):
    _name = 'change.companies.wizard'

    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
    )



    def set_companies(self):
        product_templates = self.env['product.template'].browse(self.env.context.get('default_company_ids'))
        product_templates.write({'company_ids': [(6, 0, self.company_ids.ids)]})