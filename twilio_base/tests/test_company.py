# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest.mock import patch, MagicMock
from odoo.tests.common import TransactionCase


class TestTwilioBase(TransactionCase):

    def setUp(self):
        super(TestTwilioBase, self).setUp()
        self.main_company = self.env.ref('base.main_company')
        self.main_company.twilio_account_sid = 'some_id'
        self.main_company.twilio_auth_token = 'some_token'

    @patch('odoo.addons.twilio_base.models.res_company.Client')
    def test_balance_twilio(self, mock):
        mock.return_value.api.balance.fetch.return_value = MagicMock(
            currency='US', balance='1000.00')
        self.assertEqual(self.main_company.balance_account, 'US: 1000.00')

    @patch('odoo.addons.twilio_base.models.res_company.Client')
    def test_retrieve_phones(self, mock):
        mock.return_value.incoming_phone_numbers.list.return_value = [
            MagicMock(friendly_name='PH 1', phone_number='+12345678'),
            MagicMock(friendly_name='MO 2', phone_number='+87654321'),
        ]
        self.main_company.retrieve_phone_numbers()
        phones = self.env['twilio.phone.number'].search([])
        self.assertEqual(len(phones), 2)
        # TODO Validar as outras propriedades
