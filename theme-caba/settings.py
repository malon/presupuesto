# -*- coding: UTF-8 -*-

MAIN_ENTITY_LEVEL = 'provincia'
MAIN_ENTITY_NAME = 'CABA'

BUDGET_LOADER = 'CabaBudgetLoader'
INSTITUTIONAL_FILE = 'jurisdiccion_clas.csv'
ECONOMICAL_FILE = 'economico_clas.csv'
FUNDING_FILE = 'fuente_fin_clas.csv'
FUNCTIONAL_FILE = 'finalidad_clas.csv'

FEATURED_PROGRAMMES = ['31', '34', '35']

# # Sobre la Renta, IVA, Impuestos Especiales,
# # Financiación Autonómica, FEAGA, Capital
#OVERVIEW_INCOME_NODES = ['10', '21', '22', '40', '49', '11']
# OVERVIEW_INCOME_NODES = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '20', '21', '22', '23', '24', '30', '31', '32', '33', '34']
OVERVIEW_INCOME_NODES = ['11', '13', '14', '16', '17', '21', '22', '23']
# OVERVIEW_INCOME_NODES = ['111','112','113','130','140','160','170','210','220','230']
#OVERVIEW_INCOME_NODES = ['111','113','114','116','117','121','122','123','131']
# # Sanidad, Educación, Agricultura, Protección Social,
# # Deuda Pública, Infraestructuras
#OVERVIEW_EXPENSE_NODES = ['241', '242', '371', '231', '001', '351']
#OVERVIEW_EXPENSE_NODES = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '29', '30', '31', '32', '33', '34', '35', '39']
#OVERVIEW_EXPENSE_NODES = ['11', '12', '13', '15', '16', '17', '31', '32', '34', '35', '37', '38', '36', '43', '44', '49', '46', '45', '48', '22', '51', '91']
OVERVIEW_EXPENSE_NODES = ['1', '2', '3', '4', '5', '9']

# Show an extra tab with institutional breakdown. Default: True.
# SHOW_INSTITUTIONAL_TAB = True

# Show an extra tab with funding breakdown
# (only applicable to some budgets). Default: False.
SHOW_FUNDING_TAB = True

# Show an extra column with actual revenues/expenses. Default: True.
# Warning: the execution data still gets
# shown in the summary chart and in downloads.
# SHOW_ACTUAL = True

# Include financial income/expenditures in overview
# and global policy breakdowns. Default: False.
# INCLUDE_FINANCIAL_CHAPTERS_IN_BREAKDOWNS = False
INCLUDE_FINANCIAL_CHAPTERS_IN_BREAKDOWNS = True

# Search in entity names. Default: True.
# SEARCH_ENTITIES = True
