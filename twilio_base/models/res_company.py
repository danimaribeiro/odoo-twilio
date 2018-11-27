# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, fields, models

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
    twilio_number_id = fields.Many2one(
        'twilio.phone.number', string="Default Twilio Number")

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

    @api.multi
    def retrieve_phone_numbers(self):
        for item in self:
            if not item.twilio_account_sid or not item.twilio_auth_token:
                continue
            client = Client(item.twilio_account_sid, item.twilio_auth_token)
            phone_numbers = client.incoming_phone_numbers.list()
            for phone in phone_numbers:
                self.env['twilio.phone.number'].sudo().create({
                    'name': phone.friendly_name,
                    'phone_number': phone.phone_number,
                    'sms_enabled': phone.capabilities['sms'],
                    'whatsapp_enabled': '',
                    'voice_enabled': phone.capabilities['sms'],
                    'sid': phone.sid,
                })
