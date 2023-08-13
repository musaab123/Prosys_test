# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ReportPackingList(models.AbstractModel):
    _name = 'report.prosys_packing_list_custom.prosys_invoice_report_pdf'
    _description = 'Get packing list  result as PDF.'

    @api.model
    def _calculate_amount(self):
        hs_code_array = []
        
        for rec in self.hscode_id:  
            amount = 0
            quantity = 0
            
            for product in rec.order_line:
                quantity += product.product_uom_qty
                amount += product.price_subtotal
            
            vals = {'hs_code': rec.name,  
                    'quantity': quantity,
                    'amount': amount
                    }
            price_unit = quantity / amount
            hs_code_array.append(vals)
        print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',hs_code_array)
        return hs_code_array
    

    @api.model
    def get_report_data(self, docids):
        report_data = []
        for doc_id in docids:
            hs_code_array = self._calculate_amount(doc_id)
            report_data.append({
                'doc_id': doc_id,
                'hs_code_array': hs_code_array,
            })
        return report_data
    

    def print_packing_list_report(self):
        active_id = self.env.context.get('active_id')
        report = self.env.ref('prosys_packing_list_custom.prosys_invoice_report_pdf')
        return report.report_action(self, data={'doc_id': active_id})
        
    # def _get_report_values(self, docids, data):
    #     return self._get_report_data(data, 'pdf')
    


    
   



