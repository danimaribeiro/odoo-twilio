# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestUsers(TransactionCase):

    def setUp(self):
        super(TestUsers, self).setUp()
        self.main_company = self.env.ref('base.main_company')

    def test_twilio_client(self):
        with self.assertRaises(UserError):
            self.env.user.get_twilio_client()

    def test_default_phone(self):
        phone = self.env.user.get_default_phone()
        self.assertFalse(phone)

        default_phone = self.env['twilio.phone.number'].create({
            'name': 'Default Phone',
        })
        self.main_company.twilio_number_id = default_phone
        phone = self.env.user.get_default_phone()
        self.assertEqual(phone, default_phone)
