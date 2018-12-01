# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

try:
    from twilio.twiml.voice_response import Dial, Gather, VoiceResponse
except ImportError:
    _logger.error('Cannot import twilio library', exc_info=True)


class TwilioVoiceFlow(models.Model):
    _name = 'twilio.voice.flow'
    _description = 'Voice Flow Configuration from Twilio'
    _order = 'sequence asc'

    name = fields.Char(string="Description", size=100, required=True)
    sequence = fields.Integer(string="Sequence")

    flow_type = fields.Selection(
        [('say', 'Say'),
         ('gather', 'Gather Information'),
         ('connect', 'Connect Call')],
        string="Type Action",
        help="Connect Call will ring for all connected users \
        unless specified partner or channel")

    say_message = fields.Text(string="Message to Play", size=1000)
    record_call = fields.Boolean(string="Record Call")

    gather_key = fields.Char(string="Gather Key Name", size=20,
                             help="Identifier to be used in the next flows \
                             that identify the question asked!")
    gather_possible_values = fields.Text(
        string="Possible values", size=500,
        help="Possible values to the caller answer. Use one answer per line! \
        Type just numbers or words, it is going to ask for digits or \
        for the caller to say the words. Use ; for use both: e.g 1;sales")

    to_partner_id = fields.Many2one(
        'res.partner', string="Partner", help="Partner to connect this call")
    to_mail_channel_id = fields.Many2one(
        'mail.channel', string="Mail Channel",
        help="Channel to connect this call")

    filter_key = fields.Char(string="Filter Key")
    filter_value = fields.Char(string="Filter Value")

    def next_flow(self, sequence):
        flow = self.search(
            [('sequence', '>', sequence)], limit=1, order='sequence asc')
        return flow

    def current_flow(self, sequence):
        flow = self.search(
            [('sequence', '=', sequence)], limit=1)
        return flow

    def _get_dial_to(self):
        if self.to_partner_id and self.to_partner_id.twilio_client:
            return [self.to_partner_id.twilio_client]
        elif self.to_mail_channel_id:
            partners = self.to_mail_channel_id.channel_last_seen_partner_ids
            return [x.twilio_client for x in partners if x.twilio_client]
        return None

    def _generate_say(self, response):
        if self.say_message and len(self.say_message) > 0:
            response.say(self.say_message, voice="alice", language="pt-BR")

    def _generate_gather(self, response):
        input = ''
        if self.gather_possible_values:
            values = [x.strip() for x in
                      self.gather_possible_values.split('\n')]
            if ";" in values[0]:
                input = 'dtmf speech'
            elif values[0].isdigit():
                input = 'dtmf'
            else:
                input = 'speech'

        gather = Gather(timeout=10, speechTimeout='auto',
                        input=input, language='pt-BR')
        self._generate_say(gather)
        response.append(gather)

    def _generate_dial(self, response):
        self._generate_say(response)
        dial_to = self._get_dial_to()
        if len(dial_to) > 0:
            dial = Dial()
            for item in dial_to[:10]:
                dial.client(item)
            response.append(dial)
        else:
            response.say('Nobody is available to answer your call!')

    def generate_twiml(self):
        response = VoiceResponse()
        if self.flow_type == 'say':
            self._generate_say(response)
        elif self.flow_type == 'gather':
            self._generate_gather(response)
        elif self.flow_type == 'connect':
            self._generate_dial(response)

        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'twilio.base.url')
        if not base_url:
            base_url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
        response.redirect(base_url + '/twilio/voice')
        return response

    def match_response(self, result):
        if self.gather_possible_values:
            values = [x.strip() for x in
                      self.gather_possible_values.split('\n')]
            for value in values:
                if result in value.split(';'):
                    return True
        return False
