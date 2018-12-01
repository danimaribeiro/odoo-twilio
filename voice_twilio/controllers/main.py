# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    from twilio.twiml.voice_response import VoiceResponse
    from twilio.jwt.access_token import AccessToken
    from twilio.jwt.access_token.grants import VoiceGrant
except ImportError:
    _logger.error('Cannot import twilio library', exc_info=True)


class TwilioController(http.Controller):

    # @http.route('/twilio/on-hold', type='http', auth="public",
    #             cors="*", csrf=False)
    # def call_in_hold(self, **post):
    #     request.env['phone.call'].sudo().update_call_status(**post)
    #
    #     response = twiml.Response()
    #     if post["Direction"] == 'inbound' and \
    #        post["CallStatus"] == 'in-progress':
    #         if int(post['QueueTime']) > 60:
    #             response.hangup()
    #             return str(response)
    #     response.play("http://com.twilio.sounds.music.s3.amazonaws.com/" +
    #                   "MARKOVICHAMP-Borghestral.mp3")
    #     return str(response)

    def new_incoming_call(self, voice_call_id, vals):
        resp = VoiceResponse()
        resp.say("Você será atendido agora", voice="alice", language="pt-BR")
        return str(resp)

    def call_completed(self, voice_call_id, vals):
        voice_call_id.action_call_completed(vals)
        return 'true'

    @http.route('/twilio/voice', type='http', auth="public",
                cors="*", csrf=False)
    def twilio_voice_request(self, **vals):
        voice_obj = request.env['twilio.voice.call'].sudo()
        voice_call_id = voice_obj.register_new_call(vals)
        call_status = vals['CallStatus']
        if call_status == 'ringing':
            return self.new_incoming_call(voice_call_id, vals)
        elif call_status == 'completed':
            return self.call_completed(voice_call_id, vals)
        else:
            resp = VoiceResponse()
            resp.say("Desculpe ",
                     voice="alice", language="pt-BR")
            resp.hangup()
            return str(resp)

        # if "client" not in post["From"]:
        #     resp.say("Estamos transferindo sua chamada, por favor aguarde",
        #              voice="alice", language="pt-BR")
        #     resp.enqueue('trustcode',
        #                  waitUrl='http://%s/twilio/on-hold' % url_base)
        #     return str(resp)
        #
        # else:
        #     if post["To"] != 'queue':
        #         with resp.dial(callerId=twilio_number) as dial:
        #             dial.number(post['To'])
        #         return str(resp)
        #     else:
        #         with resp.dial(callerId=twilio_number,
        #                        record='record-from-answer') as dial:
        #             dial.queue(
        #                 'trustcode',
        #                 url="http://%s/twilio/call-connected" % url_base)
        #         return str(resp)

    @http.route('/twilio/token', type='json')
    def generate_token(self):
        sid_account = request.env.user.company_id.twilio_account_sid
        api_key = request.env.user.company_id.twilio_api_key
        api_secret = request.env.user.company_id.twilio_api_secret
        sid_twiml = request.env.user.company_id.twiml_application

        # Create access token with credentials
        token = AccessToken(sid_account, api_key, api_secret, identity='user')

        # Create a Voice grant and add to token
        voice_grant = VoiceGrant(outgoing_application_sid=sid_twiml)
        token.add_grant(voice_grant)

        return token.to_jwt()
