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

    def new_incoming_call(self, voice_call_id, vals):
        flow_obj = request.env['twilio.voice.flow'].sudo()
        flow = flow_obj.next_flow(voice_call_id.voice_flow_sequence)
        resp = flow.generate_twiml()
        voice_call_id.voice_flow_sequence += 1
        return str(resp)

    def call_completed(self, voice_call_id, vals):
        voice_call_id.action_call_completed(vals)
        return 'true'

    def call_in_progress(self, voice_call_id, vals):
        flow_obj = request.env['twilio.voice.flow'].sudo()

        if "Digits" in vals or "SpeechResult" in vals:
            result = vals.get('Digits') or vals.get('SpeechResult')
            flow = flow_obj.current_flow(voice_call_id.voice_flow_sequence)
            match = flow.match_response(result)
            if not match:
                return str(flow.generate_twiml())

        flow = flow_obj.next_flow(voice_call_id.voice_flow_sequence)
        if not flow:
            resp = VoiceResponse()
            resp.hangup()
            return str(resp)
        else:
            voice_call_id.voice_flow_sequence += 1
            return str(flow.generate_twiml())

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
        elif call_status == 'in-progress':
            return self.call_in_progress(voice_call_id, vals)
        else:
            resp = VoiceResponse()
            resp.hangup()
            return str(resp)

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
