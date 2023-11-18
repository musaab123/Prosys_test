# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, _, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_employee_related(self):
        employee = self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
        if employee:
            return employee.id
        else:
            return False

    part_id = fields.Char('Partner ID',related='partner_id.partner_id',store=True)
    responsible_employee_id = fields.Many2one('hr.employee','Responsible Employee',default=_get_employee_related)
   
    from_city_id = fields.Many2one('res.country.state','From City')
    to_city_id = fields.Many2one('res.country.state','to City')
    distributer_name_id = fields.Char('Distributer Name')
    distributer_car_number_id = fields.Char('Distributer Car Number')
    shipping_company_name_id = fields.Char('Shipping Company Name')
    lading_number_id = fields.Char('Lading Number')

    shipping_port_id = fields.Char("Shipping Port" ,store=True)
    deliver_port_id = fields.Char("Delivery Port" ,store=True)
    policy_number_id = fields.Char("Policy Number" ,store=True)
     # shipping_port = fields.Char('Shipping Port')
    # deliver_port = fields.Char('Deliver Port')
    # policy_number = fields.Char('Policy Number')

    
    container_ids = fields.One2many('container.details','sale_id',string="Containers")

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['responsible_employee_id'] = self.responsible_employee_id.id
        invoice_vals['shipping_port_id'] = self.shipping_port_id
        invoice_vals['deliver_port_id'] = self.deliver_port_id
        invoice_vals['policy_number_id'] = self.policy_number_id
        invoice_vals['from_city_id'] = self.from_city_id.id
        invoice_vals['to_city_id'] = self.to_city_id.id
        invoice_vals['distributer_name_id'] = self.distributer_name_id
        invoice_vals['distributer_car_number_id'] = self.distributer_car_number_id
        invoice_vals['policy_number_id'] = self.policy_number_id
        invoice_vals['shipping_company_name_id'] = self.shipping_company_name_id
        invoice_vals['container_ids'] = [(6,0,self.container_ids.ids)]
        return invoice_vals




class Containers(models.Model):
    _name = 'container.details'
    _rec_name = 'container_number'

    sale_id = fields.Many2one('sale.order','Sale Order')
    purchase_id = fields.Many2one('purchase.order','Purchase Order')
    account_id = fields.Many2one('account.move','Accounts')
    container_number = fields.Char('Container Number')
    container_weight = fields.Char('Container weight')
    container_size = fields.Char('Container Size')
    cbm = fields.Char('CBM')




class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order','Sale Order')
    purchase_id = fields.Many2one('purchase.order','Purchase Order')
    account_id = fields.Many2one('account.move','Accounts')
    invoice_id = fields.Many2one('account.move','Invoice Number')
    # container_ids = fields.One2many('container.details','sale_id',string="Containers" , compute="_get_questions")
    container_ids = fields.One2many('container.details', 'sale_id', string="Containers", compute="_compute_container_ids")

   
    vendor_bill_number = fields.Char('Vendor Bill Number' , related='purchase_id.vendor_bill_number',store=True)
    shipping_port = fields.Char('Shipping Port' , related='purchase_id.shipping_port',store=True)
    deliver_port = fields.Char('Deliver Port' , related='purchase_id.deliver_port',store=True)
    policy_number = fields.Char('Policy Number' , related='purchase_id.policy_number',store=True)
    shipping_company_name = fields.Char('Shipping Company Name' , related='purchase_id.shipping_company_name',store=True)
    lading_number = fields.Char('Lading Number' , related='purchase_id.lading_number',store=True)
    distributer_name =fields.Char('Distributer Name' , related='purchase_id.distributer_name',store=True)
    distributer_car_number = fields.Char('Distributer Car Name' , related='purchase_id.distributer_car_number',store=True)
    from_city = fields.Many2one('res.country.state','From City', related='purchase_id.from_city',store=True)
    to_city = fields.Many2one('res.country.state','to City', related='purchase_id.to_city',store=True)



    # responsible_employee_id = fields.Many2one('hr.employee','Responsible Employee',default=_get_employee_related)








    from_city_id = fields.Many2one('res.country.state','From City' , related='sale_id.from_city_id',store=True)
    to_city_id = fields.Many2one('res.country.state','to City' , related='sale_id.to_city_id',store=True)
    distributer_name_id = fields.Char('Distributer Name' , related='sale_id.distributer_name_id',store=True)
    distributer_car_number_id = fields.Char('Distributer Car Number' , related='sale_id.distributer_car_number_id',store=True)
    shipping_company_name_id = fields.Char('Shipping Company Name' , related='sale_id.shipping_company_name_id',store=True)
    lading_number_id = fields.Char('Lading Number' , related='sale_id.lading_number_id',store=True)
    shipping_port_id = fields.Char("Shipping Port" , related='sale_id.shipping_port_id' ,store=True)
    deliver_port_id = fields.Char("Delivery Port" , related='sale_id.deliver_port_id' ,store=True)
    policy_number_id = fields.Char("Policy Number" , related='sale_id.policy_number_id' ,store=True)


    @api.depends('sale_id', 'purchase_id')
    def _compute_container_ids(self):
        for rec in self:
            if rec.sale_id:
                rec.container_ids = self.env['container.details'].search([('sale_id', '=', rec.sale_id.id)])
            elif rec.purchase_id:
                rec.container_ids = self.env['container.details'].search([('purchase_id', '=', rec.purchase_id.id)])
            else:
                rec.container_ids = False

    # def _get_questions(self):
    #     for rec in self:
    #         if rec.sale_id:
    #             rec.container_ids = self.env['container.details'].search([('sale_id','=',rec.sale_id.id)])
    #         if rec.purchase_id:
    #             rec.container_ids = self.env['container.details'].search([('purchase_id','=',rec.purchase_id.id)])

    # def _get_questions(self):
    #     for rec in self:
    #         self.container_ids = self.env['container.details'].search([('sale_id','=',self.sale_id.id)])




