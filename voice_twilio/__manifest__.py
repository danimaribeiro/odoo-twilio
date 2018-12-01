# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{   # pylint: disable=C8101,C8103
    'name': 'Twilio Voice Integration',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'author': 'Danimar Ribeiro',
    'website': 'https://danimaribeiro.github.io/',
    'description': """Add Twilio Voice conversation to Odoo""",
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'twilio_base',
        'phone_validation',
        'mail',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/twilio_assets.xml',
        'views/twilio_voice_call.xml',
        'views/voice_flow.xml',
    ],
    'qweb': [
        'static/src/xml/dial.xml'
    ],
}
