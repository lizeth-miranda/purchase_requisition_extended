{
    'name': 'Purchase Requisition Extended',
    'version': '1.0',
    'category': 'Purchase',
    'depends': ['purchase', 'purchase_requisition', 'purchase_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_requisition_views.xml',
        'views/purchase_order_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}