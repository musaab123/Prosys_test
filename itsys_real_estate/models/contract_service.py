from odoo import fields, models, api, _


class ContractService(models.Model):
    _name = 'contract.service'

    property_service_ids = fields.Many2many('building.service', string="Property Services", required=True)
    service_type = fields.Selection([('income', 'Income'),
                                       ('expense', 'Expense'),
                                       ], default='income', string="Service Type", required=True)
    rent_contract_id = fields.Many2one('rental.contract', string='Contract', readonly=True)
    tenant_id = fields.Many2one('res.partner', string='Tenant', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    amount = fields.Float('Amount', required=True)
    tax_amount = fields.Float('Tax Amount', readonly=True)
    from_date = fields.Date('From Date', readonly=True)
    to_date = fields.Date('To Date', readonly=True)
    building_units = fields.Many2one('product.template', string='Building Units')
    state = fields.Selection([('draft', 'Draft'),
                                       ('confirmed', 'Confirmed'),
                                       ], default='draft', string="State")
    with_tax = fields.Boolean ('Taxes' ,default=False)
    ref = fields.Text('Ref')
    sale_order_id = fields.Many2one('sale.order', 'sale_order_id')
    expense_id = fields.Many2one('hr.expense', 'expense_id')
    expense_sheet_id = fields.Many2one('hr.expense.sheet', 'expense_sheet_id')

    def create_sale_order(self):
        vals = {
            'partner_id': self.rent_contract_id.partner_id.id,
            'rent_contract_id': self.rent_contract_id.id,
            'building_units': self.rent_contract_id.building_unit.id,
            'user_id': self.env.uid,
            'pricelist_id': self.rent_contract_id.partner_id.property_product_pricelist.id,
        }
        new_sale_order_id = self.env['sale.order'].create(vals)
        for rec in self.property_service_ids:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec.product_templ_id.id)])
            if not self.with_tax:
                new_sale_order_id.write({
                    'order_line': [
                        (0, 0, {
                            'order_id': new_sale_order_id.id,
                            'product_id': product_id.id,
                            'name': product_id.product_tmpl_id.name,
                            'product_uom_qty': 1,
                            'display_type': False,
                            'tax_id': False,
                        })
                    ]
                })

            if self.with_tax:
                new_sale_order_id.write({
                    'order_line': [
                        (0, 0, {
                            'order_id': new_sale_order_id.id,
                            'product_id': product_id.id,
                            'name': product_id.product_tmpl_id.name,
                            'product_uom_qty': 1,
                            'display_type': False,
                        })
                    ]
                })

        new_sale_order_id.action_confirm()
        so_id = self.write(
            {
                'sale_order_id': new_sale_order_id.id,
                'state': 'confirmed',
            }
        )

    def create_expense(self):
        expense_id = []
        for rec in self.property_service_ids:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec.product_templ_id.id)])
            employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
            vals = {}
            if not self.with_tax:
                vals = {
                    'product_id': product_id.id,
                    'employee_id': employee_id.id,
                    'paid_by_partner': 'paid_by_partner',
                    'partner_id': self.rent_contract_id.partner_id.id,
                    'rent_contract_id': self.rent_contract_id.id,
                    'building_units': self.rent_contract_id.building_unit.id,
                    'tax_ids': False,
                }

            if self.with_tax:
                vals = {
                    'product_id': product_id.id,
                    'employee_id': employee_id.id,
                    'paid_by_partner': 'paid_by_partner',
                    'partner_id': self.rent_contract_id.partner_id.id,
                    'rent_contract_id': self.rent_contract_id.id,
                    'building_units': self.rent_contract_id.building_unit.id,
                }

            new_hr_expense_id = self.env['hr.expense'].create(vals)
            self.write(
                {
                    'expense_id': new_hr_expense_id.id,
                }
            )
            expense_id.append(new_hr_expense_id.id)

        new_expenses_id = self.env['hr.expense'].search([('id', 'in', expense_id)], order='id asc')
        sheet_description = ''

        for rec in new_expenses_id:
            sheet_description += rec.name +" "

        expense = self.env['hr.expense'].search([('id', 'in', expense_id)], limit=1)
        sheet_vals = {
            'name': sheet_description,
            'employee_id': expense.employee_id.id,
            'partner_id': expense.partner_id.id,
            'rent_contract_id': expense.rent_contract_id.id,
            'building_units': expense.rent_contract_id.building_unit.id,
        }
        # update_sheet_id
        new_hr_expense_sheet_id = self.env['hr.expense.sheet'].create(sheet_vals)
        for rec in new_expenses_id:
            rec.write(
                {
                    'sheet_id': new_hr_expense_sheet_id.id,
                }
            )

        # update expense_sheet_id and state
        self.write(
            {
                'expense_sheet_id': new_hr_expense_sheet_id.id,
                'state': 'confirmed',
            }
        )

        # update again
        new_hr_expense_sheet_id.write(sheet_vals)
        # submit sheet
        new_hr_expense_sheet_id.action_submit_sheet()
        new_hr_expense_sheet_id.approve_expense_sheets()
        new_hr_expense_sheet_id.action_sheet_move_create()



    @api.onchange('property_service_ids', 'amount', 'service_type')
    def on_change_fields(self):
        if self.property_service_ids and self.service_type == 'expense':
            total_amount = 0
            for rec in self.property_service_ids:
                total_amount += rec.unit_price
            self.write(
                {
                    'amount': total_amount,
                }
            )
        elif self.property_service_ids and self.service_type == 'income':
            total_amount = 0
            for rec in self.property_service_ids:
                total_amount += rec.unit_price
            self.write(
                {
                    'amount': total_amount,
                }
            )

        if self.amount and self.amount and self.service_type == 'expense':
            self.write(
                {
                    'amount': self.amount * -1,
                }
            )

    @api.onchange('service_type')
    def check_service_type(self):
        if self.property_service_ids or self.service_type:
            self.write(
                {
                    'tenant_id': self.rent_contract_id.partner_id.id,
                    'analytic_account_id': self.rent_contract_id.account_analytic_id.id,
                    'from_date': self.rent_contract_id.date_from,
                    'to_date': self.rent_contract_id.date_to,
                    'building_units': self.rent_contract_id.building_unit.id,
                }
            )

    def view_sale_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'domain': [('id', '=', self.sale_order_id.id)],
            'view_mode': 'tree,form',
            'view_type': 'tree,form',
            'context': {'create': False},
        }

    def view_expense(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expenses',
            'res_model': 'hr.expense.sheet',
            'domain': [('id', '=', self.expense_sheet_id.id)],
            'view_mode': 'tree,form',
            'view_type': 'tree,form',
            'context': {'create': False},
        }

class RentalContract(models.Model):
    _inherit = 'rental.contract'

    property_service_ids = fields.Many2many('building.service', string="Property Services")

    contract_service_ids = fields.One2many('contract.service', 'rent_contract_id', string='service')