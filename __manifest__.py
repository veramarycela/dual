# -*- coding: utf-8 -*-
{
    'name': "Moneda Dual",

    'summary': """
        Este modulo sirve para gestionar las monedas dolar y bolivar""",

    'description': """
        Este modulo sirve para gestionar las monedas dolar y bolivar
    """,
    'author': "Marycela Vera",
    'website': "http://www.servitecht.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'account', 'point_of_sale', 'web', 'product', 'sale', 'stock', 'stock_account'],
    'data': [
             'views/views_productos.xml', 
             'views/views_detalle_factura.xml',
             'views/views_dual_pago.xml',
             #'security/ir.model.access.csv',
             'views/views_dual_venta.xml',
             'views/views_dual_compra.xml',
             'views/views_dual_inventario.xml',
             'views/views_dual_asientos_contables.xml',
             'views/views_dual_partner.xml',
             #'views/views_dual_analisis_ventas.xml',
             'views/views_dual_moneda_venta.xml',                                                  
             #'views/views_dual_moneda_compra.xml',
             'template/template_factura.xml',
             'report/reporte_factura.xml',

    ],
    "installable": True,    
    'application': True,
    'assets': {
        'web.assets_qweb':[
            # 'dual/static/src/xml/pos_product_button_view.xml',
            # 'dual/static/src/xml/pos_top_button_view.xml',
            # 'dual/static/src/xml/pos_payment_button_view.xml',
            # 'dual/static/src/xml/pos_vuelto_confirm_popup_view.xml',
            # 'dual/static/src/xml/message_popup_button.xml',
        ],
        'web.assets_backend': [
            # 'dual/static/src/js/pos_product_screen_button.js',
            # 'dual/static/src/js/pos_top_button.js',
            # 'dual/static/src/js/pos_payment_button.js',
            # 'dual/static/src/js/message_popup_button.js',           
        ],
        'point_of_sale.assets': [
                # 'dual/static/src/pos/**/*.js',
                # 'dual/static/src/pos/**/*.xml',
                # 'dual/static/src/pos/**/*.scss',
                # 'dual/static/src/scss/**/*.scss',
        ]
    },
   
}
