# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    from twilio import twiml
    from twilio.util import TwilioCapability
except ImportError:
    _logger.error('Cannot import twilio library', exc_info=True)


class TwilioController(http.Controller):

    @http.route('/twilio/call-ended', type='http', auth="public",
                cors="*", csrf=False)
    def call_ended(self, **post):
        request.env['phone.call'].sudo().update_call_status(**post)

    @http.route('/twilio/on-hold', type='http', auth="public",
                cors="*", csrf=False)
    def call_in_hold(self, **post):
        request.env['phone.call'].sudo().update_call_status(**post)

        response = twiml.Response()
        if post["Direction"] == 'inbound' and \
           post["CallStatus"] == 'in-progress':
            if int(post['QueueTime']) > 60:
                response.hangup()
                return str(response)
        response.play("http://com.twilio.sounds.music.s3.amazonaws.com/" +
                      "MARKOVICHAMP-Borghestral.mp3")
        return str(response)

    @http.route('/twilio/call-connected', type='http', auth="public",
                cors="*", csrf=False)
    def call_connected(self, **post):
        resp = twiml.Response()
        resp.say(u"Você será atendido agora", voice="alice", language="pt-BR")
        return str(resp)

    @http.route('/twilio/response', type='http', auth="public",
                cors="*", csrf=False)
    def receive_call(self, **post):
        url_base = request.env.user.company_id.url_base
        twilio_number = request.env.user.company_id.twilio_number

        request.env['phone.call'].sudo().register_new_call(**post)
        resp = twiml.Response()

        if "client" not in post["From"]:
            resp.say("Estamos transferindo sua chamada, por favor aguarde",
                     voice="alice", language="pt-BR")
            resp.enqueue('trustcode',
                         waitUrl='http://%s/twilio/on-hold' % url_base)
            return str(resp)

        else:
            if post["To"] != 'queue':
                with resp.dial(callerId=twilio_number) as dial:
                    dial.number(post['To'])
                return str(resp)
            else:
                with resp.dial(callerId=twilio_number,
                               record='record-from-answer') as dial:
                    dial.queue(
                        'trustcode',
                        url="http://%s/twilio/call-connected" % url_base)
                return str(resp)

    @http.route('/twilio/token', type='json')
    def generate_token(self):
        sid_account = request.env.user.company_id.twilio_account_sid
        token_account = request.env.user.company_id.twilio_auth_token
        sid_twiml = request.env.user.company_id.twiml_application

        capability = TwilioCapability(sid_account, token_account)

        # Allow our users to make outgoing calls with Twilio Client
        capability.allow_client_outgoing(sid_twiml)
        capability.allow_client_incoming('support_agent')

        # Generate the capability token
        token = capability.generate()
        return token
