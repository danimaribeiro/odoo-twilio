# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{   # pylint: disable=C8101,C8103
    'name': 'Twilio SMS Integration',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'author': 'Danimar Ribeiro',
    'website': 'https://danimaribeiro.github.io/',
    'description': """Add Twilio SMS integration to Odoo""",
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'sms',
    ],
    'data': [
        'views/res_company.xml',
    ],
}
