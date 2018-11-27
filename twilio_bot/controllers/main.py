# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)

try:
    from twilio.twiml.messaging_response import MessagingResponse
except ImportError:
    _logger.error('Cannot import twilio library', exc_info=True)


class TwilioBotController(http.Controller):

    @http.route('/trustbot/new-sms', type='http', auth="public",
                cors="*", csrf=False)
    def call_ended(self, **post):
        flow = request.env['twilio.bot.flow'].sudo().search([], limit=1)
        response = MessagingResponse()
        if not flow:
            response.message('Sorry the Bot is being building')
            return str(response)

        response.message(flow.interaction_ids[0].message)
        return str(response)
