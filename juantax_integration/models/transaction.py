'''
Created on 12 December 2018

@author: Denbho
'''
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, date

from io import BytesIO
import xlwt
from xlsxwriter.workbook import Workbook
from xlwt import easyxf
import base64
import xlsxwriter

class InvoicedTransactionLine(models.Model):
    _name = 'invoiced.transaction.line'
    _order = 'invoice_id asc'

    transaction_id = fields.Many2one('invoiced.transaction', string="Transaction Batch")
    invoice_id = fields.Many2one('account.invoice', string="Invoice")

    partner_id = fields.Many2one('res.partner', string="Partner")
    contact_tin = fields.Char(string="Contact TIN")
    contact_name = fields.Char(string="Contact Name")
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    middle_name = fields.Char(string="Middle Name")

    address = fields.Text(string="Address Line")
    city = fields.Char(string="City")
    zip_code = fields.Char(string="Zip Code")
    branch_code = fields.Char(string="Branch Code")

    invoice_number = fields.Char(string="Invoice No.")
    reference_number = fields.Char(string="Reference No.")
    description = fields.Text(string="Description")
    date = fields.Date(string="Date")
    tax_type = fields.Char(string="Tax Type")
    category = fields.Char(string="Category")
    atc = fields.Char(string="ATC")

    coa_code = fields.Char(string="COA Code")
    amount_exclusive = fields.Float(string="Amount (Exclusive)")
    vat_amount_exclusive = fields.Float(string="VAT Amount (Exclusive)")
    net = fields.Float(string="Net")
    cwt = fields.Float(string="CWT")
    price = fields.Float(string="Price")
    qty = fields.Float(string="Quantity")
    transaction_tax_ids = fields.Many2many('account.tax', string="ATC/s")

class InvoicedTransaction(models.Model):
    _name = 'invoiced.transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'file_name'

    @api.multi
    def _export_transaction(self):

        if self.inv_type in ['Sale']:
            f_name = datetime.strftime(datetime.now(), "%Y/%m/%d") + " - " + 'sale_transaction.csv'
            content = '"Date","Tax Type","Category","Amount (Exclusive)","VAT (Exclusive)","Net","CWT","Contact TIN","Contact Name","First Name","Last Name","Middle Name","Invoice No.","Description","Reference No.","Quantity","Price","ATC","Address Line","City","Zip Code","COA Code","Branch Code"\r\n'
            row = 1
            for i in self.line_ids:
                content += '"%s","%s","%s",%s,%s,%s,%s,"%s","%s","%s","%s","%s","%s","%s","%s",%s,%s,"%s","%s","%s","%s","%s"\r\n'%(i.date, i.tax_type or "", i.category or "", i.amount_exclusive, i.vat_amount_exclusive,i.net, abs(i.cwt),
                                                                                                                                    i.contact_tin or "", i.contact_name or "", i.first_name or "", i.last_name or "", i.middle_name or "",
                                                                                                                                    i.invoice_id and i.invoice_id.name or "", i.description or "", i.reference_number or "", i.qty, i.price, i.atc and ((i.atc).split('-')[0]).rstrip(' ') or "",
                                                                                                                                    i.address or "", i.city or "", i.zip_code or "", i.coa_code or "")
                row += 1
        else:
            f_name = datetime.strftime(datetime.now(), "%Y/%m/%d") + " - " + 'purchase_transaction.csv'
            content = '"Date","Amount (Exclusive)","VAT (Exclusive)","Net","Category","Contact TIN","Contact Name","First Name","Last Name","Middle Name","Description","Reference No.","Quantity","Price","ATC","Address Line","City","Zip Code","COA Code","Branch Code"\r\n'
            row = 1
            for i in self.line_ids:
                content += '"%s",%s,%s,%s,"%s","%s","%s","%s","%s","%s","%s","%s",%s,%s,"%s","%s","%s","%s","%s",\r\n'%(i.date,i.amount_exclusive,i.vat_amount_exclusive,i.net,i.category or "",i.contact_tin or "",i.contact_name or "",
                                                                                                                     i.first_name or "", i.last_name or "", i.middle_name or "", i.description or "", i.reference_number or "",
                                                                                                                     i.qty, i.price, i.atc and ((i.atc).split('-')[0]).rstrip(' ') or "", i.address or "", i.city or "", i.zip_code or "", i.coa_code or "")
                row += 1
        export_id = self.write({'excel_file': base64.encodestring(content.encode()),'file_name': f_name})
        return True


    # @api.multi
    # def _export_transaction(self):
    #     output = BytesIO()
    #     workbook = xlsxwriter.Workbook(output)
    #     data_style = easyxf('font: height 180, name Arial')
    #     if self.inv_type in ['Sale']:
    #         f_name = 'sale_transaction.xlsx'
    #         sheet = workbook.add_worksheet('sale_transaction')
    #         sheet.write(0, 0, "Date")
    #         sheet.write(0, 1, "Tax Type")
    #         sheet.write(0, 2, "Category")
    #         sheet.write(0, 3, "Amount (Exclusive)")
    #         sheet.write(0, 4, "VAT (Exclusive)")
    #         sheet.write(0, 5, "Net")
    #         sheet.write(0, 6, "CWT")
    #         sheet.write(0, 7, "Contact TIN")
    #         sheet.write(0, 8, "Contact Name")
    #         sheet.write(0, 9, "First Name")
    #         sheet.write(0, 10, "Last Name")
    #         sheet.write(0, 11, "Middle Name")
    #         sheet.write(0, 12, "Invoice No.")
    #         sheet.write(0, 13, "Description")
    #         sheet.write(0, 14, "Reference No.")
    #         sheet.write(0, 15, "Quantity")
    #         sheet.write(0, 16, "Price")
    #         sheet.write(0, 17, "ATC")
    #         sheet.write(0, 18, "Address Line")
    #         sheet.write(0, 19, "City")
    #         sheet.write(0, 20, "Zip Code")
    #         sheet.write(0, 21, "COA Code")
    #         sheet.write(0, 22, "Branch Code")
    #         row = 1
    #         for i in self.line_ids:
    #             sheet.write(row, 0, i.date)
    #             sheet.write(row, 1, i.tax_type or "")
    #             sheet.write(row, 2, i.category or "")
    #             sheet.write(row, 3, i.amount_exclusive)
    #             sheet.write(row, 4, i.vat_amount_exclusive)
    #             sheet.write(row, 5, i.net)
    #             sheet.write(row, 6, abs(i.cwt))
    #             sheet.write(row, 7, i.contact_tin or "")
    #             sheet.write(row, 8, i.contact_name or "")
    #             sheet.write(row, 9, i.first_name or "")
    #             sheet.write(row, 10, i.last_name or "")
    #             sheet.write(row, 11, i.middle_name or "")
    #             sheet.write(row, 12, i.invoice_id and i.invoice_id.name or "")
    #             sheet.write(row, 13, i.description or "")
    #             sheet.write(row, 14, i.reference_number or "")
    #             sheet.write(row, 15, i.qty)
    #             sheet.write(row, 16, i.price)
    #             sheet.write(row, 17, i.atc or "")
    #             sheet.write(row, 18, i.address or "")
    #             sheet.write(row, 19, i.city or "")
    #             sheet.write(row, 20, i.zip_code or "")
    #             sheet.write(row, 21, i.coa_code or "")
    #             row += 1
    #     else:
    #         f_name = 'purchase_transaction.xlsx'
    #         sheet = workbook.add_worksheet('purchase_transaction')
    #         sheet.write(0, 0, "Date")
    #         sheet.write(0, 1, "Amount (Exclusive)")
    #         sheet.write(0, 2, "VAT (Exclusive)")
    #         sheet.write(0, 3, "Net")
    #         sheet.write(0, 4, "Category")
    #         sheet.write(0, 5, "Contact TIN")
    #         sheet.write(0, 6, "Contact Name")
    #         sheet.write(0, 7, "First Name")
    #         sheet.write(0, 8, "Last Name")
    #         sheet.write(0, 9, "Middle Name")
    #         sheet.write(0, 10, "Description")
    #         sheet.write(0, 11, "Reference No.")
    #         sheet.write(0, 12, "Quantity")
    #         sheet.write(0, 13, "Price")
    #         sheet.write(0, 14, "ATC")
    #         sheet.write(0, 15, "Address Line")
    #         sheet.write(0, 16, "City")
    #         sheet.write(0, 17, "Zip Code")
    #         sheet.write(0, 18, "COA Code")
    #         sheet.write(0, 19, "Branch Code")
    #         row = 1
    #         for i in self.line_ids:
    #             sheet.write(row, 0, i.date)
    #             sheet.write(row, 1, i.amount_exclusive)
    #             sheet.write(row, 2, i.vat_amount_exclusive)
    #             sheet.write(row, 3, i.net)
    #             sheet.write(row, 4, i.category or "")
    #             sheet.write(row, 5, i.contact_tin or "")
    #             sheet.write(row, 6, i.contact_name or "")
    #             sheet.write(row, 7, i.first_name or "")
    #             sheet.write(row, 8, i.last_name or "")
    #             sheet.write(row, 9, i.middle_name or "")
    #             sheet.write(row, 10, i.description or "")
    #             sheet.write(row, 11, i.reference_number or "")
    #             sheet.write(row, 12, i.qty)
    #             sheet.write(row, 13, i.price)
    #             sheet.write(row, 14, i.atc or "")
    #             sheet.write(row, 15, i.address or "")
    #             sheet.write(row, 16, i.city or "")
    #             sheet.write(row, 17, i.zip_code or "")
    #             sheet.write(row, 18, i.coa_code or "")
    #             row += 1
    #     workbook.close()
    #     xlsx_data = output.getvalue()
    #     export_id = self.write({'excel_file': base64.encodestring(xlsx_data),'file_name': f_name})
    #     return True

    excel_file = fields.Binary('Export Excel', copy=False)
    file_name = fields.Char('Export Excel', copy=False)
    name = fields.Char(string="Name", copy=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id, required=True)
    date_start = fields.Date(string="Start")
    date_end = fields.Date(string="End")
    date_run = fields.Datetime('Start date', default=lambda self: fields.datetime.now())
    user_id = fields.Many2one('res.users', string="Run By", default=lambda self: self.env.user)
    paid_invoice = fields.Boolean(string="Paid", default=True)
    open_invoice = fields.Boolean(string="Open", default=True)
    inv_type = fields.Selection([('Sale', 'Sale'), ('Purchase', 'Purchase')], string="Type")
    line_ids = fields.One2many('invoiced.transaction.line', 'transaction_id', string="Transactions", copy=False)
    invoice_ids = fields.Many2many('account.invoice', 'transaction_invoice_rel', string="Invoices", copy=False)
    final = fields.Boolean(string="Final", copy=False)

    # @api.multi
    # def unlink(self):
    #     if self.final:
    #         raise ValidationError(_('The system would not allow you to delete finalized report/s.'))
    #     return super(InvoicedTransaction, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('inv_type') == 'Sale':
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.invoice.transaction.action')
        else: vals['name'] = self.env['ir.sequence'].next_by_code('purchase.invoice.transaction.action')
        return super(InvoicedTransaction, self).create(vals)

    @api.multi
    def get_invoice_detail(self, invoice, invoice_line):
        data = {
            'invoice_id': invoice.id,
            'partner_id': invoice.partner_id.id,
            'date': invoice.date_invoice,
        }
        data['contact_name'] = invoice.partner_id.name
        data['contact_tin'] = invoice.partner_id.vat and "%s-%s-%s-000" %(invoice.partner_id.vat[0:3],invoice.partner_id.vat[3:6],invoice.partner_id.vat[6:]) or "000-000-001-000"
        if invoice.partner_id.company_type == 'person':
            data['first_name'] = invoice.partner_id.first_name
            data['last_name'] = invoice.partner_id.last_name
            data['middle_name'] = invoice.partner_id.middle_name
        data['address'] = invoice.partner_id.street and "%s %s"%(invoice.partner_id.street, invoice.partner_id.street1) or False
        data['city'] = invoice.partner_id.city
        data['zip_code'] = invoice.partner_id.zip
        data['transaction_tax_ids'] = invoice_line.invoice_line_tax_ids and [(6, 0, [i.id for i in invoice_line.invoice_line_tax_ids])] or False
        data['description'] = invoice_line.name
        data['price'] = invoice_line.price_unit
        data['qty'] = invoice_line.quantity
        data['cwt'] = invoice_line.withholding
        # data['vat_amount_exclusive'] = invoice_line.vat_amount
        data['net'] = invoice_line.price_total
        data['coa_code'] = invoice_line.account_id.bir_coa_id and invoice_line.account_id.bir_coa_id.code or False
        if self.inv_type == 'Sale':
            data['invoice_number'] = "%s%s"%(invoice.sequence_number_next_prefix, invoice.sequence_number_next)
            data['reference_number'] = invoice.origin
            data['category'] = invoice_line.sale_tax_category
            data['tax_type'] = invoice_line.sale_tax_type
            for tax in invoice_line.invoice_line_tax_ids:
                if tax.type_tax_use in ['sale', 'purchase']:
                    data['atc'] = tax.name
                if not tax.type_tax_use in ['withholding', 'purchase']:
                    if not tax.price_include:
                        data['amount_exclusive'] = invoice_line.price_subtotal
                        data['vat_amount_exclusive'] = invoice_line.vat_amount
                        continue
        else:
            data['reference_number'] = invoice.reference
            data['category'] = invoice_line.purchase_tax_category
            for tax in invoice_line.invoice_line_tax_ids:
                if tax.type_tax_use in ['sale', 'purchase']:
                    data['atc'] = invoice_line.withholding_tax_account_id.name
                if tax.type_tax_use in ['purchase']:
                    if not tax.price_include:
                        data['amount_exclusive'] = invoice_line.price_subtotal
                        data['vat_amount_exclusive'] = invoice_line.vat_amount
                        continue
        return data

    @api.multi
    def finalize_document(self):
        return self.write({'final': True})

    @api.multi
    def generate_transaction(self):
        # if not self.date_start:
        #     self.write({'date_start': date.today(), 'date_end': date.today()})
        condition = [('company_id', '=', self.company_id.id), ('state', 'in', ['paid', 'open'])]
        if self.date_start:
            condition.append(('date_invoice', '>=', self.date_start))
            condition.append(('date_invoice', '<=', self.date_end))
        if self.inv_type == 'Sale':
            condition.append(('type', '=', 'out_invoice'))
        else: condition.append(('type', '=', 'in_invoice'))
        transaction = self.search([('final', '=', True), ('inv_type', '=', self.inv_type)])
        inv_transactions = []
        for i in transaction:
            for inv in i.invoice_ids:
                inv_transactions.append(inv.id)
        if inv_transactions:
            condition.append(('id', 'not in', list(set(inv_transactions))))
        invoices = self.env['account.invoice'].search(condition)
        if not invoices[:1]:
            raise ValidationError(_('No Records to be generated'))
        else:
            for i in self.line_ids:
                i.unlink()
            data = []
            for i in invoices:
                category = []
                invoice_ids = []
                for line in i.invoice_line_ids:
                    if i.type == 'out_invoice':
                        if line.sale_tax_category and line.sale_tax_category in ['Services', 'Goods'] and i.state == 'paid':
                            for payment in i.payment_ids:
                                if payment.official_receipt_number:
                                    data.append([0, 0, self.get_invoice_detail(i, line)])
                                    invoice_ids.append(i.id)
                    elif i.type == 'in_invoice':
                        if line.purchase_tax_category and line.purchase_tax_category in ['G', 'CG', 'GNQ', 'I', 'S', 'SNQ', 'SNR'] and i.state == 'paid':
                            data.append([0, 0, self.get_invoice_detail(i, line)])
                            invoice_ids.append(i.id)
            if data:
                self.write({'line_ids': data, 'invoice_ids': [(6, 0, set(invoice_ids))]})
                self._export_transaction()
            return True
