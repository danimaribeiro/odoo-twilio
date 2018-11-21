# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

try:
    from twilio.rest import Client
except ImportError:
    _logger.error('Cannot import twilio dependencies', exc_info=True)

class ResCompany(models.Model):
    _inherit = 'res.company'

    twilio_account_sid = fields.Char(string="Twilio Account SID")
    twilio_auth_token = fields.Char(string="Twilio Auth Token")
    twilio_api_key = fields.Char(string="Twilio API Key")
    twilio_api_secret = fields.Char(string="Twilio API Secret")
    twilio_number = fields.Char(string="Twilio Número")

    balance_account = fields.Char(
        string="Account Balance", compute='_compute_balance_twilio')

    def _compute_balance_twilio(self):
        for item in self:
            if not item.twilio_account_sid or not item.twilio_auth_token:
                continue
            client = Client(item.twilio_account_sid, item.twilio_auth_token)

            balance = client.api.balance.fetch()
            item.balance_account = "%s: %s" % (
                balance.currency, balance.balance)
