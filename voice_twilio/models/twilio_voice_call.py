# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime
from odoo import fields, models


class TwilioVoiceCall(models.Model):
    _name = 'twilio.voice.call'
    _description = 'Voice Call from Twilio'

    name = fields.Char(string="Name", size=50, required=True)
    sid = fields.Char(string="Unique Identifier", size=40, readonly=True)
    calling_date = fields.Datetime('Calling Date')
    type = fields.Selection([('inbound', 'Inbound'),
                             ('outbound', 'Outbound')])
    from_number = fields.Char(string="From")
    to_number = fields.Char(string="To")

    from_city = fields.Char(string="From City")
    to_city = fields.Char(string="To City")
    from_state = fields.Char(string="From State")
    to_state = fields.Char(string="To State")
    from_country = fields.Char(string="From Country")
    to_country = fields.Char(string="To Country")
    state = fields.Selection([('ringing', 'Ringing'),
                              ('on-hold', 'On Hold'),
                              ('talking', 'Talking'),
                              ('completed', 'Completed')])
    call_duration = fields.Integer(string="Duration")
    voice_flow_sequence = fields.Integer(default=0)
    last_gather_key = fields.Char()
    last_gather_value = fields.Char()

    def register_new_call(self, vals):
        call = self.search([('sid', '=', vals['CallSid'])])
        if not call:
            return self.create({
                'name': 'Call from %s to: %s' % (vals['From'], vals['To']),
                'sid': vals['CallSid'],
                'type': vals['Direction'],
                'calling_date': datetime.now(),
                'from_number': vals['From'],
                'to_number': vals['To'],
                'from_city': vals.get('FromCity'),
                'to_city': vals.get('ToCity'),
                'from_state': vals.get('FromState'),
                'to_state': vals.get('ToState'),
                'from_country': vals.get('FromCountry'),
                'to_country': vals.get('ToCountry'),
                'state': vals['CallStatus'],
            })
        return call

    def action_call_completed(self, vals):
        self.write({'state': 'completed',
                    'call_duration': vals.get('CallDuration', 0)})
