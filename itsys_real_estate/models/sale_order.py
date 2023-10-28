from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    rent_contract_id = fields.Many2one('rental.contract', string="Contract")
    building_units = fields.Many2one('product.template', string='Building Units', related='rent_contract_id.building_unit')
    owner_id = fields.Many2one('res.partner', string="Owner", related='building_units.building_id.partner_id')
    statement = fields.Text('Statement', readonly=True, compute='_set_statement')

    def _set_statement(self):
        from_date = ''
        to_date = ''
        for rec in self.rent_contract_id:
            from_date = rec.date_from
            to_date = rec.date_to

        self.statement = 'Install period from '+" "+str(from_date)+" to date"+" "+str(to_date)

    @api.onchange('partner_id')
    def _get_contract_domain(self):
        if self.partner_id:
            return {'domain': {'rent_contract_id': [('partner_id', '=', self.partner_id.id)]}}