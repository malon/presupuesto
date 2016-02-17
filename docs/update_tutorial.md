# TUTORIAL DE ACTUALIZACION DE DATOS

Es imprescindible leer antes el [Tutorial de datos] (data_tutorial.md) para entender cuales son los formatos de los datos de entrada, las fuentes de las que se obtienen y las transformaciones que se deben hacer de los datos fuente en los datos de entrada de la aplicación.
En el presente tutorial se listarán los pasos a seguir para hacer actualizaciones, pero estos pasos se explican con mayor detalle en el citado tutorial.
## Pasos para actualizar datos en la aplicación

### 1. Añadir datos de ejecución del 4to trimestre del añoN 
Este apartado se refiere a añadir datos de ejecución de un año del que ya tenemos datos sancionados. Como los archivos de clasificación de ese año ya están disponibles, no es necesario, en principio obtener nuevas clasificaciones. 

1. Colocar el archivo `presupuesto-ejecutado-<añoN>-4Trimestre.csv` en el directorio `input_actual` de `theme-caba/scripts`. Fijarse en que la linea de títulos no tenga espacios en blanco (porque leemos con csvdictkitreader). Además los archivos deben ser UTF-8, los podemos transformar con Sublime (guardar con encoding). 

2. Ejecutar el comando de la carpeta `theme-caba/scripts` que extrae los gastos ejecutados:
    ```
    $ python extractBudgetActual.py
    ```
    Si bien se van a regenerar los archivos **ejecucion_gastos.csv** para todos los años con información en la carpeta `input_actual`, los archivos preexistentes no deberían verse modificados.
    En caso de haber algún error en esta extracción del presupuesto, podrías suceder que el archivo `presupuesto-ejecutado-<añoN>-4Trimestre.csv`, contenga un gasto en una clasificación presupuestaria que no hubiera sido recogida con anterioridad en el archivo `presupuesto-sancionado-<añoN>.csv` del mismo año, por lo que estas clasificaciones deberán ser revisadas. En la carpeta `theme-caba/data/provincia/añoN` deberá verse ahora un archivo **ejecucion_gastos.csv**.

3. Cargar los datos que se acaban de generar desde la raíz del proyecto de presupuestos
    ```
    $ python manage.py load_execution añoN
    ```

4. Eliminar la caché de la aplicación para que vuelva a hacer las queries a la BD y traiga también los datos que acabamos de agregar.
    ```
    $ python manage.py remove_cache
    ```
    Para hacer esta operación también podemos ejecutar el comando de django:
    ```
    $ python manage.py clear_cache
    ```
    Pero este segundo comando no informará de si ha habido algún error y no ha podido borrar la carpeta de caché de la aplicación.

### 2. Añadir datos de sanción de un nuevo añoN 

Al tratarse de un nuevo año necesitamos obtener primero las clasificaciones para ese año, y luego extraer las partidas presupuestarias. Para que la aplicación pueda mostrar el gráfico Sankey de la visión global y el treemap de recursos de la sección de detalle, deberíamos disponer también de datos de ingresos para el añoN.

1. Colocar el archivo `presupuesto-sancionado-<añoN>.csv` en el directorio `input` de `theme-caba/scripts`. Fijarse en que la linea de títulos no tenga espacios en blanco (porque leemos con csvdictkitreader). Además los archivos deben ser UTF-8, los podemos transformar con Sublime (guardar con encoding).  

2. Ejecutar el comando de la carpeta `theme-caba/scripts` que extrae las clasificaciones presupuestarias:
    ```
    $ python extractClassifications.py
    ```
    Si bien se van a regenerar los archivos de clasificación para todos los años con información en la carpeta `input`, los archivos preexistentes no deberían verse modificados.
    Deberá aparecer ahora una carpeta `theme-caba/data/provincia/añoN` donde deberán encontrarse los archivos:
    * **finalidad_clas.csv**
    * **fuente_fin_clas.csv**
    * **jurisdiccion_clas.csv**
    * **programa_clas.csv**
    * **ubicacion_geografica_clas.csv**

3. Introducir a mano las clasificaciones económicas del añoN, en principio, las mismas que se crearon para los años anteriores deberían seguir siendo válidas. Simplemente copiar el archivo **economico_clas.csv** de cualquiera de los años anteriores en la carpeta `theme-caba/data/provincia/añoN` cambiando el valor de la columna "ejercicio" al nuevo añoN.

4. Ejecutar el comando de la carpeta `theme-caba/scripts` que extrae los gastos:
    ```
    $ python extractBudget.py
    ```
    Si bien se van a regenerar los archivos **gastos.csv** para todos los años con información en la carpeta `input`, los archivos preexistentes no deberían verse modificados.

5. Crear el archivo **ingresos.csv**, la información de que disponemos actualmente no presenta información de ingresos para años posteriores al 2015 por lo que se debería solicitar esta información al Gobierno de la Ciudad.

6. En caso de disponer también de los datos de ejecución del añoN, ver los pasos del apartado anterior (Añadir datos de ejecución del 4to trimestre del añoN).

7. Cargar los datos que se acaban de generar desde la raíz del proyecto de presupuestos
    ```
    $ python manage.py load_budget añoN
    ```
8. Al estar introduciendo un año nuevo en la aplicación deberemos añadir también datos de inflación y población para ese año por lo que deberemos actualizar de manera correspondiente los archivos **inflacion.csv** y **poblacion.csv** de la carpeta `theme-caba/data/provincia`, y ejecutar edepués el comando siguiente desde la raíz del proyecto de presupuestos:
    ```
    $ python manage.py load_stats
    ```

9. Eliminar la caché de la aplicación para que vuelva a hacer las queries a la BD y traiga también los datos que acabamos de agregar.
    ```
    $ python manage.py remove_cache
    ```
    Para hacer esta operación también podemos ejecutar el comando de django:
    ```
    $ python manage.py clear_cache
    ```
    Pero este segundo comando no informará de si ha habido algún error y no ha podido borrar la carpeta de caché de la aplicación.


### 3. Actualizar la información complementaria
#### Modificación del glosario
1. Actualizar el archivo **glosario.csv** de la carpeta `theme-caba/data/provincia` 
2. Ejecutar el comando siguiente desde la raíz del proyecto de presupuestos:

    ```
    $ python manage.py load_glossary
    ``` 
3. Eliminar la caché de la aplicación para que vuelva a hacer las queries a la BD y traiga también los datos que acabamos de agregar.

    ```
    $ python manage.py remove_cache
    ```

#### Modificación de datos de población o de inflación.
1. Actualizar los archivos **inflacion.csv** y **poblacion.csv** de la carpeta `theme-caba/data/provincia` 
2. Ejecutar el comando siguiente desde la raíz del proyecto de presupuestos:

    ```
    $ python manage.py load_stats
    ``` 
3. Eliminar la caché de la aplicación para que vuelva a hacer las queries a la BD y traiga también los datos que acabamos de agregar.

    ```
    $ python manage.py remove_cache
    ```
