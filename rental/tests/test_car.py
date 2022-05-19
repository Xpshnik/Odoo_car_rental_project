from psycopg2.errors import UniqueViolation
from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests import tagged, HttpCase, Form
from odoo.tools import mute_logger
from .common import TestRentalCommonBase

@tagged('car')
class TestCar(TestRentalCommonBase):

    def test_01_sequence(self):
        self.assertEqual(self.car_1.number, '#000001')
        self.assertEqual(self.car_2.number, '#000002')

    def test_02_action_pass_to_client(self):
        self.assertEqual(self.car_3.status, 'in_garage', 'Status is not in_garage')
        self.assertFalse(self.car_3.rentee_id)
        result = self.car_3.action_pass_to_client()
        expected_result = {
            'name': _('Pass to client %s') % self.car_3.name,
            'view_mode': 'form',
            'res_model': 'rental.wizard.pass_to_client',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_initial_odometer_value': self.car_3.odometer,
            }
        }
        self.assertItemsEqual(expected_result, result)
        form_data = self.env['rental.wizard.pass_to_client'].with_context(**result['context'], active_model='rental.car', active_ids=self.car_3.ids)
        form_pass_to_client = Form(form_data)
        form_pass_to_client.rentee_id = self.rentee_1
        form_pass_to_client.save()
        wizard = form_pass_to_client.save()
        wizard.action_pass_car_to_client()
        self.assertEqual(self.car_3.status, 'rented', 'Status is not rented')
        with self.assertRaises(ValidationError):
            #swapping initial and final odometer values should raise validation error
            #a 1 is added there to make sure that after swapping the initial value turns out higher than the final one
            self.car_3.rental_history_ids.final_odometer_value, self.car_3.rental_history_ids.initial_odometer_value = \
                self.car_3.rental_history_ids.initial_odometer_value - 1, self.car_3.rental_history_ids.final_odometer_value


@tagged('car')
class TestCarModel(TestRentalCommonBase):

    def test_01_model_name_constraint(self):
        with self.assertRaises(UniqueViolation), mute_logger('odoo.sql_db'):
            self.CarModel.create({
                'model_name': 'Model X',
                'manufacturer_id': self.car_manufacturer_1.id,
            })


@tagged('car', 'post_install', '-at_install')
class TestRentalJs(HttpCase):

    def test_tour(self):
        self.start_tour("/web", 'rental_tour', login='admin', timeout=180)
