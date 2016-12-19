#  -*-  coding: utf-8 -*-


input_path = "input"
input_path_actual = "input_actual"
output_path = "../data/provincia"

classifications = [
    # JURISDICCION
    [{
        'entity_name': 'jurisdiccion',
        'id_title': 'JUR',
        'name_title': 'JUR_DESC',
        'length': '2'
    # }, {
    #     'entity_name': 'subjurisdiccion',
    #     'id_title': 'subjurisdiccion',
    #     'name_title': 'desc_sjuris'
    # }, {
    #     'entity_name': 'entidad',
    #     'id_title': 'entidad',
    #     'name_title': 'desc_entidad'
    }, {
        'entity_name': 'servicio',
        'id_title': 'OGESE',
        'name_title': 'OGESE_DESC',
        'length': '3'
    }, {
        'entity_name': 'unidad_ejecutora',
        'id_title': 'UE',
        'name_title': 'UE_DESC',
        'length': '4'
    }],
    # PROGRAMA
    [{
        'entity_name': 'programa',
        'id_title': 'PROG',
        'name_title': 'PROG_DESC',
        'length': '3'
    }, {
        'entity_name': 'subprograma',
        'id_title': 'SPROG',
        'name_title': 'SPROG_DESC',
        'length': '2'
    }, {
        'entity_name': 'proyecto',
        'id_title': 'PROY',
        'name_title': 'PROY_DESC',
        'length': '2'
    }],
    # INCISO
    # [{
    #     'entity_name': 'inciso',
    #     'id_title': 'inciso',
    #     'name_title': 'desc_inciso',
    #     'length': '1'
    # }, {
    #     'entity_name': 'principal',
    #     'id_title': 'principal',
    #     'name_title': 'desc_principal',
    #     'length': '1'
    # }, {
    #     'entity_name': 'parcial',
    #     'id_title': 'parcial',
    #     'name_title': 'desc_parcial',
    #     'length': '1'
    # }],
    # UBICACION GEOGRÁFICA
    [{
        'entity_name': 'ubicacion_geografica',
        'id_title': 'GEO',
        'name_title': 'GEO_DESC',
        'length': '2'
    }],
    # FINALIDAD
    [{
        'entity_name': 'finalidad',
        'id_title': 'FIN',
        'name_title': 'FIN_DESC',
        'length': '1'
    }, {
        'entity_name': 'funcion',
        'id_title': 'FUN',
        'name_title': 'FUN_DESC',
        'length': '1'
    }],
    # FINANCIACION
    [{
        'entity_name': 'fuente_fin',
        'id_title': 'FF',
        'name_title': 'FF_DESC',
        'length': '2'
    }]
]


def map_financiacion(x):
    return {
        '11': u'Tesoro de la Ciudad',
        '12': u'Recursos propios',
        '13': u'Recursos con afectación específica',
        '14': u'Transferencias internas',
        '15': u'Crédito interno',
        '21': u'Transferencias externas',
        '22': u'Crédito externo'
    }.get(x, u'Sin especificar')


def map_finalidad(x):
    return {
        '1': u'Administracion gubernamental',
        '2': u'Servicios de defensa y seguridad',
        '3': u'Servicios sociales',
        '4': u'Servicios económicos',
        '5': u'Deuda Pública'
    }.get(x, u'No clasificados')


def get_titles(key):
    mylist = ['ejercicio']
    for clas in classifications:
        if clas[0]['entity_name'] == key:
            for entity in clas:
                mylist.append(entity['entity_name'])
            break
    mylist.append('descripcion')
    return mylist


def format_zeroes(n, z):
    return ('%0'+str(z)+'d') % n
