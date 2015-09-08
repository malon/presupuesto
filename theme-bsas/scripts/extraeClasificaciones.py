#  -*-  coding: utf-8 -*-

#usa la misma función a la que llama variando la estructura de búsqueda

import os

from csvkit.py2 import CSVKitDictReader, CSVKitWriter
from os import listdir
from os.path import join
from utils import clasifications, map_financiacion
from utils import map_finalidad, get_titles
from utils import input_path, output_path

structure = []


def object_exists(array_to_use, object_to_search, key_to_compare):
    for index, element in enumerate(array_to_use):
        if object_to_search == element[key_to_compare]:
            return index
    return -1


def write_lines(wr, titles, index_entity, array_to_use, line, year):
    # print titles
    for a in array_to_use:
        used_line = line[:]
        # if titles[1] == 'fuente_fin':
        #     print "elemento array----->", a
        if used_line[-1] == year:  # first entity
            used_line.append(a['id'])
        else:
            used_line.append(used_line[-1]+a['id'])
        # print "index_entity+1", titles[index_entity+1]
        # print "titles:", titles
        # print "len(titles)-2:", len(titles)-2
        if index_entity+1 <= len(titles)-2:
            # if titles[1] == 'fuente_fin':
            #     print "entra subentidad"
            write_lines(
                wr, titles, index_entity+1, a[titles[index_entity+1]],
                used_line[:], year)
        # fill with blanks all the positions till description
        fill_blanks(used_line, index_entity, titles)
        used_line.append(a['name'])
        # print "used_line-------", used_line
        wr.writerow(used_line)


def fill_blanks(line, index_entity, titles):
    for i in range(index_entity+1, len(titles)-2+1):
        line.append('')


def create_csvs(structure):
    for year_element in structure:
        year = year_element['year']
        # print "year--->", year
        line = [year]
        # create directory
        if not os.path.exists(join(output_path, year)):
            os.makedirs(join(output_path, year))
        for key in year_element.keys():
            if 'year' == key:
                continue
            # myfile = open('%s/%s_clas.csv' % (year, key), 'wb')
            with open('%s/%s/%s_clas.csv' % (
                      output_path, year, key), 'w') as f:
                wr = CSVKitWriter(f, delimiter=';')
                # wr = csv.writer(
                #     myfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                titles = get_titles(key)
                # mylistUnicode = [x.encode('UTF8') for x in mylist]
                wr.writerow(titles)
                # copying value of array not reference
                array_to_use = year_element[key][:]
                index_entity = 1
                write_lines(
                    wr, titles, index_entity, array_to_use, line[:], year)

# def utf_8_encoder(unicode_csv_data):
#     for line in unicode_csv_data:
#         yield line.encode('utf-8')

# def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
#     csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
#     for row in csv_reader:
#         yield [unicode(cell, 'utf-8') for cell in row]
debug_list = []


def fill_year(year, structure, clasification, reader):
    """
    starting point is a pointer where the previous entity was created
    """
    index_year = object_exists(structure, year, 'year')
    if index_year == -1:
        structure.append({'year': year})
        original_index = len(structure)-1
    else:
        original_index = index_year
    starting_point = structure[original_index]
    # print starting_point
    count = 0
    for row in reader:
        for clasification in clasifications:
            for entity in clasification:
                if entity['entity_name'] not in debug_list:
                    debug_list.append(entity['entity_name'])
                if entity['entity_name'] not in starting_point:
                    starting_point[entity['entity_name']] = []
                id = row[entity['id_title']]
                existing_index = object_exists(
                    starting_point[entity['entity_name']], id, 'id')
                if existing_index == -1:
                    if 'desc_fuente_fin' == entity['name_title']:
                        name = map_financiacion(id)
                        # print "name financ----,", name
                        # print "id financ-----", id
                    elif 'desc_finalidad' == entity['name_title']:
                        name = map_finalidad(id)
                        # print "name finalid----,", name
                        # print "id finalid-----", id
                    elif entity['name_title'] in row.keys():
                        name = row[entity['name_title']]
                    else:
                        name = ""
                    starting_point[entity['entity_name']].append({
                        'id': id,
                        'name': name
                    })
                    index_to_use = len(starting_point[entity['entity_name']])-1
                    starting_point = starting_point[
                        entity['entity_name']][index_to_use]
                else:
                    starting_point = starting_point[
                        entity['entity_name']][existing_index]
            # pointer
            starting_point = structure[original_index]
        count += 1
        if count % 10000 == 0:
            print "Processing %s lines for year %s" % (count, year)
        #     print row
        # if count == 10:
        #     break

files = [f for f in listdir(input_path)]

for fname in files:
    # for clasification in clasifications:
        with open('%s/%s' % (input_path, fname), 'r') as f:
            reader = CSVKitDictReader(f,  delimiter=';')
            year = fname.split("-")[2][0:4]
            # print year
            # print "entidad---->",entity[0]['entity_name']
            # fill_year(year, structure, clasification, reader)
            fill_year(year, structure, clasifications, reader)

print "Entidades completadas", debug_list
#print structure
create_csvs(structure)
