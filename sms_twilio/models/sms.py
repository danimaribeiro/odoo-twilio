# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging
from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from twilio.base.exceptions import TwilioRestException
except ImportError:
    _logger.error('Cannot import twilio', exc_info=True)


class SmsApi(models.AbstractModel):
    _inherit = 'sms.api'

    @api.model
    def _send_sms(self, numbers, message):
        client = self.env.user.get_twilio_client()
        from_number = self.env.user.company_id.twilio_number
        try:
            for number in numbers:
                client.api.account.messages.create(
                    to=number,
                    from_=from_number,
                    body=message)
        except TwilioRestException as e:
            raise UserError(e.msg)
