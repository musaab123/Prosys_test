""" Purchase Requisition model"""
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class PurchasePlan(models.Model):

    _name = 'purchase.plan'

    _description = 'Purchase Plan'
    _inherit = "mail.thread", "mail.activity.mixin"


    name = fields.Char('Number', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    description = fields.Char('Name', required=True, copy=False, readonly=True,)

    date = fields.Date(string="Date",
                                   default=lambda self: fields.Date.today(),
                                   help='Date of PLan')
    state=fields.Selection([('new','New'),('running','Running'),('cancel', 'Cancelled'),('lock','Locked')],"Status",default='new', copy=False, tracking=True)

    purchase_plan_planned_ids=fields.One2many("purchase.plan.planned","purchase_plan_id","Purchase Plan")
    purchase_plan_actual_ids=fields.One2many("purchase.plan.actual","purchase_plan_id","Purchase Plan")
    purchase_plan_diff_ids=fields.One2many("purchase.plan.diff","purchase_plan_id","Purchase Plan")
    purchase_plan_perentage_ids=fields.One2many("purchase.plan.percentage","purchase_plan_id","Purchase Plan")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 help='Company')
    purchase_count = fields.Integer(string='Purchase Count',
                                    help='Purchase Count',
                                    compute='_compute_purchase_count')






    @api.model
    def create(self, vals):
        """generate purchase plan sequence"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'purchase.order.plan') or 'New'
        result = super(PurchasePlan, self).create(vals)
        return result


    def _compute_purchase_count(self):
        self.purchase_count = self.env['purchase.order'].search_count([
            ('purchase_plan_ids', 'in', self.ids)])



    def get_purchase_order(self):
        """purchase order smart button view"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('purchase_plan_ids', 'in', self.ids)],
        }



    def unlink(self):
        for rec in self:
            if not rec.state == 'new':
                raise UserError("Only new records can be deleted!")


    # @api.onchange('purchase_plan_planned_ids')
    def action_running(self):
        for rec in self:
            pland_line=[]
            line_ids=[]

            for line in rec.purchase_plan_planned_ids:
                pland_line.append(line)


            for a_line in pland_line:

                lines = {'purchase_plan_id': a_line.purchase_plan_id.id,
                    'product_category_type': a_line.product_category_type,
                    'product_id': a_line.product_id.id,
                    'category_id': a_line.category_id.id,
                }

                line_ids.append(lines)



        actual_create_obj = self.env['purchase.plan.actual'].create(line_ids)
        diff_create_obj = self.env['purchase.plan.diff'].create(line_ids)
        per_create_obj = self.env['purchase.plan.percentage'].create(line_ids)

        self.state = 'running'





    def action_set_to_draft(self):
        self.state = 'new'



    def action_cancel(self):
        self.state = 'cancel'

    def action_lock(self):
        self.state = 'lock'






class PurchasePlanPlanned(models.Model):

    _name = 'purchase.plan.planned'

    _description = 'Purchase Plan planned'

    name=fields.Char("Name")
    purchase_plan_id=fields.Many2one("purchase.plan","Purchase Plan")


    state = fields.Selection(string='State',
                             related='purchase_plan_id.state')
    product_category_type = fields.Selection(
        string='Product/Category',
        selection=[
            ('category', 'Category'),
            ('product', 'Product'),
        ], help='Product/Category')
    product_id = fields.Many2one('product.product',
                                 help='Product')

    category_id = fields.Many2one('product.category',
                                 help='Category')

    product_qty = fields.Float(string='Quantity', help='Quantity')
    unit_cost = fields.Float(string='Unit Cost', help='UC')
    amount = fields.Float(string='Amount', help='amount',readonly=True,store=True,compute="get_amount")

    @api.depends('product_qty','unit_cost')
    def get_amount(self):
        amount=0.0
        for rec in self:
            amount=rec.product_qty*rec.unit_cost
            rec.amount=amount



class PurchasePlanActual(models.Model):

    _name = 'purchase.plan.actual'

    _description = 'Purchase Plan Actual'

    name=fields.Char("Name")
    purchase_plan_id=fields.Many2one("purchase.plan","Purchase Plan")



    state = fields.Selection(string='State',
                             related='purchase_plan_id.state')
    product_category_type = fields.Selection(
        string='Product/Category',
        selection=[
            ('category', 'Category'),
            ('product', 'Product'),
        ], help='Product/Category')
    product_id = fields.Many2one('product.product', 
                                 help='Product')

    category_id = fields.Many2one('product.category',
                                 help='Category')

    product_qty = fields.Float(string='Quantity', help='Quantity')
    unit_cost = fields.Float(string='Unit Cost', help='UC',compute="get_amount")
    amount = fields.Float(string='Amount', help='amount',readonly=True,store=True,compute="get_amount")
    flag=fields.Boolean("")

    # def get_amount(self):
    #     amount=0.0
    #     total_cost=0.0
    #     for rec in self:
            
    #         order_id=self.env['purchase.order.line'].search([('order_id.purchase_plan_ids','in',self.purchase_plan_id.ids),('order_id.state','=','purchase')])
            
    #         x = len(order_id)

    #         for line in order_id:

    #             unit_cost=0.0
    #             if rec.product_category_type=='product':

    #                 if line.product_id==rec.product_id:
    #                     if x!=0.0:
    #                         rec.unit_cost+=line.price_unit/x 
    #             else:
    #                 if line.product_id.categ_id


                
    #         amount=rec.product_qty*rec.unit_cost
    #         rec.amount=amount



    @api.depends('product_qty','unit_cost')
    def get_amount(self):
        amount=0.0
        total_cost=0.0
        for rec in self:
            
            order_id=self.env['purchase.order.line'].search([('order_id.purchase_plan_ids','in',self.purchase_plan_id.ids),('product_id','=',rec.product_id.id),('order_id.state','=','purchase')])
            
            categ_order_id=self.env['purchase.order.line'].search([('order_id.purchase_plan_ids','in',self.purchase_plan_id.ids),('product_id.categ_id','=',rec.category_id.id),('order_id.state','=','purchase')])
            x = len(order_id)
            y = len(categ_order_id)


            for line in order_id:

                unit_cost=0.0

                if line.product_id==rec.product_id and rec.product_category_type=='product':
                    if x!=0.0:
                        rec.unit_cost+=line.price_unit/x 
                        line.flag=True


            for line in categ_order_id:

                unit_cost=0.0

                if line.product_id.categ_id==rec.category_id and rec.product_category_type=='category':
                    if y!=0.0 and line.flag==False:
                        rec.unit_cost+=line.price_unit/y



                
            amount=rec.product_qty*rec.unit_cost
            rec.amount=amount




class PurchasePlanDiff(models.Model):

    _name = 'purchase.plan.diff'

    _description = 'Purchase Plan Diff'

    name=fields.Char("Name")
    purchase_plan_id=fields.Many2one("purchase.plan","Purchase Plan")

    state = fields.Selection(string='State',
                             related='purchase_plan_id.state')
    product_category_type = fields.Selection(
        string='Product/Category',
        selection=[
            ('category', 'Category'),
            ('product', 'Product'),
        ], help='Product/Category')
    product_id = fields.Many2one('product.product',
                                 help='Product')

    category_id = fields.Many2one('product.category', 
                                 help='Category')

    product_qty = fields.Float(string='Quantity', help='Quantity',compute="get_amount")
    unit_cost = fields.Float(string='Unit Cost', help='UC',compute="get_amount")
    amount = fields.Float(string='Amount', help='amount',readonly=True,store=True,compute="get_amount")


    @api.depends('product_qty','unit_cost')
    def get_amount(self):
        amount=0.0
        total_cost=0.0
        for rec in self:
            purchase_plan_id=self.env['purchase.plan.planned'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('product_id','=',rec.product_id.id)])
            purchase_actual_id=self.env['purchase.plan.actual'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('product_id','=',rec.product_id.id)])

            purchase_plan_c_id=self.env['purchase.plan.planned'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('category_id','=',rec.category_id.id)])
            purchase_actual_c_id=self.env['purchase.plan.actual'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('category_id','=',rec.category_id.id)])



            for line in purchase_plan_id:
                for line2 in purchase_actual_id:
                    if rec.product_category_type=='product':
                        if line.product_id==line2.product_id :
                            rec.product_qty=line.product_qty-line2.product_qty
                            rec.unit_cost=line.unit_cost-line2.unit_cost
                            rec.amount=line.amount-line2.amount


            for line_c in purchase_plan_c_id:
                for line_ca in purchase_actual_c_id:
                    if rec.product_category_type=='category':
                        if line_c.category_id==line_ca.category_id :
                            rec.product_qty=line_c.product_qty-line_ca.product_qty
                            rec.unit_cost=line_c.unit_cost-line_ca.unit_cost
                            rec.amount=line_c.amount-line_ca.amount


                # if line.product_id.categ_id==rec.category_id and rec.product_category_type=='category':
                #     if y!=0.0 and line.flag==False:
                #         rec.unit_cost+=line.price_unit/y







class PurchasePlanPercentage(models.Model):

    _name = 'purchase.plan.percentage'

    _description = 'Purchase Plan percentage'

    name=fields.Char("Name")
    purchase_plan_id=fields.Many2one("purchase.plan","Purchase Plan")


    state = fields.Selection(string='State',
                             related='purchase_plan_id.state')
    product_category_type = fields.Selection(
        string='Product/Category',
        selection=[
            ('category', 'Category'),
            ('product', 'Product'),
        ], help='Product/Category')
    product_id = fields.Many2one('product.product',
                                 help='Product')

    category_id = fields.Many2one('product.category',
                                 help='Category')

    product_qty = fields.Float(string='Quantity', help='Quantity',compute="get_amount")
    unit_cost = fields.Float(string='Unit Cost', help='UC',compute="get_amount")
    amount = fields.Float(string='Amount', help='amount',readonly=True,store=True,compute="get_amount")


    @api.depends('product_qty','unit_cost')
    def get_amount(self):
        amount=0.0
        total_cost=0.0
        for rec in self:
            purchase_plan_id=self.env['purchase.plan.planned'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('product_id','=',rec.product_id.id)])
            purchase_diff_id=self.env['purchase.plan.diff'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('product_id','=',rec.product_id.id)])

            purchase_plan_c_id=self.env['purchase.plan.planned'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('category_id','=',rec.category_id.id)])
            purchase_diff_c_id=self.env['purchase.plan.diff'].search([('purchase_plan_id','=',rec.purchase_plan_id.id),('category_id','=',rec.category_id.id)])



            for line in purchase_plan_id:
                for line2 in purchase_diff_id:
                    if rec.product_category_type=='product':
                        if line.product_id==line2.product_id :
                            rec.product_qty=(line2.product_qty/line.product_qty)*100
                            rec.unit_cost=(line2.unit_cost/line.unit_cost)*100
                            rec.amount=(line2.amount/line.amount)*100


            for line_c in purchase_plan_c_id:
                for line_ca in purchase_diff_c_id:
                    if rec.product_category_type=='category':
                        if line_c.category_id==line_ca.category_id :
                            rec.product_qty=(line_ca.product_qty/line_c.product_qty)*100
                            rec.unit_cost=(line_ca.unit_cost/line_c.unit_cost)*100
                            rec.amount=(line_ca.amount/line_c.amount)*100


                # if line.product_id.categ_id==rec.category_id and rec.product_category_type=='category':
                #     if y!=0.0 and line.flag==False:
                #         rec.unit_cost+=line.price_unit/y



                
            # amount=(rec.product_qty*rec.unit_cost)
            # rec.amount=amount









