# -*- coding: utf-8 -*-
# Part of Odoo and Trescloud. See LICENSE file for full copyright and licensing details.

{
	'name': 'Test Jerry',
	'version': '1.0',
	'category': '',
	'description': '''
 		Personalizaciones 
	Autores:
	- Jerry Rivera
	''',
	'author': 'TRESCLOUD',
	'maintainer': 'TRESCLOUD',
	'website': 'https://www.trescloud.com',
	'summary': '',
	'license': 'OEEL-1',
	'depends': [
        'l10n_ec_edi',
        'stock',
        'sale_management'
	],
	'data': [
		# security
		# data
		# views
        'views/account_move_views.xml',
        'views/stock_picking_delivery_views.xml',
        'views/menu_views.xml',
		# wizards
	],
	'application': False,
	'installable': True,
	'auto_install': False,
}
