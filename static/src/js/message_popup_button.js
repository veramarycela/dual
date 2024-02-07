odoo.define('point_os_sale.MessagePopupButton', function(require){
    'use stric';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require ('point_of_sale.Registries');

    class MessagePopupButton extends PosComponent {
        setup(){
            super.setup();
            console.log("Mi Pantalla Favorita")
        }

        showMessagePopup(){
            this.showPopup('MessagePopup')
        }
    }

    MessagePopupButton.template = 'MessagePopupButton';
    Registries.Component.add(MessagePopupButton);



})