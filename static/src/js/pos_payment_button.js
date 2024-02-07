odoo.define('clinica.PaymentScreenButton', function(require){
    'use strict';
        const { useState, useRef } = owl.hooks;
        //const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
        //const { Gui } = require('point_of_sale.Gui');
        const Registries = require('point_of_sale.Registries');
        const PaymentScreen = require ('point_of_sale.PaymentScreen');
        const { _lt } = require('@web/core/l10n/translation');

        const CustomButtonPaymentScreen = (PaymentScreen) =>
            class extends PaymentScreen {                
                setup(){
                    super.setup()
                    this.state = useState({ inputEfectivobs: this.props.startingValue                    
                    });
                    this.inputEfectivobsRef = useRef('input-efectivobs-ref'); 
                }
                mounted() {                    
                    if (this.inputEfectivobsRef && this.inputEfectivobsRef.el) {
                        this.inputEfectivobsRef.el.focus();
                    }              
                 }                
                getPayload() {
                     return this.state.inputEfectivobs;
                }
                async IsCustomButton(){
                    const result= await this.showPopup("TextInputPopup", {
                        title: this.env._t('Cambio'),
                        body: this.env._t('SELECCIONE EL MÉTODO DE CAMBIO:'),                                                
                        confirmText: _lt('Ok'),
                        cancelText: _lt('Cancel'),
                        startingValue: this.props.inputEfectivobs || '',                        
                    });          
                    if (result && result.payload && result.payload.inputEfectivobs !== undefined){
                        
                        //const { inputEfectivobs } = result.payload;{
                        const { inputValue, inputEfectivobs } = result.payload;                        
                        console.log("1.-Se hizo clic en el boton SIIII", inputValue, inputEfectivobs);

                        // Actualiza el estado con el valor de inputEfectivobs
                        this.state.inputEfectivobs = inputEfectivobs;
                        console.log("2.-Estado actualizado de inputEfectivobs:", this.state.inputEfectivobs);

                         // Agreguemos algunos registros de consola adicionales para depurar
                        console.log("3.-Estado actual de inputEfectivobs:", this.state.inputEfectivobs);
                        
                        // Actualiza el estado con el valor de inputEfectivobs
                        this.state.inputEfectivobs = inputEfectivobs;
                        console.log("4.-Estado actualizado de inputEfectivobs:", this.state.inputEfectivobs);
                    }
                    else{
                        console.log("5.-Se hizo clic en el boton NOOOO");
                    }
                    console.log("6.-Hola, se confirmó el boton", result && result.confirmed);                  
                }                
            };        
        Registries.Component.extend(PaymentScreen, CustomButtonPaymentScreen);
        return CustomButtonPaymentScreen;
});