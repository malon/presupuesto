
# TUTORIAL DE DATOS
## Formato de los datos de entrada

Los datos de entrada que maneja la aplicación ¿Dónde van mis impuestos? son una serie de archivos CSV con un formato y estructura determinados, que debería respetarse para el correcto funcionamiento de la aplicación. Estos datos se cargan en la BD del proyecto por medio de una serie de comandos de carga que se explican en el documento de instalación [INSTALL.md](../INSTALL.md). Un ejemplo de estos comandos de carga sería:
    
    $ python manage.py load_budget 2014

Para que estos comandos funcionen, los datos deben estar almacenados en la carpeta `theme-caba/data`. Existen una serie de datos comunes a la aplicación que denominamos **archivos de información extra** que se encontrarán en la raíz de la carpeta `data` y una serie de archivos con datos específicos para una entidad geográfica concreta (**archivos de clasificación** y **archivos de partidas presupuestarias**). La entidad en este caso es la provincia de CABA, pero podríamos tener más entidades a la vez representadas en la misma aplicación, Por tanto los datos específicos de CABA deberán estar dentro de una carpeta denominada en este caso `theme-caba/data/provincia`. Explicaremos por qué la palabra "provincia" más adelante.


###Archivos de información extra###
Son una serie de archivos CSV que no deberían tener espacios ni líneas en blanco. Estos archivos son:
* **entidades.csv**: contiene la lista de entidades geográficas que se van a representar, con el formato del ejemplo: 

    > [id],[nivel],[nombre]  
    > AR1,estado,Argentina  
    > 01,provincia,CABA

    En nuestro ejemplo tenemos dos entidades, Argentina y CABA. Aunque en estos momentos solamente estamos usando CABA. 

    * *id* que será escogido por nosotros, en nuestro caso 'AR1' para el país (por si en un futuro queremos incluir datos del país), y '01' para la provincia CABA que coincide id usado por el gobierno para las elecciones.
    * *nivel* de la entidad, en nuestro ejemplo estado y provincia.
    * *nombre* de la entidad geográfica.


    Tanto [nivel] como [nombre] deberán ser referenciados con las siguientes variables (que en nuestro caso se encuentran en el archivo presupuestos/theme-caba/settings.py):
    
    > MAIN_ENTITY_LEVEL = 'provincia'  
    > MAIN_ENTITY_NAME = 'CABA'

    Precisamente [nivel], que en nuestro caso es 'provincia', es el nombre de la carpeta en la que, como explicamos antes, debemos almacenar los **archivos de clasificación** y los **archivos de partidas presupuestarias**  
         
        

* **glosario.csv**: contiene los términos que aparecen en la pestaña *¿Qué significa?* de la aplicación. Debe contener líneas con el formato del siguiente ejemplo: 

    > [título],[descripción]  
    > "Jurisdicción","Son las organizaciones públicas...

* **inflacion.csv**: contiene los valores de la inflación interanual. Debe contener líneas con el formato del siguiente ejemplo: 

    > [año],[inflación]  
    > 2012,1  
    > 2013,26.6  
    > 2014,38.0   
    > 2015,0    


    El año en curso aparecerá con un cero, ya que para el año actual no tenemos en cuenta la inflación. Si el primer año representado es el N, debemos tener un valor para N-1 (en nuestro ejemplo 2012), el valor que tenga ese año no nos importa ya que no se tendrá en cuenta al no representarse ese año, pero la línea debe aparecer en el archivo. A partir de los índices generales de la inflación proporcionados por el Gobierno (ver apartado Fuentes de Datos) calculamos la tasa anual como la media de las tasas interanuales durante los 12 meses del año. Para ello hacemos la siguiente operación:
    
        inflación_2014 = ((indice_dec-14 / indice_dec-13) - 1 ) * 100

    Así para los siguientes índices generales:

    fecha | índice_general
    --- | --- 
    dec-12 | 122.48 
    dec-13 | 155.06 
    dec-14 | 214.04

    El contenido del archivo debería coincidir con el del archivo de ejemplo presentado más arriba.
            

    La forma en que se aplica la inflación a los años anteriores al actual es la siguiente, se calcula internamente un índice de inflación con la siguiente fórmula:

        indice_año_N-1 = indice_año_N / (1+inflacion_año_N)

    siendo el índice del primer año 100, por lo que obtendríamos los siguientes índices:

    año | inflación | índice_interno
    --- | --- | ---
    2015 | 0 | 100
    2014 | 38 | 100/(1+(0/100)) = 100
    2013 | 26.6 | 100/(1+(38/100))
    2012 | 1 | 100/(1+(26.6/100))

    Para ajustar los valores a la inflación, se usa el índice del año anterior al que se está calculando, así:
    
        ajustado_N = (original_N / index_N-1) * 100

    Resultando en este ejemplo:

        ajustado_2015 = original_2015
        ajustado_2014 = original_2014 * (1 + 0.38)  : un 38% más que el valor original
        ajustado_2013 = original_2013 * (1 + 0.38) * (1 + 0.266) : aplicamos un 38% más y un 26.6% más


* **poblacion.csv**: contiene las estadísticas poblacionales con el formato: 

    > [id_entidad],[nombre_entidad],[año],[habitantes]    
    > 01,Caba,2013,2890151  
    > 01,Caba,2014,2890151  
    > 01,Caba,2015,2890151  



###Archivos de clasificación###
Contienen datos de cada categoría con la que representamos el presupuesto, los niveles que la componen y los identificadores de cada uno de esos niveles. El formato es común a todos, usando ";" como separador. La primera línea, la de títulos, empieza por "ejercicio" (año de esa clasificación) y continúa con el nombre de cada uno de los niveles de la categoría, en orden descendiente, mostramos como ejemplo el archivo `jurisdiccion_clas.csv` en cuyo caso los niveles son "jurisdicción", "servicio" y "unidad_ejecutora". Los niveles están anidados, es decir, una jurisdicción tiene uno o varios servicios, y un servicio una o varias unidades_ejecutoras, del mismo modo sus identificadores también se anidan, como veremos en el ejemplo. Por último se incluye una descripción de ese nivel.Cuando una línea tenga información de, por ejemplo, el nivel "servicio", tendrá en blanco la columna "unidad_ejecutora", lo cual se representa de esta manera: ";;", sin espacios en blanco. Es muy importante que los títulos no contengan espacios en blanco, ni antes ni después de ";", ni líneas en blanco. Además el formato de los archivos debe ser UTF-8, de no ser así se pueden transformar, por ejemplo con el editor sublime. Veamos un ejemplo:


> ejercicio;jurisdiccion;servicio;unidad_ejecutora;descripcion  (esta línea debe estar también)    
> 2013;01;01001;010010010;SECRETARIA ADMINISTRATIVA  
> 2013;01;01001;;LEGISLATURA CABA  
> 2013;01;;;LEGISLATURA DE LA CIUDAD DE BUENOS AIRES  
> ...  

Ejemplo de identificador anidado (contiene identificadores de sus niveles superiores):

    unidad_ejecutora = SECRETARIA ADMINISTRATIVA 
    010010010  : 9 dígitos en total
    01+001+0010: 2 para jurisdicción + 3 para servicio + 4 para unidad_ejecutora

    servicio = LEGISLATURA DE CABA
    01001 : 5 dígitos en total
    01+001: 2 para jurisdicción + 3 para servicio

    jurisdicción = LEGISLATURA DE LA CIUDAD DE BUENOS AIRES 
    01 : 2 dígitos en total


La lista de archivos de clasificación se muestra a continuación, veremos como se pueden generar y alguna particularidad de alguno de ellos más adelante:

* **economico_clas.csv**: clasificación económica
* **finalidad_clas.csv**: clasificación por finalidad y función
* **fuente_fin_clas.csv**: clasificación por fuente de financiamiento
* **jurisdiccion_clas.csv**: clasificación por jurisdicción
* **programa_clas.csv**: clasificación por programa (no se usa esta categoría de momento)
* **ubicacion_geografica_clas.csv**: clasificación por ubicación geográfica (no se usa esta categoría de momento)

###Archivos de partidas presupuestarias###
Al igual que los **archivos de clasificación** tienen un formato fijo que se debe respetar. Estos archivos muestran las diferentes partidas presupuestarias de gastos e ingresos categorizadas según los clasificadores cuyos archivos explicamos con anterioridad. Al igual que en el anterior caso, usamos ";" como separador, y la línea de títulos empezará por "EJERCICIO" (año de esa partida presupuestaria), y continuará por cada una de las clasificaciones que usaremos, utilizando para cada clasificación el identificador del nivel inferior de la clasificación correspondiente. Por ejemplo para "jurisdicción", usaremos el identificador de la "unidad ejecutora", ya que este identificador, como vimos con anterioridad, lleva información también de a qué "servicio" y a que "jurisdicción" pertenece. Por último se incluye una descripción de la partida (este campo no es importante ya que las descripciones que se verán en la aplicación serán las de las clasificaciones presupuestarias) y la cantidad sancionada en el campo "SANCIONADO" o ejecutada en el campo "DEVENGADO". 

Vemos, por ejemplo el contenido de `gastos.csv`:

> EJERCICIO;CENTRO GESTOR;FUNCIONAL;ECONOMICA;FINANCIACION;DESCRIPCION;SANCIONADO
> 2013;010010010;11;120;11;Retribución del cargo;247000000
> 2013;010010010;11;120;11;Sueldo anual complementario;20000000

Un ejemplo de `ejecucion_gastos.csv`:

> EJERCICIO;CENTRO GESTOR;FUNCIONAL;ECONOMICA;FINANCIACION;DESCRIPCION;DEVENGADO
> 2013;010010010;11;120;11;Retribución del cargo;274489487.94
> 2013;010010010;11;120;11;Sueldo anual complementario;23739333.22

Y un ejemplo de `ingresos.csv`:

> EJERCICIO;CENTRO GESTOR;FUNCIONAL;ECONOMICA;FINANCIACION;DESCRIPCION;SANCIONADO
> 2013;;;111;;Impuestos Directos;5147268000
> 2013;;;112;;Impuestos Indirectos;28059918400

Estos son los tres archivos utilizados, el archivo de ejecución no es obligatorio, y esas cantidades no serán mostradas si no se dispone de ellas o serán mostradas en blanco en la aplicación.

* **gastos.csv**: partidas de gasto presupuestado (sanción de ley)
* **ejecucion_gastos.csv**: partidas de gasto ejecutado
* **ingresos.csv**: partidas de recursos


## Fuentes de datos

Los archivos anteriormente mencionados son extraídos a partir de la información facilitada por el Gobierno de la Ciudad de Buenos Aires a través de las siguiente fuentes:

* Gastos presupuestados (sanción de ley): Portal de datos de Buenos Aires, [presupuesto sancionado][2]
* Gastos ejecutados: Portal de datos de Buenos Aires, [presupuesto ejecutado][3] hemos tomado el dato del cuarto cuatrimestre para años finalizados solamente.
* Ingresos (recursos): Página de estadística presupuestaria,[clasificación por carácter económico][4] 
* Clasificadores de gastos: obtenidos a partir de los gastos presupuestados.
* Clasificadores económicos de gastos y recursos: obtenidos a mano a partir de [documento de clasificadores, año 2009][1]
* Datos de inflación y población: obtenidos de la [Dirección General de Estadística y Censos - Ministerio de Hacienda GCBA][7]

## Procesado de los datos fuente

A partir de los CSVs de gastos y el PDF de recursos debemos obtener los archivos de entrada antes mencionados. En el caso de los gastos esto se hace de manera automática, pero para los ingresos, tratándose de un PDF de escaso tamaño lo hemos hecho de forma manual. Para el procesado automático se utilizan los scripts ubicados en `theme-caba/scripts`

### 1. Obteniendo los archivos de clasificación

Obtenemos estos datos a partir de los archivos del presupuesto sancionado. Estos archivos, de nombre `presupuesto-sancionado-<año>.csv` deben estar almacenados en la carpeta `input` de `theme-caba/sripts`.

Si ejecutamos el siguiente script:

    $ python extractClassifications.py

Obtendremos un resultado similar a lo siguiente:

    Processing 10000 lines for year 2014
    Processing 20000 lines for year 2014
    Processing 30000 lines for year 2014
    Processing 40000 lines for year 2014
    Processing 50000 lines for year 2014
    Processing 10000 lines for year 2015
    Processing 20000 lines for year 2015
    Processing 30000 lines for year 2015
    Processing 40000 lines for year 2015
    Processing 10000 lines for year 2013
    Processing 20000 lines for year 2013
    Processing 30000 lines for year 2013
    Processing 40000 lines for year 2013
    Processing 50000 lines for year 2013
    Entidades completadas ['jurisdiccion', 'servicio', 'unidad_ejecutora', 'programa', 'subprograma', 'proyecto', 'ubicacion_geografica', 'finalidad', 'funcion', 'fuente_fin']


En este caso se han procesado tres años (2013, 2014 y 2015) para los cuales se han encontrado las entidades que se detallan. Esto quiere decir que se han creado las siguientes carpetas, en caso de no existir:

    theme-caba/data/provincia/2013/
    theme-caba/data/provincia/2014/
    theme-caba/data/provincia/2015/

Y dentro de cada una de ellas se han creado los archivos de clasificación que contienen esas entidades, es decir:

* **finalidad_clas.csv**: contiene dos niveles de la clasificación de finalidad: finalidad y función.
* **fuente_fin_clas.csv**: contiene el clasificador fuente_fin.
* **jurisdiccion_clas.csv**: contiene tres niveles de la clasificación jurisdiccional: jurisdicción, servicio y unidad_ejecutora.
* **programa_clas.csv**: contiene tres niveles de la clasificación por programa: programa, subprograma y proyecto (no se usa esta categoría de momento).
* **ubicacion_geografica_clas.csv**: contiene el clasificador ubicación_geográfica (no se usa esta categoría de momento).

El archivo **economico_clas.csv**, es un caso especial. Ya que en los datos que proporciona el gobierno esta categoría aparece agrupada en un único clasificador con el nombre `clas_economico`, es decir no se desagrega este clasificador en ninguno de sus niveles anidados, por lo que se ha tenido que hacer esa desgraguegación en niveles de manera manual, obteniendo los datos de los diferentes niveles de esta clasificación y sus identificadores del siguiente [documento][1] proporcionado por el ministerio de Hacienda de la Ciudad. Cabe señalar que hay dos clasificaciones, una para los gastos y otra para los ingresos, ambas se encuentran en el mismo archivo **economico_clas.csv**, diferenciándose por la columna gasto/ingreso con los valores "G" e "I". Los niveles que se presentan para esta clasificación los hemos denominado *chapter*, *article* y *heading*.



### 2. Obteniendo los archivos de partidas presupuestarias

#### Archivo de partidas de gasto presupuestado `gastos.csv`

Obtenemos un archivo **gastos.csv** para cada año con el que estamos trabajando a partir de los archivos del presupuesto sancionado. Estos archivos, de nombre `presupuesto-sancionado-<año>.csv`, deben estar almacenados en la carpeta `input` de `theme-caba/sripts`.
Si ejecutamos el siguiente script:

    $ python extractBudget.py

No debería presentarse ninguna salida, pero deberíamos ver que en cada una de las carpetas:

    theme-caba/data/provincia/2013/
    theme-caba/data/provincia/2014/
    theme-caba/data/provincia/2015/

Tenemos un archivo **gastos.csv** con las partidas presupuestarias de gastos de ese año clasificadas por cada una de las categorías que estamos utilizando. La cabecera de dicho archivo debería tener el siguiente formato:

    EJERCICIO;CENTRO GESTOR;FUNCIONAL;ECONOMICA;FINANCIACION;DESCRIPCION;SANCIONADO


#### Archivo de partidas de gasto ejecutado `ejecucion_gastos.csv`

Obtenemos un archivo **ejecucion_gastos.csv** para cada año con el que estamos trabajando a partir de los archivos del presupuesto ejecutado. Estos archivos, de nombre `presupuesto-ejecutado-<año>-4Trimestre.csv`, deben estar almacenados en la carpeta `input_actual` de `theme-caba/sripts`.
Si ejecutamos el siguiente script:

    $ python extractBudgetActual.py

No debería presentarse ninguna salida, pero deberíamos ver que en cada una de las carpetas:

    theme-caba/data/provincia/2013/
    theme-caba/data/provincia/2014/
    theme-caba/data/provincia/2015/

Tenemos un archivo **ejecucion_gastos.csv** con las partidas presupuestarias de gastos de ese año clasificadas por cada una de las categorías que estamos utilizando. La cabecera de dicho archivo debería tener el siguiente formato:
    
    EJERCICIO;CENTRO GESTOR;FUNCIONAL;ECONOMICA;FINANCIACION;DESCRIPCION;DEVENGADO


#### Archivo de partidas de recursos `ingresos.csv`

Ya que el [portal de datos][5] del gobierno e la Ciudad de Buenos Aires no dispone de datos sobre los recursos o ingresos de la ciudad, hemos obtenido estos datos a través de PDFs de la [página de estadística presupuestaria][6] del Ministerio de Hacienda de la Ciudad, en concreto del [documento][4] que muestra la clasificación por carácter económico de los ingresos entre los años 2005 y 2015. De manera manual se crearon los archivos de `ingresos.csv` para los años 2013, 2014 y 2015, a partir de dicho de documento, el cual muestra los datos en miles de pesos, mientras que en el archivo csv deben anotarse en pesos. 



[1]: http://www.buenosaires.gob.ar/areas/hacienda/pdf/resolucion_1280_mhgc_09_clasificadores.pdf
[2]: http://data.buenosaires.gob.ar/dataset/presupuesto-sancionado
[3]: http://data.buenosaires.gob.ar/dataset/presupuesto-ejecutado
[4]: http://www.buenosaires.gob.ar/sites/gcaba/files/recursos_totales_-_clasificacion_por_caracter_economico_2005-2015.pdf
[5]: http://data.buenosaires.gob.ar/
[6]: http://www.buenosaires.gob.ar/hacienda/presupuesto/estadistica-presupuestaria
[7]: http://www.estadisticaciudad.gob.ar/eyc/?p=47752