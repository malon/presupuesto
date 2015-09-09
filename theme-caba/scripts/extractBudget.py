#  -*-  coding: utf-8 -*-

# Creates the gastos.csv file from the budget data

from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
from os import listdir, makedirs
from os.path import join, exists
from utils import input_path, output_path


def create_csv_gastos(year, reader):
    if not exists(join(output_path, year)):
        makedirs(join(output_path, year))
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
                'CENTRO GESTOR': row[
                    'jurisdiccion']+row['ogese']+row['unidad_ejecutora'],
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
            create_csv_gastos(year, reader)