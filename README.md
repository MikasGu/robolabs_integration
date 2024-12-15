# 📄 RoboLabs Integration for Odoo

## 🚀 Overview
This module provides integration with the RoboLabs API to streamline invoice management within Odoo. It includes functionality to fetch invoices, create new invoices, and manage related configurations.

---

## 📦 Features

### 🧾 Invoice Fetching Wizard
- Fetch invoices from RoboLabs API within a specified date range.
- Automatically create `robo.invoice` and `robo.invoice.line` records in Odoo.

### ✍️ Invoice Creation Wizard
- Create new invoices in RoboLabs directly from Odoo.
- Support for detailed invoice lines and optional PDF attachments.

### ⚙️ Settings
- Configure RoboLabs API key and base URL directly in Odoo's settings.

---

## 🛠️ Installation
1. Clone the repository and add it to your Odoo custom addons path.
2. Update your module list in Odoo.
3. Install the **RoboLabs Integration** module.

---

## 🧑‍💻 Usage

### 🧾 Fetching Invoices
1. Navigate to the **RoboLabs Fetch Invoices** wizard.
2. Specify the **Start Date** and **End Date**.
3. Click **Fetch** to retrieve invoices from RoboLabs.
4. Fetched invoices are displayed in the `robo.invoice` model.

#### Sample Code:
```python
start_date = fields.Date(string='Start Date', required=True)
end_date = fields.Date(string='End Date', required=True)

# Fetch invoices
robolabs = robolabs_api.RoboLabsAPI(self.env.company)
invoices = robolabs.get_invoices(start_date=self.start_date, end_date=self.end_date)
```

### ✍️ Creating Invoices
1. Navigate to the **RoboLabs Create Invoice** wizard.
2. Fill in the invoice details and add line items.
3. Optionally attach a PDF.
4. Click **Create** to send the invoice to RoboLabs.

#### Sample Code:
```python
payload = {
    'partner_id': self.partner_id,
    'date_invoice': self.invoice_date,
    'invoice_lines': [{
        'product_id': line.product_id,
        'qty': line.quantity,
        'price': line.price_unit,
    } for line in self.invoice_line_ids],
}
robolabs.create_invoice(payload)
```

### ⚙️ Configuring API Settings
1. Navigate to **Settings > General Settings**.
2. Configure the **RoboLabs API Key** and **Base URL**.

#### Sample Code:
```python
robolabs_key = fields.Char(string='RoboLabs API Key')
robolabs_base_url = fields.Char(string='RoboLabs API Base URL', default='https://sandbox.robolabs.lt/api/v2')
```

---

## 🗂️ Models

### `robo.invoice.fetch.wizard`
Wizard to fetch invoices from RoboLabs.

| Field          | Type     | Description            |
|----------------|----------|------------------------|
| start_date     | Date     | Start date for fetching invoices |
| end_date       | Date     | End date for fetching invoices   |

### `robo.invoice.create.wizard`
Wizard to create invoices in RoboLabs.

| Field          | Type     | Description            |
|----------------|----------|------------------------|
| partner_id     | Integer  | Partner ID             |
| invoice_date   | Date     | Invoice date           |
| due_date       | Date     | Due date               |
| currency       | Char     | Currency (default: EUR)|
| invoice_lines  | One2many | Line items for the invoice |

### `res.company`
Settings for RoboLabs API integration.

| Field              | Type   | Description                       |
|--------------------|--------|-----------------------------------|
| robolabs_key       | Char   | RoboLabs API Key                 |
| robolabs_base_url  | Char   | Base URL for RoboLabs API         |

---

## 🖼️ Example Screenshots

![Fetch Wizard Example](https://via.placeholder.com/800x400?text=Fetch+Wizard+Example)

![Create Wizard Example](https://via.placeholder.com/800x400?text=Create+Wizard+Example)

---

## 📋 License
This module is licensed under the MIT License. See the LICENSE file for details.

---

## 🌐 Links
- **RoboLabs API Documentation**: [https://sandbox.robolabs.lt/docs](https://sandbox.robolabs.lt/docs)
- **Odoo Documentation**: [https://www.odoo.com/documentation](https://www.odoo.com/documentation)

---

## 🛠️ Maintainers
- **Your Name** ([your.email@example.com](mailto:your.email@example.com))
- **Your Company**
