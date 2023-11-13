# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SetuCustomerRating(models.Model):
    _name = 'setu.customer.rating'
    _description = 'Customer Rating'
    _rec_name = 'rating'

    rating = fields.Char(string="Rating", required=True)

    image = fields.Image(string="Image")

    from_score = fields.Integer(string="From Score", required=True)
    to_score = fields.Integer(string="To Score", required=True)

    total_customers_ratio = fields.Float(string="Customers Ratio", compute='_calculate_ratio')
    total_customers = fields.Integer(string="Total Customers", compute='_calculate_ratio')
    total_orders_ratio = fields.Float(string="Total Orders Ratio", compute='_calculate_ratio')
    total_orders = fields.Integer(string="Total Orders", compute='_calculate_ratio')
    total_revenue_ratio = fields.Float(string="Revenue Ratio", compute='_calculate_ratio')
    total_revenue = fields.Monetary(string="Total Revenue", compute='_calculate_ratio',
                                    currency_field='company_currency')

    crc_id = fields.Many2one('setu.customer.rating.company', string="Customer Rating Company", ondelete='cascade')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.get_company())
    company_currency = fields.Many2one('res.currency', compute='_compute_company_currency')

    @api.constrains('from_score', 'to_score', 'rating')
    def validations(self):
        for line in self:
            if line.to_score > 100:
                raise ValidationError(_('To Score cannot be exceeded 100.'))
            rules = line.sudo().search([('company_id', '=', line.company_id.id)])
            if rules.filtered(
                    lambda rule: rule.id != line.id and rule.rating == line.rating and
                                 rule.company_id == line.company_id):
                raise ValidationError(_('Same Rating can not be applied to new rule for the same company.'))
            conflicting_rules = rules.filtered(lambda rule: rule.id != line.id).filtered(
                lambda rule: rule.company_id == line.company_id and
                             rule.from_score < line.from_score and
                             rule.to_score > line.to_score or
                             rule.from_score > line.from_score and
                             rule.to_score < line.to_score or
                             line.from_score <= rule.from_score <= line.to_score <= rule.to_score or
                             rule.from_score <= line.from_score <= rule.to_score <= line.from_score)

            overlapping_rules = self.sudo().search([('company_id', '=', line.company_id.id),
                                                    ('id', '!=', line.id),
                                                    ('from_score', '<=', line.from_score),
                                                    ('to_score', '>=', line.from_score),
                                                    ('to_score', '<=', line.to_score)])
            conflicting_rules |= overlapping_rules
            if conflicting_rules:
                other_rules = ', '.join(conflicting_rules.mapped('rating'))
                raise ValidationError(_(f"Rule's score range is conflicting with rating(s) {other_rules}."))
            if not self._context.get('let_me_create', False):
                if not rules.filtered(lambda r: r.to_score == 100):
                    raise ValidationError(_('Please configure 100 as To Score field in one of the rules.'))
                if not rules.filtered(lambda r: r.from_score == 0):
                    raise ValidationError(_('Please configure 0 as From Score field in one of the rules.'))

    def _compute_company_currency(self):
        currency = self.env['res.company'].browse(self.env.context.get('allowed_company_ids')[0]).currency_id
        for record_id in self:
            record_id.company_currency = currency

    def get_company(self):
        company = self.env.context.get('allowed_company_ids')
        return company[0]

    def _calculate_ratio(self):
        overall_orders = 0
        overall_revenue = 0

        for record_id in self:
            all_customers = record_id.query_customer()
            overall_customers = all_customers and len(all_customers) > 0 and len(all_customers) or 0
            overall_orders_data = record_id.query_order_data()
            if overall_orders_data:
                overall_orders = overall_orders_data and len(overall_orders_data[0]) > 0 and overall_orders_data[0][
                    0] or 0
                overall_revenue = overall_orders_data and len(overall_orders_data[0]) > 1 and overall_orders_data[0][
                    1] or 0
            rating_orders_data = record_id.query_segment_order_data()
            rating_orders = rating_revenue = 0
            if rating_orders_data:
                rating_orders = rating_orders_data and len(rating_orders_data[0]) > 0 and rating_orders_data[0][0] or 0
                rating_revenue = rating_orders_data and len(rating_orders_data[0]) > 1 and rating_orders_data[0][1] or 0
            segment_all_customers = record_id.query_segment_customer()
            segment_customers = segment_all_customers and len(segment_all_customers) > 0 and len(
                segment_all_customers) or 0
            record_id.update({'total_customers_ratio': overall_customers and round(
                (segment_customers / overall_customers) * 100.0) or 0,
                              'total_customers': segment_customers,
                              'total_orders_ratio': overall_orders and round((rating_orders / overall_orders) * 100.0) or 0,
                              'total_orders': rating_orders,
                              'total_revenue_ratio': overall_revenue and round(
                                  (rating_revenue / overall_revenue) * 100.0) or 0,
                              'total_revenue': rating_revenue})

    def query_customer(self):
        company = self.env.context.get('allowed_company_ids')[0]
        allowed_company_ids_str = company
        self._cr.execute(
            """select partner_id from setu_customer_score where company_id in (%s);""" % (allowed_company_ids_str))
        record_id = self._cr.fetchall()
        partner_ids = self.env['res.partner'].browse(record_id)
        return partner_ids

    def query_segment_customer(self):
        company = self.env.context.get('allowed_company_ids')[0]
        allowed_company_ids_str = company
        self._cr.execute("""select partner_id from setu_customer_score where customer_rating_id in (%s) and company_id in 
        (%s);""" % (self.id, allowed_company_ids_str))
        record_id = self._cr.fetchall()
        record_id = [i[0] for i in record_id if len(i) > 0]
        partner_ids = self.env['res.partner'].browse(record_id)
        return partner_ids

    def query_order_data(self, data='count'):
        allowed_company_ids_str = ",".join(map(str, self.company_id.ids))
        if data == 'record':
            select = "distinct rel.sale_id,so.amount_total"
        else:
            select = "count(distinct rel.sale_id),sum(so.amount_total)"
        self._cr.execute("""select %s from average_sale_rel rel left 
                            join sale_order so on rel.sale_id = so.id where so.company_id in (%s)""" % (
            select, allowed_company_ids_str))
        return self._cr.fetchall()

    def query_segment_order_data(self, data='count'):
        allowed_company_ids_str = ",".join(map(str, self.company_id.ids))
        if data == 'record':
            select = "distinct rel.sale_id,so.amount_total"
        else:
            select = "count(distinct rel.sale_id),sum(so.amount_total)"
        self._cr.execute("""select %s from average_sale_rel rel 
                        left join setu_customer_score cs on rel.score_id=cs.id 
                        left join sale_order so on rel.sale_id = so.id
                        where cs.customer_rating_id in (%s) and so.company_id in (%s)""" % (
            select, self.id, allowed_company_ids_str))
        return self._cr.fetchall()

    def open_customer(self):
        kanban_view_id = self.env.ref('base.res_partner_kanban_view').id
        tree_view_id = self.env.ref('base.view_partner_tree').id
        form_view_id = self.env.ref('base.view_partner_form').id
        report_display_views = [(kanban_view_id, 'kanban'), (form_view_id, 'form'), (tree_view_id, 'tree')]
        partner_ids = self.query_segment_customer()
        if partner_ids:
            partner_ids = partner_ids.ids
        else:
            partner_ids = []
        return {
            'name': _('Customers'),
            'domain': [('id', 'in', partner_ids)],
            'res_model': 'res.partner',
            'view_mode': "kanban,form,tree",
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'edit': False},
            'views': report_display_views}

    def open_orders(self):
        form_view_id = self.env.ref('sale.view_order_form').id
        tree_view_id = self.env.ref('sale.view_order_tree').id
        report_display_views = [(tree_view_id, 'tree'), (form_view_id, 'form')]
        rating_orders_data = self.query_segment_order_data(data='record')
        order_ids = [i[0] for i in rating_orders_data if len(i) > 0]
        return {
            'name': _('Sales Order'),
            'domain': [('id', 'in', order_ids)],
            'res_model': 'sale.order',
            'view_mode': "tree,form",
            'context': {'create': False, 'edit': False},
            'type': 'ir.actions.act_window',
            'views': report_display_views}

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'from_score' in fields:
            fields.remove('from_score')
        if 'to_score' in fields:
            fields.remove('to_score')
        return super(SetuCustomerRating, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    def evaluate(self):
        pass

