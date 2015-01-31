# -*- coding: utf-8 -*-

{
    'name': 'InfoSaône / Module Odoo de gestion des lots pour le contrôle qualité',
    'version': '1.0',
    'category': 'InfoSaône',
    'description': """
Gestion du contrôle qualité
""",
    'author': 'Tony GALMICHE / Asma BOUSSELMI',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': ['base', 'stock'],
    'data': ['security/is_gestion_lot_security.xml',
             'is_stock_view.xml',
             'wizard/is_gestion_lot_view.xml',
             'wizard/is_stock_mise_rebut_view.xml',
             'report/report_stock_bloquer_lot.xml',
             'report/report_stock_debloquer_lot.xml',
             'report/report_stock_change_location_lot.xml',
             'report/report_stock_rebut_lot.xml',       
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
