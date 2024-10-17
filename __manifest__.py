{
    'name': 'Purchase Requisition Extended',
    'version': '1.0',
    'category': 'Purchase',
    'depends': ['purchase_requisition'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_requisition_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}