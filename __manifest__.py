{
    'name': 'Purchase Order Extended',
    'version': '1.0',
    'category': 'Purchase',
    'summary': 'Extensión de órdenes de compra',
    'depends': [
        'base',
        'purchase',
        'purchase_requisition'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/multi_orden_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
