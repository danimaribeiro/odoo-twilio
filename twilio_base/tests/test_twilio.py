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

    @patch('odoo.addons.twilio_base.models.res_users.Client')
    def test_create_key(self, mock):
        mock.return_value.new_keys.create.return_value = MagicMock(
            sid='sid123', secret='secret123')
        # in create it should ignore sid and secret
        key = self.env['twilio.api.key'].create({
            'name': 'Key test',
            'sid': 'key sid',
            'secret': 'secret key',
        })
        self.assertEqual(key.name, 'Key test')
        self.assertEqual(key.sid, 'sid123')
        self.assertEqual(key.secret, 'secret123')

    @patch('odoo.addons.twilio_base.models.res_users.Client')
    def test_write_key(self, mock):
        mock.return_value.new_keys.create.return_value = MagicMock(
            sid='sid123', secret='secret123')
        # in create it should ignore sid and secret
        key = self.env['twilio.api.key'].create({
            'name': 'Key test',
        })
        key.write({'name': 'new name'})
        mock.return_value.keys.assert_called_with('sid123')
        mock.return_value.keys.return_value.update.assert_called_with(
            friendly_name='new name')

    @patch('odoo.addons.twilio_base.models.res_users.Client')
    def test_unlink_key(self, mock):
        mock.return_value.new_keys.create.return_value = MagicMock(
            sid='sid123', secret='secret123')
        # in create it should ignore sid and secret
        key = self.env['twilio.api.key'].create({
            'name': 'Key test',
        })
        key.unlink()
        mock.return_value.keys.assert_called_with('sid123')
        mock.return_value.keys.return_value.delete.assert_called_once_with()
