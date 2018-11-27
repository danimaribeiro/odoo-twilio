# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class TwilioPhoneNumber(models.Model):
    _name = 'twilio.phone.number'
    _description = 'Twilio Phone Number'

    name = fields.Char(string="Friendly Name")
    phone_number = fields.Char(string="Phone Number")
    sms_enabled = fields.Boolean(string="SMS?")
    whatsapp_enabled = fields.Boolean(string="Whatsapp?")
    voice_enabled = fields.Boolean(string="Voice?")
    sid = fields.Char(string="SID")

    _sql_constraints = [
        ('uniq_phone_sid', 'unique(sid)',
         'You already have this sid used in other record'),
        ('uniq_phone_number', 'unique(phone_number)',
         'You already have this phone number used in other record')]
