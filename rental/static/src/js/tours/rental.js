/** @odoo-module **/

import { _t } from 'web.core';
import { Markup } from 'web.utils';
import tour from 'web_tour.tour';

tour.register('rental_tour', {
    url: "/web",
    rainbowManMessage: _t("Now you're up to go! :)"),
    sequence: 10,
}, [tour.stepUtils.showAppsMenuItem(), {
    trigger: '.o_app[data-menu-xmlid="rental.car_rental_menu_root"]',
    content: Markup(_t('Let\'s have a look at your <b>Pipeline</b>.')),
    position: 'right',
    edition: 'community',
}, {
    trigger: '.dropdown-toggle[data-menu-xmlid="rental.car_rental_first_level_menu"]',
    content: Markup(_t('You can choose what you want displayed on the page.')),
    position: 'bottom'
}, {
    trigger: '.dropdown-item[data-menu-xmlid="rental.display_all_models_menu_action"]',
    content: Markup(_t('Let\'s see what models are already in catalogue!')),
    position: 'right'
}, {
    trigger: '.o_list_button_add',
    extra_trigger: '.o_rental_car_model_tree',
    content: Markup(_t('Create your first model!')),
    position: 'right'
}, {
    trigger: ".o_form_view .o_field_widget[name='model_name']",
    content: Markup(_t('Write your model name!')),
    position: 'top',
    run: function(actions) {
        actions.text('ХС40', this.$anchor);
    }
}, {
    trigger: ".o_form_view .o_field_widget[name='manufacturer_id']",
    content: Markup(_t('Write a trademark name to get prompted.')),
    position: 'left',
    run: function(actions) {
        actions.text('Volvo', this.$anchor.find('input'));
    }
}, {
    trigger: ".ui-menu-item > a",
    auto: true,
    in_modal: false
}, {
    trigger: '.o_form_button_save',
    extra_trigger: '.o_rental_car_model_form',
    content: Markup(_t('Save your first model.')),
    position: 'right'
}, {
    mobile: false,
    trigger: '.breadcrumb-item:first',
    content: Markup(_t('Use the breadcrumbs to go back.')),
    position: 'bottom',
    run: function(actions) {
        actions.auto('.breadcrumb-item:not(.active)');
    }
}
])