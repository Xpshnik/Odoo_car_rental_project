from odoo import models, fields

class CarReport(models.Model):
    _name = 'rental.car.report'
    _description = 'Car report'
    _auto = False

    car_id = fields.Many2one('rental.car')
    car_model_name = fields.Char()
    year = fields.Integer()
    #rental_history_id = fields.Many2one('rental.history')
    #maintenance_history_id = fields.Many2one('rental.maintenance_history')
    rentee_id = fields.Many2one('res.partner')

    max_year = fields.Integer(group_operator='max')
    
    @property
    def _table_query(self):
        return '''
        SELECT
            rc.id,
            rc.id car_id,
            COALESCE (rcm.model_name, 'unknown model') car_model_name,
            rc.year AS year,
            rentee_id,
            COALESCE (year, 0) max_year
        FROM rental_car rc
        LEFT JOIN rental_car_model rcm ON rc.model = rcm.model_name
        '''