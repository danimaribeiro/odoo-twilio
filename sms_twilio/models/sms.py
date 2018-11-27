# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import re
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
        from_phone = self.env.user.get_default_phone(whats=True)
        if not from_phone:
            return super(SmsApi, self)._send_sms(numbers, message)
        try:
            for number in numbers:
                from_number = re.sub('[^0-9]', '', from_phone.phone_number)
                number = re.sub('[^0-9]', '', number)
                if from_phone.whatsapp_enabled:
                    number = 'whatsapp:+' + number
                    from_number = 'whatsapp:+' + from_number
                else:
                    number = '+' + number
                    from_number = '+' + from_number
                client.api.account.messages.create(
                    to=number,
                    from_=from_number,
                    body=message)
        except TwilioRestException as e:
            raise UserError(e.msg)
