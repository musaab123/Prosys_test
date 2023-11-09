from odoo import models, fields, api, tools

class SaleLines(models.Model):
    _inherit = 'res.partner'

    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')


class SaleLines(models.Model):
    _name = 'sale.lines'

    name = fields.Char(String="Sale Lins" ,translate=True)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sale_lines_id = fields.Many2one('sale.lines', string='Sale Lines')


class FieldServices(models.Model):
    _inherit = 'project.task'

    sale_lines_id = fields.Many2one('sale.lines', related='partner_id.sale_lines_id' ,string='Sale Lines')








   

