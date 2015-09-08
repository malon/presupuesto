#  -*-  coding: utf-8 -*-

#usa la misma función a la que llama variando la estructura de búsqueda

import csv # BORRAR LUEGO
import os


from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
from os import listdir
from os.path import join
from utils import classifications, map_financiacion
from utils import map_finalidad, get_titles
from utils import input_path, output_path

# structure = []

# outputFile = 'gastos'
# inputFile = 'jurisdiccionGastos.csv'


# def object_exists(structure_to_use, object_to_search, id_to_compare):
#     for index, element in enumerate(structure_to_use):
#         if object_to_search == element[id_to_compare]:
#             return index
#     return -1


# def create_csvs(structure):
#     for element in structure:
#         year = element['year']
#         # print "year--->", year
#         if not os.path.exists(year):
#             os.makedirs(year)
#         myfile = open('%s/%s.csv' % (year, outputFile), 'wb')
#         fieldnames = [
#             'EJERCICIO', 'CENTRO GESTOR', 'FUNCIONAL',
#             'ECONOMICA', 'FINANCIACION', 'DESCRIPCION',
#             'PRESUPUESTADO', 'COMPROMETIDO', 'DEVENGADO',
#             'PAGADO'
#         ]
#         wr = csv.DictWriter(
#             myfile,
#             fieldnames=fieldnames,
#             delimiter=';',
#             quoting=csv.QUOTE_NONNUMERIC)
#         wr.writeheader()
#         for data in element['data']:
#             wr.writerow(data)


# def utf_8_encoder(unicode_csv_data):
#     for line in unicode_csv_data:
#         yield line.encode('utf-8')


# def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
#     csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
#     for row in csv_reader:
#         yield [unicode(cell, 'utf-8') for cell in row]

# with open(inputFile, 'rb') as csvfile:
#     reader = csv.reader(csvfile)
#     # reader = unicode_csv_reader(csvfile)
#     reader.next()
#     for row in reader:
#         # print "-----linea nueva"
#         # print row[11]
#         # print "buscamos anho"
#         #index_year = year_exists(row[11])
#         index_year = object_exists(structure, row[11], 'year')
#         if (index_year >= 0):
#             # print "anho ya existe", index_year
#             pass
#         else:
#             # print "anho es nuevo"
#             structure.append({'year': row[11], 'data': []})
#             index_year = len(structure)-1

#         # print "añadimos datos"
#         structure[index_year]['data'].append({
#             'EJERCICIO': row[11],
#             'CENTRO GESTOR': row[0]+'.'+row[2],
#             'FUNCIONAL': row[2]+'.'+row[4],
#             'ECONOMICA': '',
#             'FINANCIACION': '',
#             'DESCRIPCION': row[5],
#             'PRESUPUESTADO': row[6],
#             'COMPROMETIDO': row[7],
#             'DEVENGADO': row[8],
#             'PAGADO': row[9]})

# # print "final"
# # print structure
# create_csvs(structure)


def create_csv_gastos(year,reader):
    if not os.path.exists(join(output_path, year)):
        os.makedirs(join(output_path, year))
    with open('%s/%s/gastos.csv' % (
                      output_path, year), 'w') as f:
        fieldnames = [
            'EJERCICIO', 'CENTRO GESTOR', 'FUNCIONAL',
            'ECONOMICA', 'FINANCIACION', 'DESCRIPCION',
            'SANCIONADO'
        ]        
        wr = CSVKitDictWriter(f, fieldnames=fieldnames, delimiter=';')
        wr.writeheader()        
        for row in reader:
            line = {}
            # line.append(year)            
            line = {
            'EJERCICIO': year,
            'CENTRO GESTOR': row['jurisdiccion']+row['ogese']+row['unidad_ejecutora'],
            'FUNCIONAL': row['finalidad']+row['funcion'],
            'ECONOMICA': row['inciso']+row['principal']+row['parcial'],
            'FINANCIACION': row['fuente_fin'],
            'DESCRIPCION': row['desc_parcial'],
            'SANCIONADO': row['sancion']            
            }
            wr.writerow(line)


files = [f for f in listdir(input_path)]

for fname in files:
        with open('%s/%s' % (input_path, fname), 'r') as f:
            reader = CSVKitDictReader(f,  delimiter=';')
            year = fname.split("-")[2][0:4]
            create_csv_gastos(year,reader)
