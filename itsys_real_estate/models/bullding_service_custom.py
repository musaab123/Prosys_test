from odoo import fields, models, api, _

class Building(models.Model):
    _inherit = 'building'

    license_code = fields.Char('License Code')
    license_date = fields.Date('License Date')
    registration_date_on_recorder_of_deeds = fields.Date('Registration Date on Recorder of deeds')
    license_authorization = fields.Char('License Authorization')

    units_count = fields.Integer(compute='get_units_count', string='Units Count')

    def get_units_count(self):
        units_obj = self.env['product.template']
        for unit in self:
            units_ids = units_obj.search([('building_id', '=', self.id)])
            unit.units_count = len(units_ids)

    def view_build_units(self):
        unit_obj = self.env['product.template']
        units_ids = unit_obj.search([('building_id', '=', self.id)])
        units=[]
        for obj in units_ids: units.append(obj.id)
        return {
            'name': _('Units'),
            'domain': [('id', 'in', units)],
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'product.template',
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'view_id': False,
            'target':'current',
        }

class ProductTemplate(models.Model):
    _inherit = ['product.template']

    put_on_hold = fields.Boolean('Active', help="If the active field is set to False, it will allow you set unit status to on hold.",default=True)
    is_build_service = False
    state = fields.Selection([('free', 'Available'),
                              ('reserved', 'Booked'),
                              ('on_lease', 'Leased'),
                              ('sold', 'Sold'),
                              ('blocked', 'Blocked'),
                              ('on_hold', 'On Hold'),
                              ], 'State', default='free')

    license_code = fields.Char('License Code')
    license_date = fields.Date('License Date')
    registration_date_on_recorder_of_deeds = fields.Date('Registration Date on Recorder of deeds')
    license_authorization = fields.Char('License Authorization')

    property_service_ids = fields.Many2many('building.service', string="Property Services")
    air_conditions = fields.Selection([('central', 'Central'),
                              ('split', 'Split'),
                              ('window', 'Window'),
                              ], default='central', string="Air Condition Type")

    units_contract_count = fields.Integer(compute='get_units_contracts', string='Units Contract')

    def get_units_contracts(self):
        contract_obj = self.env['rental.contract']
        for contract in self:
            contract_objs = contract_obj.search([('building_unit', '=', self.id)])
            contract.units_contract_count = len(contract_objs)

    def view_units_contracts(self):
        contract_obj = self.env['rental.contract']
        contract_objs = contract_obj.search([('building_unit', '=', self.id)])
        contracts=[]
        for obj in contract_objs: contracts.append(obj.id)
        return {
            'name': _('Contracts'),
            'domain': [('id', 'in', contracts)],
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'rental.contract',
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'view_id': False,
            'target':'current',
        }

    @api.onchange('put_on_hold')
    def check_put_on_hold(self):
        if self.put_on_hold == False:
            self.state = 'on_hold'

        if self.put_on_hold == True:
            self.state = 'free'

class BuildingServices(models.Model):
    _name = 'building.service'

    name = fields.Char('Service Name', required=True)
    unit_price = fields.Float('Unit Price')
    active = fields.Boolean ('Active',
                             help="If the active field is set to False, it will allow you to hide the service without removing it.",default=True)
    product_templ_id = fields.Many2one('product.template')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Service name must be unique.'),
    ]

    _access = {
        'write': True,  # Allow editing records
        'create': True,  # Allow creating new records
    }


    @api.model_create_multi
    def create(self, vals_list):
        res = super(BuildingServices, self).create(vals_list)
        product_category = self.env['product.category'].search([('name', '=', 'Expenses')])
        product_template = self.env['product.template']
        print("list price", res.unit_price)
        new_product = product_template.create(
            {
                'name': res.name,
                'sale_ok': True,
                'purchase_ok': True,
                'can_be_expensed': True,
                'detailed_type': 'service',
                'type': 'service',
                'invoice_policy': 'order',
                'list_price': res.unit_price,
                'standard_price': res.unit_price,
                'categ_id': product_category.id,
                'sequence': 1,
                'uom_id': 1,
                'uom_po_id': 1,
                'active': True,
            }
        )

        # update service
        update_service = res.write(
            {
                'product_templ_id': new_product.id,
            }
        )

        return res

    def write(self, vals):
        res = super(BuildingServices, self).write(vals)
        product_template = self.env['product.template'].search([('id', '=', self.product_templ_id.id)])
        for rec in self:
            update_id = product_template.write(
                {
                    'name': rec.name,
                    'list_price': rec.unit_price,
                }
            )

        return res


    @api.onchange('active')
    def check_active(self):
        get_product_id = self.env['product.template'].search([('id', '=', self.product_templ_id.id)])
        if self.active == False:
            update_product_id = get_product_id.write(
                {
                    'active': False,
                }
            )
        elif self.active == True:
            update_product_id = get_product_id.write(
                {
                    'active': True,
                }
            )

class UnitReservation(models.Model):
    _inherit = 'unit.reservation'

    def action_confirm(self):
        res =  super(UnitReservation, self).action_confirm()
        unit_id = self.env['product.template'].search([('id', '=', self.building_unit.id)])
        unit_id.write(
            {
                'value_deposit': self.deposit,
            }
        )

        return res










