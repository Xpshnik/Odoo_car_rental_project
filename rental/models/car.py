from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CarManufacturer(models.Model):
    _name = 'rental.car.manufacturer'
    _description = 'Car manufacturer'
    _inherit = 'mail.thread'

    name = fields.Char(required=True)
    logo = fields.Image(string="Manufacturer logo", max_width=256, max_height=256)


class CarModel(models.Model):
    _name = 'rental.car.model'
    _description = 'Car model'
    _inherit = 'mail.thread'
    
    model_name = fields.Char(required=True)
    manufacturer_id = fields.Many2one('rental.car.manufacturer', required=True)
    manufacturer_logo = fields.Image(related='manufacturer_id.logo')
    active = fields.Boolean(default=True)
    #car_ids = fields.One2many('rental.car', 'model_id')

    _sql_constraints = [
        ('unique_model_name', 'UNIQUE(model_name, manufacturer_id)', """Such a model for this manufacturer already exists!"""),
    ]


class CarRentalHistory(models.Model):
    _name = 'rental.history'
    _description = 'Car rental history'

    car_id = fields.Many2one('rental.car', readonly=True)
    date_rented = fields.Datetime(readonly=True)
    rentee_id = fields.Many2one('res.partner', required=True)
    date_returned = fields.Datetime(readonly=True)
    initial_odometer_value = fields.Integer(readonly=True)
    final_odometer_value = fields.Integer()

    @api.constrains('final_odometer_value')
    def check_final_odometer_value(self):
        if self.final_odometer_value and self.initial_odometer_value > self.final_odometer_value:
            raise ValidationError('Invalid input: odometer value after rental cannot be smaller than before rental.')


class CarMaintenanceHistory(models.Model):
    _name = 'rental.maintenance.history'
    _description = 'Car maintenance history'

    car_id = fields.Many2one('rental.car', readonly=True)
    date_finished = fields.Datetime()
    action = fields.Selection([
        ('vehicle_inspection', 'Vehicle inspection'),
        ('repairment', 'Repairment')
        ], required=True)
    description = fields.Text()
    odometer_value = fields.Integer()


class Car(models.Model):
    _name = 'rental.car'
    _description = 'A car'
    _inherit = 'mail.thread'

    name = fields.Char(compute='_compute_car_name')
    model = fields.Char(required=True) #model_id = fields.Many2one('rental.car.model', required=True)
    number = fields.Char(required=True, default='New', readonly=True)
    logo = fields.Image()    #related='model_id.manufacturer_logo')
    year = fields.Integer()
    status = fields.Selection([
        ('in_garage', 'In garage'),
        ('rented', 'Rented'),
        ('on_maintenance', 'On maintenance'),
        ('unavailable', 'Unavailable'),
        ], default= 'in_garage', required=True, tracking=True)
    date_rented = fields.Datetime()
    rentee_id = fields.Many2one('res.partner', copy=False)
    odometer = fields.Integer(tracking=True)
    active = fields.Boolean(default=True)
    rental_history_ids = fields.One2many('rental.history', 'car_id')
    maintenance_history_ids = fields.One2many('rental.maintenance.history', 'car_id')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_number', 'UNIQUE(number)', """Number is unique for every car!"""),
    ]

    @api.model
    def get_model(self, model_name):
        return self.env['rental.car.model'].sudo().search([('model_name', 'ilike', model_name)]).read(['id', 'model_name'])

    @api.model
    def create(self, vals):
        if vals.get('number', _('New')) == _('New'):
            vals['number'] = self.env['ir.sequence'].next_by_code('rental.car') or _('New')
        return super(Car, self).create(vals)

    @api.depends('model', 'number')
    def _compute_car_name(self):
        for car in self:
            car.name = f'{car.model}_{car.number}'

    #should just remove the possibility of manually changing status
    @api.onchange('status')
    def onchange_status_rented(self):
        if self.status == 'rented':
            if not self.date_rented:
                self.date_rented = fields.Datetime.now()
        else:
            self.date_rented = False

    @api.depends('active')
    def _compute_status(self):
        for car in self:
            if not car.active:
                car.status = 'unavailable'
            else:
                return

    def action_print_barcode(self):
        return self.env['ir.actions.report']._for_xml_id("rental.action_report_car_barcode")

    def action_pass_to_client(self):
        return {
            'name': _('Pass to client %s') % self.name,
            'view_mode': 'form',
            'res_model': 'rental.wizard.pass_to_client',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_initial_odometer_value': self.odometer,
            }
        }

    def action_pass_for_maintenance(self):
        return {
            'name': _('Pass for maintenance %s') % self.name,
            'view_mode': 'form',
            'res_model': 'rental.wizard.pass_for_maintenance',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_odometer_value': self.odometer,
            }
        }
            
    def action_send_notification(self):
        days = self._context.get('days', 5)
        for car in self:
            if days == 1:
                body = '%s, please, return the car %s by tomorrow\'s evening' % (car.rentee_id.name, car.name)
            else:
                body = '%s, please, return the car %s in %s days' % (car.rentee_id.name, car.name, days)
            subtype = self.env.ref('mail.mt_comment')
            car.message_post(body=body, partner_ids=car.rentee_id.ids, message_type='comment', subtype_id=subtype.id)
