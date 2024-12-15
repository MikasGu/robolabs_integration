from odoo import api, fields, models


class RoboInvoice(models.Model):
    _name = "robo.invoice"
    _description = "RoboLabs Invoice"

    robo_id = fields.Integer(string="Robo ID", help="System internal ID from RoboLabs")
    external_id = fields.Char(string="External ID", help="External ID starting with 'E'")
    b_class_code_id = fields.Integer(string="B Class Code ID")
    comment = fields.Text(string="Comment")
    currency = fields.Char(string="Currency", default="EUR")
    date_invoice = fields.Date(string="Invoice Date")
    due_date = fields.Date(string="Due Date")
    force_dates = fields.Boolean(string="Force Dates")
    invoice_type = fields.Selection([
        ('out_invoice', 'Client Invoice'),
        ('in_invoice', 'Supplier Invoice'),
        ('out_refund', 'Client Credit Note'),
        ('in_refund', 'Supplier Credit Note')
    ], string="Invoice Type")
    journal_id = fields.Integer(string="Journal ID")
    language = fields.Selection([
        ('EN', 'English'),
        ('LT', 'Lithuanian')
    ], string="Language")
    number = fields.Char(string="Invoice Number")
    partner_id = fields.Integer(string="Partner ID")
    reference = fields.Char(string="Reference")
    registration_date = fields.Date(string="Registration Date")
    salesman_id = fields.Integer(string="Salesman ID")
    seller_partner_id = fields.Integer(string="Seller Partner ID")
    skip_isaf = fields.Boolean(string="Skip ISAF")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('proforma', 'Proforma'),
        ('proforma2', 'Proforma 2'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
        ('in_approval', 'In Approval')
    ], string="State", default="draft")
    subtotal = fields.Float(string="Subtotal")
    tax = fields.Float(string="Tax")
    total = fields.Float(string="Total")
    approved = fields.Boolean(string="Approved")
    invoice_line_ids = fields.One2many('robo.invoice.line', 'invoice_id', string="Invoice Lines")
    pdf = fields.Binary(string="PDF Document")
    pdf_filename = fields.Char(string="PDF Filename")


class RoboInvoiceLine(models.Model):
    _name = "robo.invoice.line"
    _description = "RoboLabs Invoice Line"

    invoice_id = fields.Many2one('robo.invoice', string="Invoice", ondelete="cascade")
    line_id = fields.Integer(string="Robo Line ID", help="System internal line ID from RoboLabs")
    product_id = fields.Integer(string="Product ID")
    quantity = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Unit Price")
    price_with_vat = fields.Float(string="Price with VAT")
    price_subtotal = fields.Float(string="Subtotal")
    tax_amount = fields.Float(string="Tax Amount")
    total_amount = fields.Float(string="Total Amount")
    description = fields.Text(string="Description")
