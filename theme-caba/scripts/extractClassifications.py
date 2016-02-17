#  -*-  coding: utf-8 -*-

'''
Goes through the input files creating a structure like this
[
   {
      "jurisdiccion":[  ],
      "inciso":[  ],
      "ubicacion_geografica":[  ],
      "fuente_fin":[  ],
      "finalidad":[
         {
            "funcion":[
               {
                  "id":"1",
                  "name":"Salud"
               }
            ],
            "id":"3",
            "name":"Servicios sociales"
         }
      ],
      "programa":[  ],
      "year":"2015"
   },{..}]
Then one file per classification is created grouped in a folder per year
in the ouput folder.
Check the classifications array in utils.py
'''

import os

from csvkit.py2 import CSVKitDictReader, CSVKitWriter
from os import listdir
from os.path import join
from utils import classifications, map_financiacion
from utils import map_finalidad, get_titles
from utils import input_path, output_path
from utils import format_zeroes

structure = []


def object_exists(array_to_use, object_to_search, key_to_compare):
    for index, element in enumerate(array_to_use):
        if object_to_search == element[key_to_compare]:
            return index
    return -1


def write_lines(wr, titles, index_entity, array_to_use, line, year):
    for a in array_to_use:
        used_line = line[:]
        if used_line[-1] == year:  # first entity
            used_line.append(a['id'])
        else:
            used_line.append(used_line[-1]+a['id'])
        if index_entity+1 <= len(titles)-2:
            write_lines(
                wr, titles, index_entity+1, a[titles[index_entity+1]],
                used_line[:], year)
        # fill with blanks all the positions till description
        fill_blanks(used_line, index_entity, titles)
        used_line.append(a['name'])
        if titles[1] == 'inciso' or titles[1] == 'fuente_fin':
            used_line.append('G')
        wr.writerow(used_line)


def fill_blanks(line, index_entity, titles):
    for i in range(index_entity+1, len(titles)-2+1):
        line.append('')


def create_csvs(structure):
    for year_element in structure:
        year = year_element['year']
        line = [year]
        # create directory
        if not os.path.exists(join(output_path, year)):
            os.makedirs(join(output_path, year))
        for key in year_element.keys():
            if 'year' == key:
                continue
            with open('%s/%s/%s_clas.csv' % (
                      output_path, year, key), 'w') as f:
                wr = CSVKitWriter(f, delimiter=';')
                titles = get_titles(key)
                titles_def = titles[:]
                if titles[1] == 'inciso' or titles[1] == 'fuente_fin':
                    titles_def.append('gasto/ingreso')
                wr.writerow(titles_def)
                # copying value of array not reference
                array_to_use = year_element[key][:]
                index_entity = 1
                write_lines(
                    wr, titles, index_entity, array_to_use, line[:], year)

debug_list = []


def fill_year(year, structure, classification, reader):
    """
    Fill the whole structure.
    Starting point is a pointer where the previous entity was created.
    "finalidad":[
         {
            "funcion":[
               {
                  "id":"1",
                  "name":"Salud"
               }
            ],
            "id":"3",
            "name":"Servicios sociales"
         }
      ],
    For example if we just created "finalidad" with id=3, which is
    index=0 from the "finalidad" array, starting point will be 0
    in order to keep adding to this element of the array the nested
    entities, like "funcion" in this case.

    We are reading line by line of the dictreader, and for each line
    we go through all the entities of the classificactions arrays
    (see utils.py).
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
        for classification in classifications:
            for entity in classification:
                if entity['entity_name'] not in debug_list:
                    debug_list.append(entity['entity_name'])
                if entity['entity_name'] not in starting_point:
                    starting_point[entity['entity_name']] = []
                id = format_zeroes(
                    int(row[entity['id_title']]), entity['length'])
                existing_index = object_exists(
                    starting_point[entity['entity_name']], id, 'id')
                if existing_index == -1:
                    ''' This id was not added yet to this entity.
                    First we search for special cases where the values
                    have to be mmaped manually, check utils.py for info.
                    If not a special case we take the id from the file. 
                    Starting point will point to the one we are just adding.'''
                    if 'desc_fuente_fin' == entity['name_title']:
                        name = map_financiacion(id)
                    elif 'desc_finalidad' == entity['name_title']:
                        name = map_finalidad(id)
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
                    ''' This id already existed for that entity
                    starting point will point to it'''
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
        with open('%s/%s' % (input_path, fname), 'r') as f:
            reader = CSVKitDictReader(f,  delimiter=';')
            year = fname.split("-")[2][0:4]
            fill_year(year, structure, classifications, reader)

print "Entidades completadas", debug_list
# print structure
create_csvs(structure)
