# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    twilio_account_sid = fields.Char(string="SID Twilio")
    twilio_api_key = fields.Char(string="Twilio API Key")
    twilio_api_secret = fields.Char(string="Twilio API Secret")
    twilio_number = fields.Char(string="Twilio Número")
