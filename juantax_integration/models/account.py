'''
Created on 12 December 2018

@author: Denbho
'''
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountAccount(models.Model):
    _inherit = 'account.account'

    bir_coa_id = fields.Many2one('bir.chart.of.account', string="BIR COA", help="Map JuanTax software to generate BIR Report")

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.constrains('type', 'invoice_line_ids', 'invoice_line_ids.sale_tax_category', 'invoice_line_ids.purchase_tax_category')
    def _check_item_type(self):
        for i in self:
            category = []
            if i.type == 'out_invoice':
                for line in i.invoice_line_ids:
                    if line.sale_tax_category:
                        category.append(line.sale_tax_category)
                if len(set(category)) > 1:
                    raise UserError(_("For JuanTax's compliance, You cannot mix 'Goods' with 'Services' invoice line category. "))
            elif i.type == 'in_invoice':
                for line in i.invoice_line_ids:
                    if line.sale_tax_category in ['G', 'CG', 'GNQ', 'I']:
                        category.append('Goods')
                    elif line.sale_tax_category in ['S', 'SNQ', 'SNR']:
                        category.append('Services')
                if len(set(category)) > 1:
                    raise UserError(_("For JuanTax's compliance, You cannot mix 'Goods' with 'Services' invoice line category. "))

class BIRChartOfAccount(models.Model):
    _name = 'bir.chart.of.account'
    _order = "code asc"

    code = fields.Char(string="ATC", required="1")
    name = fields.Char(string="Name", required="1")
    description = fields.Text(string="Description")
    coa_ids = fields.One2many('account.account', 'bir_coa_id', string="Chart of Accounts")
    category = fields.Selection([
                    ('Sales/Revenues/Receipts/Fees', 'Sales/Revenues/Receipts/Fees'),
                    ('Cost of Sales and Services', 'Cost of Sales and Services'),
                    ('Ordinary Allowable Itemized Deductions', 'Ordinary Allowable Itemized Deductions'),
                    ('Property, Plant and Equipment - Net', 'Property, Plant and Equipment - Net'),
                    ('Input VAT', 'Input VAT'),
                    ('Prepaid Tax Payable', 'Prepaid Tax Payable'),
                    ('Output VAT', 'Output VAT'),
                    ('WT Payable', 'WT Payable'),
                    ('Percentage Tax', 'Percentage Tax')
                ], string="Category", required="1")

    @api.multi
    def name_get(self):
        res = super(BIRChartOfAccount, self).name_get()
        data = []
        for i in self:
            display_value = ''
            display_value += i.code or ""
            display_value += ' ['
            display_value += i.name or ""
            display_value += ']'
            data.append((i.id, display_value))
        return data
