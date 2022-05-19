from odoo import models, fields

class WizardReturnFromClient(models.TransientModel):
    _name = 'rental.wizard.return_from_client'
    _description = 'Wizard Return from Client'

    final_odometer_value = fields.Integer(required=True)

    def action_return_car_to_garage_from_client(self):
        ctx = self._context
        car = self.env[ctx['active_model']].sudo().browse(ctx['active_ids'])
        last_rental_history = car.rental_history_ids[-1]
        last_rental_history.write({
            'date_returned': fields.Datetime.now(),
            'final_odometer_value': self.final_odometer_value,
        })
        car.with_context(mail_notrack=True).write({
            'status': 'in_garage',
            'rentee_id': False,
            'odometer': self.final_odometer_value,
        })


class WizardReturnFromMaintenance(models.TransientModel):
    _name = 'rental.wizard.return_from_maintenance'
    _description = 'Wizard Return from Maintenance'

    description = fields.Text(required=True)

    def action_return_car_to_garage_from_maintenance(self):
        ctx = self._context
        car = self.env[ctx['active_model']].sudo().browse(ctx['active_ids'])
        last_maintenance_history = car.maintenance_history_ids[-1]
        last_maintenance_history.write({
            'date_finished': fields.Datetime.now(),
            'description': self.description,
        })
        car.with_context(mail_notrack=True).write({
            'status': 'in_garage',
            'rentee_id': False,
        })