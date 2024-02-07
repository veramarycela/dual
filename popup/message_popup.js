odoo.define('point_of_sale.MessagePopup', function(require){
'use strict';

    const Registries = require('point_of_sale.Registries');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const { useState, useRef, onMounted} = owl;

    class MessagePopup extends AbstractAwaitablePopup {
        setup(){
            super.super()
            console.log("Marycela Vera")
            this.state = useState({text_value:''})
            this.txtRef = useRef('text-value')

            onMounted(()=>this.txtRef.el.focus())
        }

        confirm(){
            console.log("Siiiiiiiiiiiiiiiiiii")
            super.confirm()
        }

        cancel(){
            console.log("Nooooooooooo")
            super.cancel()
        }
    }

    MessagePopup.template = 'MessagePopup';
    Registries.Component.add(MessagePopup)
    return MessagePopup
})