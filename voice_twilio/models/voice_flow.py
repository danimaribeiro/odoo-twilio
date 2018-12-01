# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import fields, models


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
