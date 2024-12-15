import requests
from odoo.exceptions import UserError
from datetime import datetime


class RoboLabsAPI:
    def __init__(self, company):
        self.api_key = company.robolabs_key
        self.base_url = company.robolabs_base_url

        if not self.api_key:
            raise UserError("RoboLabs API Key is not set. Set it in the General settings.")

        self.session = requests.Session()
        self.session.headers.update({"x-api-key": self.api_key})

    def get_invoices(self, start_date, end_date):
        """Fetch all invoices and filter them based on the provided date range."""
        response = self.session.get(
            f"{self.base_url}/invoice/find",
        )

        if response.status_code != 200:
            raise UserError(response.text)

        all_invoices = response.json().get('result', {}).get('data', [])

        filtered_invoices = [
            invoice for invoice in all_invoices
            if isinstance(invoice, dict) and 'date_invoice' in invoice and start_date <= datetime.strptime(
                invoice['date_invoice'], '%Y-%m-%d').date() <= end_date
        ]

        return filtered_invoices

    def get_invoice_lines(self, invoice_id):
        response = self.session.get(
            f"{self.base_url}/invoiceLine/find",
            params={"invoice_id": invoice_id}
        )
        return response.json()

    def create_invoice(self, payload):
        response = self.session.post(
            f"{self.base_url}/invoice",
            json=payload
        )

        if response.status_code != 200:
            raise UserError(response.text)

        return response.json()
