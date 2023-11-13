# from odoo.addons.setu_rfm_analysis.controller.main import RfmBackend

from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class OnBoardingController(http.Controller):

    @http.route('/setu_customer_rating/evaluate', auth='user', type='http')
    def evaluate_customer_rating(self, **kwargs):
        res = request.env['setu.customer.score'].sudo().run_customer_score_cron()
        if res:
            message = 'Customer Rating Evaluation has been done successfully.'
        else:
            message = 'Customer Rating Evaluation has failed.'

        request.env['bus.bus']._sendone(request.env.user.partner_id, 'simple_notification', {
            'title': _('Evaluation Notification'),
            'message': _(message),
            'warning': True
        })
        action_id = request.env.ref("setu_customer_rating.setu_customer_rating_kanban_action").id
        menu_id = request.env.ref('setu_customer_rating.setu_customer_rating_dashboard_menu').id
        return request.redirect(
            request.httprequest.url_root + "/web#cids={company_id}&action={action_id}&model=setu.customer.rating&view_type=kanban&menu_id={menu_id}".format(
                company_id=request.env.company.id, action_id=action_id, menu_id=menu_id))

    @http.route('/setu_customer_rating/customer_rating_upper_panel', auth='user', type='json')
    def customer_rating_upper_panel(self):
        param = request.env.context.get('allowed_company_ids')[0]
        company = request.env['res.company'].browse(param)
        rules = request.env['setu.customer.rating.company'].search([('company_id', '=', param)])
        if rules:
            has_rules = True
            message = company.banner_message
            if not message:
                message = 'Please click on Evaluate to get Customer Ratings.'

            action_id = request.env.ref('setu_customer_rating.setu_score_configuration_action').id
            menu_id = request.env.ref('setu_customer_rating.setu_customer_rating_main_menu').id
            link = f'web#action={action_id}&model=setu.score.configuration&view_type=list&menu_id={menu_id}'
        else:
            has_rules = False
            link = False
            message = f'Customer Rating rules for {company.name} are not configured. To generate and modify rules, go to Configuration/Create Score.'

        # rendered_data = request.env['ir.ui.view']._render_template(
        #     'setu_customer_rating.customer_rating_upper_panel', {
        #         'message': message,
        #         'link': link,
        #         'has_rules': has_rules,
        #         'state': company.customer_rating_calculated
        #     })
        # return request.make_response(rendered_data, headers=[('Content-Type', 'text/html')])

        return {
            'html': request.env['ir.ui.view']._render_template(
                'setu_customer_rating.customer_rating_upper_panel', {
                    'message': message,
                    'link': link,
                    'has_rules': has_rules,
                    'state': company.customer_rating_calculated

                })
        }


class CustomerRatingDashboard(http.Controller):

    @http.route('/setu_customer_rating/fetch_rating_dashboard_data', type="json", auth='user')
    def fetch_dashboard_data(self, company_id):
        dashboard_data = []
        cmp_str = 'and ip_in.company_id = %d' % company_id[0] if company_id else ''
        query = f"""
                    select 
                        cr.customer_rating_id as name,
                        count(ip.id) as count 
                    from 
                    (
                        select 
                            * 
                        from 
                            ir_property ip_in 
                        where 
                            ip_in.name = 'rating' 
                            and ip_in.res_id like 'res.partner,%'
                            and length(ip_in.value_reference) > 16
                            {cmp_str}
                    ) ip
                    inner join setu_customer_rating cr on cr.id = substring(ip.value_reference,22)::integer 
                    group by cr.customer_rating_id
                    """
        request.env.cr.execute(query)
        customer_rating_list = request.env.cr.dictfetchall()

        if customer_rating_list:
            dashboard_data.append({'chart_type': 'pie',
                                   'chart_name': 'rating_segmant',
                                   'chart_title': 'Customer Ratings',
                                   'chart_values': [{'values': customer_rating_list}]})
        return dashboard_data
