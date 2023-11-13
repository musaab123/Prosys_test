from datetime import datetime

import pytz
from odoo import fields, models, api


def change_time_zone(local_timezone, datetime_obj):
    local_timezone = pytz.timezone(local_timezone)
    datetime_obj = datetime.strptime(f"{datetime_obj}", "%Y-%m-%d %H:%M:%S")
    local_dt = local_timezone.localize(datetime_obj, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


class RFMHistoryManagementReport(models.TransientModel):
    _name = 'setu.rating.history.management.report'
    _description = 'Customer Rating History Management Report'

    partner_ids = fields.Many2many('res.partner', string="Partner")
    team_ids = fields.Many2many('crm.team', string="Team")
    company_ids = fields.Many2many('res.company')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="END Date")

    def generate_report(self):
        domain = []
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))
        if self.company_ids:
            domain.append(('company_id', 'in', self.company_ids.ids))
        start_date = False
        end_date = False
        local_timezone = self.env.context.get('tz', 'UTC')
        if self.start_date:
            start_date = change_time_zone(local_timezone, str(self.start_date) + ' 00:00:00')
        if self.end_date:
            end_date = change_time_zone(local_timezone, str(self.end_date) + ' 23:59:59')
        if start_date:
            domain.append(('date_changed', '>=', start_date))
        if end_date:
            domain.append(('date_changed', '<=', end_date))
        history = self.env['setu.partner.rating.history'].sudo().search(domain)
        if history:
            history = history.ids
        else:
            history = []
        domain.append(('id', 'in', history))

        return {
            'name': 'Rating History Report',
            'res_model': 'setu.partner.rating.history',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'view_id': self.env.ref('prosys_customer_rating.setu_partner_rating_history_tree_view').id,
            'context': {'search_default_group_by_company_id': 1, 'search_default_group_by_partner_id': 1},
            'domain': domain
        }
