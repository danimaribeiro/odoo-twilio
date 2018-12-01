# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class MailChannel(models.Model):
    _inherit = 'mail.channel'
