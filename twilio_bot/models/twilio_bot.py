# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class TwilioBotFlow(models.Model):
    _name = 'twilio.bot.flow'

    name = fields.Char(string="Name")
    identifier = fields.Char(string="Identifier")
    model_id = fields.Many2one('ir.model', string="Model")

    end_flow_action = fields.Selection(
        [('object_create', 'Create a new record'),
         ('object_write', 'Update existing record')])

    interaction_ids = fields.One2many(
        'twilio.bot.flow.interaction', 'bot_flow_id')


class TwilioBotFlowInteraction(models.Model):
    _name = 'twilio.bot.flow.interaction'

    name = fields.Char(string="Name")
    bot_flow_id = fields.Many2one('twilio.bot.flow', string="Flow")
    model_id = fields.Many2one(related='bot_flow_id.model_id', readonly=True)
    sequence = fields.Integer(string="Sequence")
    message = fields.Text(string="Message to send")

    field_id = fields.Many2one('ir.model.fields',
                               domain=[('model_id', '=', 'model_id')])


class TwilioActiveInteraction(models.Model):
    _name = 'twilio.active.interaction'

    def _compute_next_interaction(self):
        for item in self:
            item.next_interaction_id = self.env['']

    current_interaction_id = fields.Many2one('twilio.bot.flow.interaction')
    next_interaction_id = fields.Many2one(
        'twilio.bot.flow.interaction', compute='_compute_next_interaction')
