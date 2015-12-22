### Instalando en local

Para instalar la aplicación en local es necesario seguir los siguientes pasos:

* Instalar los componentes utilizados por la aplicación. Actualmente, la aplicación requiere coffin 0.4.0, así como django 1.4.2:
    
        $ pip install -r requirements.txt

    * Incompatibilidad con otras versiones de coffin y django:
        * En coffin > 0.4.0 desaparece `coffin.common.env`.
        * En django > 1.6 desaparece el argumento [deprecado][4] `mimetype`.
        * En django > = 1.5 desaparece `django.views.generic.simple`.
        * En django < 1.4.2 no se ha incorporado aún la [compatibilidad][5] con `django.utils.six`.

* Borrar base de datos:

        $ dropdb -h localhost presupuestos_caba

* Crear la base de datos:

        $ createdb -h localhost presupuestos_caba

* Copiar `local_settings.py-example` a `local_settings.py` y modificar las credenciales de la base de datos.

* Crear el esquema de la base de datos y cargar los datos básicos (ejemplo cargando datos 2014):

        $ python manage.py syncdb

        $ python manage.py load_glossary
        $ python manage.py load_entities
        $ python manage.py load_stats
        $ python manage.py load_budget 2014
        $ python manage.py load_execution 2014

* Arrancar el servidor

        $ python manage.py runserver


[4]: https://docs.djangoproject.com/en/1.7/internals/deprecation/#deprecation-removed-in-1-7
[5]: https://docs.djangoproject.com/en/1.5/topics/python3/#philosophy



### Adaptando el aspecto visual

La aplicación soporta el concepto de 'themes' capaces de modificar el aspecto visual de la web: tanto recursos estáticos (imágenes, hojas de estilo...) como las plantillas que generan el contenido de la web. El repositorio [`presupuesto-dvmi`](https://github.com/civio/presupuesto-dvmi) de Civio -una adaptación del software de Aragón Open Data a los Presupuestos Generales del Estado- es un buen ejemplo de cómo puede organizarse el contenido de un theme.

El theme a usar se configura mediante la variable `THEME`, que es referenciada en diversos puntos de `settings.py` para instalar los directorios del theme (plantillas y recursos estáticos) justo antes de los de la aplicación principal.
