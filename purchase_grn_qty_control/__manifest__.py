{
    'name': 'GRN Over-Receipt Quantity Control',
    'version': '19.0.1.0.0',
    'summary': 'Block over-receipt in Goods Receipt (GRN) beyond PO quantity',
    'category': 'Inventory/Purchase',
    'author': 'Custom Module',
    'depends': ['purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
