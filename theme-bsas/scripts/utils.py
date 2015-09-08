#  -*-  coding: utf-8 -*-


input_path = "input"
output_path = "../data"

clasifications = [
    # JURISDICCION
    [{
        'entity_name': 'jurisdiccion',
        'id_title': 'jurisdiccion',
        'name_title': 'desc_juris'
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
        'id_title': 'ogese',
        'name_title': 'descn_servicio'
    }, {
        'entity_name': 'unidad_ejecutora',
        'id_title': 'unidad_ejecutora',
        'name_title': 'desc_ue'
    }],
    # PROGRAMA
    [{
        'entity_name': 'programa',
        'id_title': 'programa',
        'name_title': 'desc_programa'
    }, {
        'entity_name': 'subprograma',
        'id_title': 'subprograma',
        'name_title': 'desc_subprograma'
    }, {
        'entity_name': 'proyecto',
        'id_title': 'proyecto',
        'name_title': 'desc_proyecto'
    }],
    # INCISO
    [{
        'entity_name': 'inciso',
        'id_title': 'inciso',
        'name_title': 'desc_inciso'
    }, {
        'entity_name': 'principal',
        'id_title': 'principal',
        'name_title': 'desc_principal'
    }, {
        'entity_name': 'parcial',
        'id_title': 'parcial',
        'name_title': 'desc_parcial'
    }],
    # UBICACION GEOGRÁFICA
    [{
        'entity_name': 'ubicacion_geografica',
        'id_title': 'ubicacion_geografica',
        'name_title': 'desc_ubica_geo'
    }],
    # FINALIDAD
    [{
        'entity_name': 'finalidad',
        'id_title': 'finalidad',
        'name_title': 'desc_finalidad'
    }, {
        'entity_name': 'funcion',
        'id_title': 'funcion',
        'name_title': 'desc_fin_func'
    }],
    # FINANCIACION
    [{
        'entity_name': 'fuente_fin',
        'id_title': 'fuente_fin',
        'name_title': 'desc_fuente_fin'
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
    for clas in clasifications:
        if clas[0]['entity_name'] == key:
            for entity in clas:
                mylist.append(entity['entity_name'])
            break
    mylist.append('descripcion')
    return mylist
