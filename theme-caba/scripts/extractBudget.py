#  -*-  coding: utf-8 -*-

# Creates the gastos.csv file from the budget data stored in input for each year

from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
from os import listdir, makedirs
from os.path import join, exists
from utils import input_path, output_path, format_zeroes


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
            centro = format_zeroes(
                    int(row['JUR']), 2)+format_zeroes(
                    int(row['OGESE']), 3)+format_zeroes(
                    int(row['UE']), 4)


            line = {
                'EJERCICIO': year,
                'CENTRO GESTOR': centro,
                'FUNCIONAL': row['FIN']+row['FUN'],
                # 'ECONOMICA': row['inciso']+row['principal']+row['parcial'],
                'ECONOMICA': row['ECO'][1:4],
                'FINANCIACION': row['FF'],
                'DESCRIPCION': row['PARC_DESC'],
                'SANCIONADO': row['SANCION'].replace(",",".")
            }
            wr.writerow(line)


files = [f for f in listdir(input_path)]

for fname in files:
        with open('%s/%s' % (input_path, fname), 'r') as f:
            reader = CSVKitDictReader(f,  delimiter=';')
            try:
                year = fname.split("sancionado")[1][0:4]
                create_csv_gastos(year, reader)
            except:
                continue
