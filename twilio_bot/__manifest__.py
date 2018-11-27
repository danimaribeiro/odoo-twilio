# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{   # pylint: disable=C8101,C8103
    'name': 'Twilio Odoo-Bot',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'author': 'Danimar Ribeiro',
    'website': 'https://danimaribeiro.github.io/',
    'description': """Twilio Bot for whatsapp""",
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'twilio_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/twilio_bot.xml',
    ],
}
