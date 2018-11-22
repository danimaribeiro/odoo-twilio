# © 2018 Danimar Ribeiro <danimaibeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{   # pylint: disable=C8101,C8103
    'name': 'Twilio SMS Base Module',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'author': 'Danimar Ribeiro',
    'website': 'https://danimaribeiro.github.io/',
    'description': """Base module that holds twilio configuration""",
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'base',
    ],
    'data': [
        'views/res_company.xml',
        'views/twilio.xml',
        'security/ir.model.access.csv',
    ],
}
