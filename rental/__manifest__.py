# -*- coding: utf-8 -*-


{
    'name': 'Car Rental',
    'category': 'Services/Car Rental',
    'version': '0.2',
    'sequence': -50,
    'depends': [
        'mail',
        'contacts',
	],
    'demo': [
        'demo/demo.xml',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizards/wizard_pass_car.xml',
        'wizards/wizard_return_car.xml',
        'views/res_config_settings.xml',
        'views/res_partner_views.xml',
        'views/car_views.xml',
        'views/car_model_views.xml',
        'views/car_manufacturer_views.xml',
        'report/car_barcode_report.xml',
        'report/car_barcode_template.xml',
        'report/car_report_views.xml',
        'views/car_menus.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'rental/static/src/xml/custom_model_widget.xml',
            'rental/static/src/components/*/*.xml',
        ],
        'web.assets_backend': [
            'rental/static/src/js/custom_model_widget.js',
            'rental/static/src/components/*/*.js',
            'rental/static/src/js/tours/*.js',
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3'
}
