# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'author':  'Dennis Boy Silva - (Agilis Enterprise Solutions Inc.)',
    'website': 'agilis-solutions.com',
    'license': 'AGPL-3',
    'category': 'Tool',
    'data': [
        'security/ir.model.access.csv',
        'views/account.xml',
        'views/transaction.xml',
        'data/account.xml',
        ],
    'depends': [
            'base',
            'account',
            'hr_company_profile',
            'purchase_tax_ph_standard',
            'sale_tax_ph_standard',
            'accounting_payment_attributes',
        ],
    'description': '''
JuanTax Integration
    * Generates xls file of Sales and Purchases invoice transaction
    * Chart of Accounts mapping''',
    'installable': True,
    'auto_install': False,
    'name': "JuanTax Integration",
    'summary': 'JuanTax Integration',
    'test': [],
    'version': '8.0.0'

}
