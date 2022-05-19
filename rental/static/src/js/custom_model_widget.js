//currently, the widget isn't used in the corresponding form view field, thus this code is inactive!!!!!!!!
odoo.define('rental.custom_model_widget', function(require) {
    'use strict';

    const core = require('web.core');
    const Qweb = core.qweb;
    const FieldChar = require('web.basic_fields').FieldChar;

    const CustomFieldChar = FieldChar.extend({
        events: _.extend({}, FieldChar.prototype.events, {
            'input': '_onInput',
            'focusout': '_onFocusoutCleanup',
        }),

        init: function() {
            this._super.apply(this, arguments); //this._super(...arguments);
        },

        _onInput: function() {
            const self = this;
            const query = this.$el.val()
            this._rpc({
                model: 'rental.car',
                method: 'get_model',
                args: [query],
            }).then((res) => {
                this._onClickRenderTemplate(self, res);
            });
        },

        _onClickRenderTemplate: function(self, data) {
            self.$el.parent().find('.test_search_div').remove();
            if (data && data.length > 0) {
                const elem = $(Qweb.render('custom_model_widget_template', {
                    list_search: data,
                }));
                elem.find('.list_car_model').on('click', self._onClickGetModelInfo.bind(self));
                self.$el.after(elem);
            }
        },

        _onClickGetModelInfo: function(ev) {
            const self = this;
            this._rpc({
                model: 'rental.car.model',
                method: 'read',
                args: [[+ev.target.dataset.id], ['model_name', 'manufacturer_logo']],
            }).then((res) => {
                const info = {
                    model: res[0].model_name || '',
                    logo: res[0].manufacturer_logo || '',
                }
                self.$el.val(res[0].model_name);
                self.trigger_up('field_changed', {
                    dataPointID: self.dataPointID,
                    operation: 'UPDATE',
                    changes: info,
                })

                self.$el.parent().find('.test_search_div').remove();
                ev.stopPropagation();
            })
        },

        _onFocusoutCleanup: function() {
            //setTimeout is essential here to prevent dropdown list being deleted before ul click event can take place
            setTimeout(() => {
                this.$el.parent().find('.test_search_div').remove();
            }, 200);
            
        },
    });

    const fieldRegistry = require('web.field_registry');

    fieldRegistry.add('my-custom-field', CustomFieldChar);

});