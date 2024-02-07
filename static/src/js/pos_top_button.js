odoo.define('owl_pos.CustomTopButtons', function(require) {
'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class CustomTopButtons extends PosComponent {
        onClick()
        {
            Gui.showPopup("ErrorPopup", {
                title: this.env._t('Se hizo clic en el botón superior Marycela'),
                body: this.env._t('Bienvenido a OWL, desde el botón superior Marycela'), 
            });
        }
    }
    CustomTopButtons.template = 'CustomTopButtons';
    Registries.Component.add(CustomTopButtons);

});