# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class TwilioApikey(models.Model):
    _name = 'twilio.api.key'
    _description = 'Twilio Api Key'

    name = fields.Char(string="Name", size=50, required=True)
    sid = fields.Char(string="Unique Identifier", size=40, readonly=True)
    secret = fields.Char(string="Secret", size=60, readonly=True)

    @api.model
    def create(self, vals):
        client = self.env.user.get_twilio_client()
        key = client.new_keys.create(friendly_name=vals['name'])
        vals['sid'] = key.sid
        vals['secret'] = key.secret
        return super(TwilioApikey, self).create(vals)

    @api.multi
    def write(self, vals):
        if "name" in vals:
            for key in self:
                client = self.env.user.get_twilio_client()
                client.keys(key.sid).update(friendly_name=vals['name'])
        return super(TwilioApikey, self).write(vals)

    @api.multi
    def unlink(self):
        for key in self:
            client = self.env.user.get_twilio_client()
            client.keys(key.sid).delete()
        return super(TwilioApikey, self).unlink()
