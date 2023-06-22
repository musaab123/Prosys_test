# -*- coding: utf-8 -*-
from odoo import api, fields, models

class building_unit_inherit(models.Model):
    _inherit = ['product.template']
    unit_location = fields.Selection([('inside','Inside'),
                               ('outside','Outside'),
                               ], 'Unit Location',default='outside' )


    ac_type = fields.Selection([('central','Central'),
                               ('window','Window'),
                               ('aspelt','Aspelt'),

                               ], 'AC Type',default='central' )

    is_furnished = fields.Boolean( string ='Furnished')
    is_patio = fields.Boolean( string ='Patio')

    is_kitchen_cupboard = fields.Boolean( string ='kitchen cupboard')
    electricity_meter_number = fields.Char( string ='Electricity meter number')
    current_meter_reading= fields.Char( string='Current meter reading')
    gas_meter_number = fields.Char( string='Gas meter number')
    current_meter_reading_gas = fields.Char( string='Current meter reading')
    water_meter_number = fields.Char( string ='Water meter number')
    current_meter_reading_water = fields.Char( string='Current water meter reading')

    unit_number= fields.Char(string='Unit Number')
    commercial_activities = fields.Char( string="commercial activities")

    clean = fields.Boolean( string ='Cleaning')
    saft = fields.Boolean( string ='Safty')
    parking = fields.Boolean( string ='Parking')
    other = fields.Boolean( string ='Other')
    service_fees = fields.Integer(string="General service fees")
    value_deposit = fields.Integer(string="deposit Value")
    finishing_unit= fields.Selection([('scratchy','Scratchy'), ('unscratchy','Unscratchy'), ], 'Finishing')
    height = fields.Char(string=" Height")
    width = fields.Char(string=" Width")
    front = fields.Boolean( string ='Front')
    side = fields.Boolean( string ='Side')
    internal = fields.Boolean( string ='Internal')
    ac_number = fields.Char(string="AC Number")
   

class RealAccess(models.Model):
    _name = "real.access"
    _description = "Real Access"


    qui = fields.Char('Access Right', translate=True)
    is_yes= fields.Boolean ('Yes')
    is_no= fields.Boolean ('No')
    contract_id = fields.Many2one('rental.contract')

class MutualObligation(models.Model):
    _name = "mutual.obligations"
    _description = "mutual obligations"


    commitment = fields.Char('Commitment', translate=True)
    tenant_one = fields.Char(String='Tenant')
    lessor_one = fields.Char(String = 'Lessor')
    contract_obj_id = fields.Many2one('rental.contract' )



class AdditionalObligations (models.Model):
    _name = "test.access"
    _description = "test access"


    commitment_qustion = fields.Char('Ask',translate=True)
    tenant_answer = fields.Char(String ='Tenant')
    lessor_answer = fields.Char( String = 'Lessor')
    contract_com_id = fields.Many2one('rental.contract')


class rental_inherit(models.Model):
    _inherit = ['rental.contract']
    contract_time = fields.Integer(string="Contract Time")
    is_creation = fields.Boolean( string ='Creation Auto')
    is_create = fields.Boolean(string="is create")

    contract_type = fields.Selection([('commercial', 'Commercial'), ('residential', 'residential'),
                                             ],
                                           string='Contract Type', required=True,
                                           tracking=True)

    admin_qustion = fields.One2many('real.access', 'contract_id', compute="_get_questions", string=' ')
    mutual_obligation = fields.One2many('mutual.obligations', 'contract_obj_id', compute="_get_questions_test", string=' ')
    mutual_access = fields.One2many('test.access', 'contract_com_id', compute="_get_questions_test2",  string=' ')


    def _get_questions(self):
        for rec in self:
            rec.admin_qustion = self.env['real.access'].search([])
    
    def _get_questions_test(self):
        self.mutual_obligation = self.env['mutual.obligations'].search([])

    def _get_questions_test2(self):
        self.mutual_access = self.env['test.access'].search([])

 
    # @api.onchange()
    # def action_calculate(self):
    #     if not self.admin_qustion:
    #         self.admin_qustion = [
    #             [ 0, 0, { "qui": x.qui }] for x in self.env['real.access'].search([])
    #         ]


    # @api.onchange()
    #  def action_calculate_test(self):
    #     if not self.mutual_obligation:
    #         self.mutual_obligation = [
    #             [ 0, 0, { "commitment": x.commitment }] for x in self.env['mutual.obligations'].search([])
    #         ]


    # @api.onchange()
    # def action_access_test(self):
    #     if not self.mutual_access:
    #         self.mutual_access = [
    #             [ 0, 0, { "commitment_qustion": x.commitment_qustion }] for x in self.env['test.access'].search([])
    #         ]




    # @api.model
    # def create(self ,vals):
    #     if self.is_create ==True:
    #         vals['admin_qustion'] = [
    #                 [ 0, 0, { "qui": x.qui }] for x in self.env['real.access'].search([])
    #             ]

    #         vals['mutual_obligation']= [
    #             [ 0, 0, {"commitment": x.commitment }] for x in self.env['mutual.obligations'].search([])
    #         ]

    #         vals['mutual_access'] = [
    #             [ 0, 0, {"commitment_qustion": x.commitment_qustion }] for x in self.env['test.access'].search([])
    #         ]
    #     print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",vals)
    #     return super(rental_inherit,self).create(vals)
    

