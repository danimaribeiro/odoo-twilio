# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class TwilioUsage(models.Model):
    _name = 'twilio.usage'
    _description = 'Twilio Usage History'
    _order = 'start_date desc'

    name = fields.Char(string="Description")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    price = fields.Float(string="Price")
    price_unit = fields.Char(string="Price Unit")
    usage = fields.Float(string="Usage")
    usage_unit = fields.Char(string="Usage Unit")
