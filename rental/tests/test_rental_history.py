from odoo.exceptions import ValidationError
from odoo.tests import tagged
from .common import TestRentalCommonBase

@tagged('car')
class TestCarRentalHistory(TestRentalCommonBase):

    def test_01_check_final_odometer_value_constraint(self):
        with self.assertRaises(ValidationError):
            self.car_rental_history_1.final_odometer_value = self.car_rental_history_1.initial_odometer_value - 1