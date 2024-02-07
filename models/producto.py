from odoo import models, fields, api
from odoo.exceptions import UserError
import re
import logging
_logger = logging.getLogger(__name__)




#CLASE PRODUCTO, ES PARA AGREGAR AL MODELO PRODUCTO INFORMACION SOBRE EL PRECIO EN BOLIVARES
#PRODUCTO
class Productos(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    x_dual_precio_bolivares = fields.Float(compute="_compute_precio_bolivar", store=True)
    x_dual_tasa_cambio_id = fields.Many2one("res.currency.rate", string='Tasa de Cambio', readonly=True)
    x_dual_fecha_tasa = fields.Date(string="Fecha", readonly=True)
    x_dual_tasa_cambio_valor = fields.Float(string="Tasa", readonly=True)
    
    x_dual_coste_bolivares = fields.Float(compute="_compute_coste_bolivar", store=True)
    
    x_dual_utilidad30 = fields.Float(compute='_utilidad_financiera', store=True)
    x_dual_porcentaje = fields.Float(string="Porcentaje", store =True)
    #x_dual_checklist = fields.Many2many('your.checklist.option', string='Aplicar al Precio')
    #x_dual_ costo_producto = fields.Float(string='Costo del Producto', related='product_id.standard_price', readonly=True)

    #FUNCION QUE SIRVE PARA CALCULAR LA UTILIDAD FINANCIERA DEL COSTO DE PRODUCTO
    @api.depends('standard_price')
    def _utilidad_financiera(self):
        print("Entre a calcular la utilidad financiera")
        for tarifa in self:
            if tarifa.standard_price and tarifa.x_dual_porcentaje:
                tarifa.x_dual_utilidad30 = tarifa.standard_price / ((100 - tarifa.x_dual_porcentaje)/100)
                tarifa.list_price = tarifa.x_dual_utilidad30
                print("utilidad:", tarifa.x_dual_utilidad30)
                print("porcentaje:", tarifa.x_dual_porcentaje)
            else:
                tarifa.x_dual_utilidad30 = 0.0
    
    #FUNCION PARA M,ANEJAR EL EVENTO ONCHANGE AL COSTO
    @api.onchange('standard_price')
    def onStandardPriceChange(self):
        self._utilidad_financiera()

    #FUNCION PARA MANEJAR EL EVENTO ONCHANGE AL PORCENTAJE
    @api.onchange('x_dual_porcentaje')
    def onPorcentajeChange(self):
        self._utilidad_financiera()

    #FUNCION QUE SIRVE PARA CALCULAR PRECIO DEL PRODUCTO EN BOLIVARES, RECIBE EL PRECIO EN DOLARES
    print("0.Estoy en la Clase Productos...")
    @api.depends('list_price')
    def _compute_precio_bolivar(self):        
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Obteniendo la tasa de cambio.... ")       
        for product in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:                
                # Calcular el precio del producto en bolívares utilizando la tasa de cambio
                product.x_dual_precio_bolivares = product.list_price * currency_rate.rate
                # Almacenar la tasa de cambio en el nuevo campo x_dual_tasa_cambio_id
                product.x_dual_tasa_cambio_id = currency_rate.id
                # Almacenar la fecha de la tasa de cambio en x_dual_fecha_tasa
                product.x_dual_fecha_tasa = currency_rate.name
                product.x_dual_tasa_cambio_valor = currency_rate.rate
                print("3.Asigno la fecha y la tasa de cambio a una variable....")
                print(product.list_price)
            else:
                # Si no se encuentra una tasa de cambio, dejar ambos campos como 0.0, None y None respectivamente
                print("4.No es posible encontrar la tasa de cambio....")
                product.x_dual_precio_bolivares = 0.0
                product.x_dual_tasa_cambio_id = None
                product.x_dual_fecha_tasa = None
                product.x_dual_tasa_cambio_valor = 0.0
    
    #FUNCION QUE SIRVE PARA CALCULAR COSTO DEL PRODUCTO EN BOLIVARES, RECIBE EL COSTO EN DOLARES
    print("0.Estoy en la Clase Productos...")
    @api.depends('standard_price')
    def _compute_coste_bolivar(self):        
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Computando el precio del bolivar, en funcion de la tasa de cambio.... ")             
        for product in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:                
                # Calcular el precio del producto en bolívares utilizando la tasa de cambio
                product.x_dual_coste_bolivares = product.standard_price * currency_rate.rate
                # Almacenar la tasa de cambio en el nuevo campo x_dual_tasa_cambio_id
                product.x_dual_tasa_cambio_id = currency_rate.id
                # Almacenar la fecha de la tasa de cambio en x_dual_fecha_tasa
                product.x_dual_fecha_tasa = currency_rate.name
                product.x_dual_tasa_cambio_valor = currency_rate.rate
                print("3.Asigno la fecha y la tasa de cambio a una variable y calculo el valo en bolivares....")
                print(product.standard_price)
            else:
                # Si no se encuentra una tasa de cambio, dejar ambos campos como 0.0, None y None respectivamente
                print("4.No es posible encontrar la tasa de cambio....")
                product.x_dual_coste_bolivares = 0.0
                product.x_dual_tasa_cambio_id = None
                product.x_dual_fecha_tasa = None
                product.x_dual_tasa_cambio_valor = 0.0

#CLASE FACTURA ESTA CLASE ME PERMITE MANEJAR INFORMACION SOBRE EL CAMBIO DE DOLARES A BOLIVARES EN LA FACTURA DEL TOTAL A PAGAR
#FACTURA
class Facturas(models.Model):
    _name='account.move'
    _inherit = 'account.move'

    #x_dual_paciente_id = fields.Many2one("dual.paciente")
    
    #x_direccion_ci_paciente = fields.Char(compute="_compute_x_direccion_ci_paciente", store=True)

    x_dual_total_dolares = fields.Float(compute='_dolarizar_total', store=True)

    x_dual_tasa_dolar = fields.Float(compute='_compute_tasa_dolar', store=True, string='Tasa de Cambio USD')
    
    
    #ESTA FUNCION PERMITE OBETNER LA TASA DE CAMBIO ACTUAL BOLIVARES 
    @api.depends('date', 'currency_id')
    def _compute_tasa_dolar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Facturas y obtengo la tasa de cambio...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_tasa_dolar = currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_tasa_dolar = 0.0            
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL TOTAL A PAGAR EN LA FACTURA
    @api.depends('amount_total', 'currency_id')
    def _dolarizar_total(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Facturas y y convierto en Bs al $...")    
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_total_dolares = move.amount_total * currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_total_dolares = 0.0     
       

#ESTA CLASE ME PERMITE REGISTRAR EL SUBTOTAL Y LOS PRECIOS DE DOLARES A BOLIVARES
#FACTURA
class DetalleFactura(models.Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'

    x_dual_precio_dolares = fields.Float(compute='_dolarizar', store=True)
    x_dual_subtotal_dolares = fields.Float(compute='_dolarizar_subtotal', store=True)
    x_dual_monto_diario = fields.Float(compute='_dolarizar_diario', store=True)
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL PRECIO DEL PRODUCTO EN LA FACTURA
    @api.depends('price_unit', 'currency_id')
    def _dolarizar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Detalle de Facturas y obtengo la tasa de cambio...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                # Calcular el precio en dólares usando el tipo de cambio y price_unit
                move.x_dual_precio_dolares = move.price_unit * currency_rate.rate
                print(currency_rate)
            else:
                # Si no se encuentra un tipo de cambio, dejar x_dual_precio_dolares como 0.0
                move.x_dual_precio_dolares = 0.0            
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL SUBTOTAL A PAGAR EN LA FACTURA    
    @api.depends('price_subtotal', 'currency_id')
    def _dolarizar_subtotal(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Detalle de Facturas y obtengo el valor en Bs de los $...")  
        for move_line in self:
            move = move_line.move_id
            if move.payment_state == 'not_paid':
                # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
                currency_rate = self.env['res.currency.rate'].search([
                    ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                    # Puedes ajustar esto según tus necesidades
                ], limit=1)
                print("2.La Tasa de Cambio actual es.....")
                print(currency_rate.rate)
                if currency_rate:
                    # Calcular el subtotal en dólares usando el tipo de cambio y price_subtotal
                    move_line.x_dual_subtotal_dolares = move_line.price_subtotal * currency_rate.rate                    
                else:
                    # Si no se encuentra un tipo de cambio, dejar x_dual_subtotal_dolares como 0.0
                    move_line.x_dual_subtotal_dolares = 0.0            

    #ESTA FUNCION SIRVE PARA TRANFORMAR EL VALOR EN DOLARES A BOLIVARES DE LOS ASIENTOS CONTABLES
    @api.depends('amount_currency', 'currency_id')
    def _dolarizar_diario(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Detalle de Facturas (Asientos Contable) y obtengo el valor en Bs de los $...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                # Calcular el subtotal en dólares usando el tipo de cambio y price_subtotal
                move.x_dual_monto_diario = move.amount_currency * currency_rate.rate                    
            else:
                # Si no se encuentra un tipo de cambio, dejar x_dual_subtotal_dolares como 0.0
                move.x_dual_monto_diario = 0.0    

#CLASE QUE PERMITE PASAR DE DOLARES A BOLIVARES EL MONTO DEL PAGO
#PAGO
class Pago(models.TransientModel):
    _name = 'account.payment.register' 
    #_name = 'odoo.addons.dual.models.producto.Pago'
    _inherit = 'account.payment.register'

    x_dual_pago_dolares = fields.Float(compute='_bolivarizar', store=True)
    x_dual_fecha_tasa = fields.Date(string="Fecha", readonly=True)
    x_dual_tasa_cambio_valor = fields.Float(string="Tasa", readonly=True)
    x_dual_pago_diferencia= fields.Float(string="Tasa", readonly=True)
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL ,MONTO DE PAGO DE LA FACTURA
    @api.depends('amount', 'currency_id', 'payment_difference')
    def _bolivarizar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Pagos y obtengo el valor en Bs de los $...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                # Calcular el precio en dólares usando el tipo de cambio y price_unit
                move.x_dual_pago_dolares = move.amount * currency_rate.rate
                move.x_dual_pago_diferencia = move.payment_difference * currency_rate.rate
                move.x_dual_fecha_tasa = currency_rate.name
                move.x_dual_tasa_cambio_valor = currency_rate.rate
                print(currency_rate)
            else:
                # Si no se encuentra un tipo de cambio, dejar x_dual_precio_dolares como 0.0
                move.x_dual_pago_dolares = 0.0                            
                move.x_dual_fecha_tasa = None
                move.x_dual_tasa_cambio_valor = 0.0
                move.x_dual_pago_diferencia = 0.0


#ESTA CLASE SIRVE PARA OBTENER LA TASA DE CAMBIO Y OBTENER EL TOTAL DEL PRESUPUESTO EN EL MODULO DE VENTAS 
#VENTAS
class Presupuesto(models.Model):
    _name='sale.order'
    _inherit = 'sale.order'

    #x_dual_paciente_id = fields.Many2one("dual.paciente")
    
    #x_direccion_ci_paciente = fields.Char(compute="_compute_x_direccion_ci_paciente", store=True)

    x_dual_presu_total_dolares = fields.Float(compute='_dolarizar_total', store=True)

    x_dual_presu_tasa_dolar = fields.Float(compute='_compute_tasa_dolar', store=True, string='Tasa de Cambio USD')
    
    #ESTA FUNCION PERMITE OBETNER LA TASA DE CAMBIO ACTUAL BOLIVARES 
    @api.depends('date_order', 'currency_id')
    def _compute_tasa_dolar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Ventas y obtengo la tasa de cambio...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_presu_tasa_dolar = currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_presu_tasa_dolar = 0.0            
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL TOTAL A PAGAR DEL PRESUPUESTO
    @api.depends('amount_total', 'currency_id')
    def _dolarizar_total(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Pago y obtengo el valor en Bs de los $...")      
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_presu_total_dolares = move.amount_total * currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_presu_total_dolares = 0.0     
       

#ESTA CLASE ME PERMITE REGISTRAR EL SUBTOTAL Y LOS PRECIOS DE DOLARES A BOLIVARES DE DETALLE DE VENTAS
#VENTAS
class DetallePresupuesto(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    x_dual_deta_precio_dolares = fields.Float(compute='_dolarizar', store=True)
    x_dual_deta_subtotal_dolares = fields.Float(compute='_dolarizar_subtotal', store=True)
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL PRECIO DEL PRODUCTO EN LA FACTURA
    @api.depends('price_unit', 'currency_id')
    def _dolarizar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Ventas y obtengo la tasa de cambio..")      
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                # Calcular el precio en dólares usando el tipo de cambio y price_unit
                move.x_dual_deta_precio_dolares = move.price_unit * currency_rate.rate
                print(currency_rate)
            else:
                # Si no se encuentra un tipo de cambio, dejar x_dual_precio_dolares como 0.0
                move.x_dual_deta_precio_dolares = 0.0            
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL SUBTOTAL A PAGAR EN LA FACTURA    
    @api.depends('price_subtotal', 'currency_id')
    def _dolarizar_subtotal(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Ventas y obtengo el valor en Bs de los $...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                # Calcular el subtotal en dólares usando el tipo de cambio y price_subtotal
                move.x_dual_deta_subtotal_dolares = move.price_subtotal * currency_rate.rate                    
            else:
                # Si no se encuentra un tipo de cambio, dejar x_dual_subtotal_dolares como 0.0
                move.x_dual_deta_subtotal_dolares = 0.0            

#ESTA CLASE SIRVE PARA OBTENER LA TASA DE CAMBIO Y OBTENER EL TOTAL DEL PRESUPUESTO EN EL MODULO DE COMPRAS 
#COMPRAS
class PresupuestC(models.Model):
    _name='purchase.order'
    _inherit = 'purchase.order'

    #x_dual_paciente_id = fields.Many2one("dual.paciente")
    
    #x_direccion_ci_paciente = fields.Char(compute="_compute_x_direccion_ci_paciente", store=True)

    x_dual_presu_total_dolares = fields.Float(compute='_dolarizar_total', store=True)

    x_dual_presu_tasa_dolar = fields.Float(compute='_compute_tasa_dolar', store=True, string='Tasa de Cambio USD')
    
    #ESTA FUNCION PERMITE OBETNER LA TASA DE CAMBIO ACTUAL BOLIVARES 
    @api.depends('date_order', 'currency_id')
    def _compute_tasa_dolar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Compra y obtengo la tasa de cambio...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_presu_tasa_dolar = currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_presu_tasa_dolar = 0.0            
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL TOTAL A PAGAR DEL PRESUPUESTO
    @api.depends('amount_total', 'currency_id')
    def _dolarizar_total(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Compra y obtengo el valor en Bs de los $...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_presu_total_dolares = move.amount_total * currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_presu_total_dolares = 0.0     
       

#ESTA CLASE ME PERMITE REGISTRAR EL SUBTOTAL Y LOS PRECIOS DE DOLARES A BOLIVARES DE DETALLE DE COMPRAS
#COMPRAS
class DetallePresupuestoC(models.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    x_dual_deta_precio_dolares = fields.Float(compute='_dolarizar', store=True)
    x_dual_deta_subtotal_dolares = fields.Float(compute='_dolarizar_subtotal', store=True)
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL PRECIO DEL PRODUCTO EN LA FACTURA
    @api.depends('price_unit', 'currency_id')
    def _dolarizar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Compra y obtengo la tasa de cambio...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                # Calcular el precio en dólares usando el tipo de cambio y price_unit
                move.x_dual_deta_precio_dolares = move.price_unit * currency_rate.rate
                print(currency_rate)
            else:
                # Si no se encuentra un tipo de cambio, dejar x_dual_precio_dolares como 0.0
                move.x_dual_deta_precio_dolares = 0.0            
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL SUBTOTAL A PAGAR EN LA FACTURA    
    @api.depends('price_subtotal', 'currency_id')
    def _dolarizar_subtotal(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.Estoy en la Clase Compra y obtengo el valor en Bs de los $...")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                # Calcular el subtotal en dólares usando el tipo de cambio y price_subtotal
                move.x_dual_deta_subtotal_dolares = move.price_subtotal * currency_rate.rate                    
            else:
                # Si no se encuentra un tipo de cambio, dejar x_dual_subtotal_dolares como 0.0
                move.x_dual_deta_subtotal_dolares = 0.0            

#ESTA CLASE SIRVE PARA OBTENER LA TASA DE CAMBIO Y OBTENER EL TOTAL DEL PRESUPUESTO EN EL MODULO DE INVENTARIO
#VALORACION DE INVENTARIO-
class Inventario(models.Model):
    _name='stock.valuation.layer'
    _inherit = 'stock.valuation.layer'

    #x_dual_paciente_id = fields.Many2one("dual.paciente")
    
    #x_direccion_ci_paciente = fields.Char(compute="_compute_x_direccion_ci_paciente", store=True)

    x_dual_inv_costo_dolares = fields.Float(compute='_dolarizar_costo', store=True)

    x_dual_inv_tasa_dolar = fields.Float(compute='_compute_tasa_dolar', store=True, string='Tasa de Cambio USD')
    
    x_dual_inv_value_dolares = fields.Float(compute='_dolarizar_value', store=True)
    #ESTA FUNCION PERMITE OBTENER LA TASA DE CAMBIO ACTUAL BOLIVARES 
    @api.depends('create_date', 'currency_id')
    def _compute_tasa_dolar(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1.-calculando la tasa de cambio en Valoracion de Inventario.....")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.La Tasa de Cambio actual es.....")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_inv_tasa_dolar = currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_inv_tasa_dolar = 0.0            
    
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL COSTO UNITARIO DEL INVENTARIO
    @api.depends('unit_cost','currency_id')
    def _dolarizar_costo(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1. Convirtiendo el costo unitario expresado en dolares a bolivares en Valoracion de Inventario.....")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.Tasa de Cambio es...")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_inv_costo_dolares = move.unit_cost * currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_inv_costo_dolares = 0.0     
       
    #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL VALOR DEL INVENTARIO
    @api.depends('value','currency_id')
    def _dolarizar_value(self):
        # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
        default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
        print("1. Convirtiendo el costo unitario expresado en dolares a bolivares en Valoracion de Inventario..... ")       
        for move in self:
            # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
            currency_rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
                # Puedes ajustar esto según tus necesidades
            ], limit=1)
            print("2.Tasa de Cambio es...")
            print(currency_rate.rate)
            if currency_rate:
                    # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
                    move.x_dual_inv_value_dolares = move.value * currency_rate.rate
            else:
                    # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
                    move.x_dual_inv_value_dolares = 0.0  

#ESTA CLASE SIRVE PARA OBTENER LA TASA DE CAMBIO DEL ANALISIS DE FACTURA
#ANALISIS DE FACTURA (REPORTE DE VENTAS)
# class Analisis(models.Model):
#     _name='account.invoice.report'
#     _inherit = 'account.invoice.report'

#     #x_dual_paciente_id = fields.Many2one("dual.paciente")
    
#     #x_direccion_ci_paciente = fields.Char(compute="_compute_x_direccion_ci_paciente", store=True)

#     #x_dual_inv_costo_dolares = fields.Float(compute='_dolarizar_costo', store=True)

#     #x_dual_inv_tasa_dolar = fields.Float(compute='_compute_tasa_dolar', store=True, string='Tasa de Cambio USD')
    
#     x_dual_analisis_venta = fields.Float(compute='_dolarizar_analisis', store=True)
    
#     # #ESTA FUNCION PERMITE OBTENER LA TASA DE CAMBIO ACTUAL BOLIVARES 
#     # @api.depends('invoice_date')
#     # def _compute_tasa_dolar(self):
#     #     # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
#     #     default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
#     #     print("1.-calculando la tasa de cambio en Valoracion de Inventario.....")       
#     #     for move in self:
#     #         # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
#     #         currency_rate = self.env['res.currency.rate'].search([
#     #             ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
#     #             # Puedes ajustar esto según tus necesidades
#     #         ], limit=1)
#     #         print("TRES")
#     #         print(currency_rate.rate)
#     #         if currency_rate:
#     #                 # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
#     #                 move.x_dual_inv_tasa_dolar = currency_rate.rate
#     #         else:
#     #                 # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
#     #                 move.x_dual_inv_tasa_dolar = 0.0            
    
        
#     #ESTA FUNCION PERMITE PASAR DE DOLARES A BOLIVARES EL VALOR DEL INVENTARIO
#     @api.depends('price_subtotal')
#     def _dolarizar_analisis(self):
#         # Obtener la moneda predeterminada, por ejemplo, USD (Dólar)
#         default_currency = self.env['res.currency'].search([('name', '=', 'VES')], limit=1)
#         print("1. Convirtiendo el costo unitario expresado en dolares a bolivares en Analisis de Ventas..... ")       
#         for move in self:
#             # Buscar la tasa de cambio para la moneda del producto en res.currency.rate
#             currency_rate = self.env['res.currency.rate'].search([
#                 ('currency_id', '=', default_currency.id),  # Utilizar la moneda predeterminada
#                 # Puedes ajustar esto según tus necesidades
#             ], limit=1)
#             print("2.Tasa de Cambio es....")
#             print(currency_rate.rate)
#             if currency_rate:
#                     # Almacenar el valor de la tasa de cambio en el campo x_dual_tasa_dolar
#                     move.x_dual_analisis_venta = move.price_subtotal * currency_rate.rate
#             else:
#                     # Si no se encuentra una tasa de cambio, dejar x_dual_tasa_dolar como 0.0
#                     move.x_dual_analisis_venta = 0.0 

class Informe(models.Model):
    _name = 'dual.informe'
    _description = 'Infortme de Ventas'

    # Campos adicionales que deseas agregar
    x_dual_informe = fields.Char(string='Campo')

    x_dual_analizar_ventas = fields.Many2one('account.invoice.report', string='Informe de Factura')

    product_categ_id = fields.Many2one('product.category', string="Categoría del Producto")

    invoice_date = fields.Date(string="Fecha de Factura")

    price_subtotal = fields.Date(string="Fecha de Factura")