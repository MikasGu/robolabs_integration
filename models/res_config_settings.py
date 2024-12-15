from odoo import api, models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    robolabs_key = fields.Char(
        string='RoboLabs API Key',
    )

    robolabs_base_url = fields.Char(
        string='RoboLabs API Base URL',
        default='https://sandbox.robolabs.lt/api/v2',
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    robolabs_key = fields.Char(
        related='company_id.robolabs_key',
        string='RobolaLabs API Key',
        readonly=False
    )

    robolabs_base_url = fields.Char(
        related='company_id.robolabs_base_url',
        string='RoboLabs API Base URL',
        readonly=False
    )
