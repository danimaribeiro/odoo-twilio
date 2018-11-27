# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from twilio.rest import Client
except ImportError:
    _logger.error('Cannot import twilio dependencies', exc_info=True)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def get_default_phone(self, sms=False, voice=False, whats=False):
        return self.env.user.company_id.twilio_number_id

    def get_twilio_client(self):
        company = self.company_id
        if not company.twilio_account_sid or not company.twilio_auth_token:
            raise UserError(_('Configure Twilio in your company first'))
        return Client(company.twilio_account_sid, company.twilio_auth_token)
