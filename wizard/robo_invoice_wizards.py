from odoo import models, fields, api
from .. import robolabs_api
from odoo.exceptions import UserError


class RoboInvoiceFetchWizard(models.TransientModel):
    _name = 'robo.invoice.fetch.wizard'
    _description = 'Wizard to Fetch Invoices'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def fetch_invoices(self):
        """Fetch invoices within the specified date range."""
        self.ensure_one()
        robolabs = robolabs_api.RoboLabsAPI(self.env.company)

        if self.start_date > self.end_date:
            raise models.ValidationError("Start date cannot be later than end date.")

        invoices = robolabs.get_invoices(start_date=self.start_date, end_date=self.end_date)

        for invoice in invoices:
            existing_invoice = self.env['robo.invoice'].search([('external_id', '=', invoice['number'])])
            if existing_invoice:
                continue
            robo_invoice = self.create_robo_invoice(invoice)
            if invoice['invoice_lines']:
                self.fetch_invoice_lines(invoice['id'], robo_invoice)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'robo.invoice',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def create_robo_invoice(self, invoice_data):
        """Create a robo.invoice record."""
        return self.env['robo.invoice'].create({
            'robo_id': invoice_data['id'],
            'external_id': invoice_data['number'],
            'b_class_code_id': invoice_data['b_class_code_id'],
            'comment': invoice_data['comment'],
            'currency': invoice_data['currency'],
            'date_invoice': invoice_data['date_invoice'],
            'due_date': invoice_data['due_date'],
            'force_dates': invoice_data['force_dates'],
            'invoice_type': invoice_data['invoice_type'],
            'journal_id': invoice_data['journal_id'],
            'language': invoice_data['language'],
            'number': invoice_data['number'],
            'partner_id': invoice_data['partner_id'],
            'reference': invoice_data['reference'],
            'registration_date': invoice_data['registration_date'],
            'salesman_id': invoice_data['salesman_id'],
            'seller_partner_id': invoice_data['seller_partner_id'],
            'skip_isaf': invoice_data['skip_isaf'],
            'state': invoice_data['state'],
            'subtotal': invoice_data['subtotal'],
            'tax': invoice_data['tax'],
            'total': invoice_data['total'],
            'approved': invoice_data['approved'],
        })

    def fetch_invoice_lines(self, robo_invoice_id, robo_invoice):
        """Fetch invoice lines for the selected invoices."""
        self.ensure_one()
        robolabs = robolabs_api.RoboLabsAPI(self.env.company)
        response = robolabs.get_invoice_lines(robo_invoice_id)

        if not response.get('result', {}).get('data'):
            return

        lines = []
        for line in response.get('result', {}).get('data', []):
            robo_line = self.create_robo_invoice_line(line)
            lines.append((4, robo_line.id))

        robo_invoice.write({
            'invoice_line_ids': lines
        })

    def create_robo_invoice_line(self, line_data):
        """Create a robo.invoice.line record."""
        return self.sudo().env['robo.invoice.line'].create({
            'line_id': line_data['id'],
            'product_id': line_data['product_id'],
            'quantity': line_data['qty'],
            'price_unit': line_data['price'],
            'price_with_vat': line_data['price_with_vat'],
        })


class RoboInvoiceCreateWizard(models.TransientModel):
    _name = 'robo.invoice.create.wizard'
    _description = 'Wizard to Create Invoice'

    partner_id = fields.Integer(string='Partner ID', required=True)
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.context_today, required=True)
    due_date = fields.Date(string='Due Date', required=True)
    currency = fields.Char(string='Currency', default='EUR', required=True)
    comment = fields.Text(string='Comment')
    invoice_type = fields.Selection([('in_invoice', 'Vendor Bill'), ('out_invoice', 'Customer Invoice')],
                                    string='Invoice Type', required=True)
    journal_id = fields.Integer(string='Journal ID', required=True)
    language = fields.Selection([('LT', 'Lithuanian'), ('EN', 'English')], string='Language', required=True,
                                default='LT')
    number = fields.Char(string='Invoice Number', required=True)
    reference = fields.Char(string='Reference')
    registration_date = fields.Date(string='Registration Date', required=True)
    salesman_id = fields.Integer(string='Salesman ID')
    seller_partner_id = fields.Integer(string='Seller Partner ID')
    skip_isaf = fields.Boolean(string='Skip ISAF', default=False)
    subtotal = fields.Float(string='Subtotal', required=True)
    tax = fields.Float(string='Tax', required=True)
    total = fields.Float(string='Total', required=True)
    force_dates = fields.Boolean(string='Force Dates', default=True)
    pdf = fields.Binary(string='PDF', attachment=True, default=None)

    invoice_line_ids = fields.One2many('robo.invoice.create.line.wizard', 'wizard_id', string='Invoice Lines',
                                       required=True)

    def create_invoice(self):
        """Send invoice data to RoboLabs API."""
        self.ensure_one()

        def convert_date_field(date_field):
            return date_field.strftime('%Y-%m-%d') if date_field else None

        pdf_data = self.pdf if self.pdf else None
        pdf_filename = "pdf_1.pdf"

        payload = {
            # 'b_class_code_id': 1 if self.invoice_type == 'out_invoice' else False
            'comment': self.comment,
            'currency': self.currency,
            'date_invoice': convert_date_field(self.invoice_date),
            'due_date': convert_date_field(self.due_date),
            'force_dates': self.force_dates,
            'invoice_type': self.invoice_type,
            'journal_id': self.journal_id,
            'language': self.language,
            'number': self.number,
            'partner_id': self.partner_id,
            'reference': self.reference,
            # 'registration_date': convert_date_field(self.registration_date),
            # 'salesman_id': self.salesman_id,
            # 'seller_partner_id': self.seller_partner_id,
            'skip_isaf': self.skip_isaf,
            'subtotal': self.subtotal,
            'tax': self.tax,
            'total': self.total,
            'invoice_lines': [{
                # 'account_id': line.account_id,
                'defer_number_of_months': 2,
                'defer_start_date': '2023-05-06',
                'description': line.description,
                'discount': line.discount,
                'price': line.price_unit,
                'price_with_vat': line.price_with_vat,
                'product_id': line.product_id,
                'qty': line.quantity,
                'vat': line.vat,
            } for line in self.invoice_line_ids],
        }

        if pdf_data:
            encoded_pdf = base64.b64encode(pdf_data).decode('utf-8')
            payload["pdf"] = [(pdf_filename, encoded_pdf)]
        else:
            payload["pdf"] = None

        robolabs = robolabs_api.RoboLabsAPI(self.env.company)
        response = robolabs.create_invoice(payload)

        if response.get('error'):
            raise UserError(f"Error from RoboLabs: {response['error']}")

        return {'type': 'ir.actions.act_window_close'}


class RoboInvoiceCreateLineWizard(models.TransientModel):
    _name = 'robo.invoice.create.line.wizard'
    _description = 'Wizard Line for Creating Invoice'

    def _default_wizard(self):
        return self.env['robo.invoice.create.wizard'].browse(self._context.get('active_id'))

    wizard_id = fields.Many2one('robo.invoice.create.wizard', string='Wizard', default=_default_wizard)
    product_id = fields.Integer(string='Product ID', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    price_unit = fields.Float(string='Unit Price', required=True)
    description = fields.Text(string='Description')
    discount = fields.Float(string='Discount (%)')
    price_with_vat = fields.Float(string='Price with VAT')
    vat = fields.Float(string='VAT (%)')
    defer_number_of_months = fields.Integer(string='Defer Number of Months')
    defer_start_date = fields.Date(string='Defer Start Date')
    account_id = fields.Integer(string='Account ID')

