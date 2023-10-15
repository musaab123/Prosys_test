from odoo import api, models

class CustomPartnerLedgerReport(models.AbstractModel):
    _name = 'report.prosys_partner_ledger.partner_ledger_report'
    _inherit = 'account.partner_ledger_report'

    @api.model
    def _get_report_parameters(self, options):
        result = super(CustomPartnerLedgerReport, self)._get_report_parameters(options)
        result['custom_header'] = "Your Custom Header Content"
        result['custom_footer'] = "Your Custom Footer Content"
        return result

    def _get_report_name(self):
        return "Custom Partner Ledger Report"
