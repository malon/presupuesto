# -*- coding:utf-8 -*-
# THIS IS A TEST FABRIC SCRIPT, IT IS NOT YET FINISHED
# steps to complete:
# update requirements.txt, fabric need to be included, which includes
# ecdsa, pycrypto, paramiko, fabric
# also, check requests in requirements.txt is it needed?
# 1)descargar csv de datos
# http://data.buenosaires.gob.ar/dataset/presupuesto-ejecutado/resource/00f80b2d-9b56-4125-9e68-2517c7da51e9
# colocar archivo presupuesto-ejecutado-<anhoN>-4Trimestre.csv 
# en el directorio input_actual 
# de theme-caba/scripts

# 2)fijarse que la línea de títulos no tenga espacios en blanco
# cambiar formato del archivo a UTF-8

# 3)ejecutar
# $ cd theme-caba/scripts
# $ python extractBudgetActual.py
# Debería haber en theme-caba/data/provincia/añoN 
# un archivo ejecucion_gastos.csv.

# 4)pushearlo al repo
# 5)descargar desde un servidor
# 6)desde la raíz del proyecto en el servidor
# $ python manage.py load_execution añoN

# 7)desde el mismo servidor borrar la cache
# $ python manage.py remove_cache

#8) repetir el borrado de cache en el segundo servidor


from __future__ import with_statement
from fabric.api import *
import fabric.contrib.project as project
from fabric.context_managers import lcd, cd
import os
import sys
import SimpleHTTPServer
import SocketServer
import shutil

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'
CURRENT_PATH = os.path.dirname(__file__)


AD_E = 'https://recursos-data.buenosaires.gob.ar/ckan2/presupuesto-ejecutado/'
AD_B = 'https://recursos-data.buenosaires.gob.ar/ckan2/presupuesto-sancionado/'
DIR_E = 'theme-caba/scripts/input_actual'
DIR_B = 'theme-caba/scripts/input'
DIR_E_test = 'test/input_actual'
DIR_B_test = 'test/input'

# EXECUTED_FILE_NAME_ = "presupuesto-ejecutado-2015-3Trimestre.csv"
# BUDGETED_FILE_NAME = "presupuesto-sancionado-2015.csv"


def get_ejecucion(year):
    directory = DIR_E_test
    address = AD_E
    filename = 'presupuesto-ejecutado-%d-4Trimestre.csv' % int(year)
    get_file(directory, address, filename)


def get_sancion(year):
    directory = DIR_B_test
    address = AD_B
    filename = 'presupuesto-sancionado-%d.csv' % int(year)
    get_file(directory, address, filename)


def get_file(directory, address, filename):
    with settings(warn_only=True):
        with lcd('%s/%s' % (CURRENT_PATH, directory)):
            conn = 'wget %s%s' % (address, filename)
            print 'Descargando: %s en carpeta %s' % (conn, directory)
            result = local(conn, capture=True)
            if result.failed:
                abort("La descarga de %s ha fallado, proceso interrumpido." % filename)
            else:
                convert_to_utf8(filename)


# def change_file(year):
#     with f = open('presupuesto-sancionado-'+year+'.csv', 'r+').read():
#         line = f.readline()
#         f.seek(0)
#         f.write(line.strip) 


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


def build():
    local('pelican -s pelicanconf.py')


def rebuild():
    clean()
    build()


def regenerate():
    local('pelican -r -s pelicanconf.py')

def serve():
    os.chdir(env.deploy_path)

    PORT = 8000
    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()


def reserve():
    build()
    serve()


def preview():
    local('pelican -s publishconf.py')


def cf_upload():
    rebuild()
    local('cd {deploy_path} && '
          'swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
          '-U {cloudfiles_username} '
          '-K {cloudfiles_api_key} '
          'upload -c {cloudfiles_container} .'.format(**env))


@hosts(production)
def publish():
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        extra_opts='-c',
    )


def publishghp(msg):
    preview() #builds publishconf.py
    local("git add -A") #will commit allll files, be careful
    local("git commit -m '%s'"%msg)
    local("ghp-import -m '%s' -b gh-pages output"%msg)
    local("git push --all")




def convert_to_utf8(filename):
    # code by https://gomputor.wordpress.com/2008/09/22/convert-a-file-in-utf-8-or-any-encoding-with-python/
    # gather the encodings you think that the file may be
    # encoded inside a tuple
    encodings = ('windows-1252', 'windows-1253', 'iso-8859-7')
 
    # try to open the file and exit if some IOError occurs
    try:
        f = open(filename, 'r').read()
    except Exception:
        sys.exit(1)
 
    # now start iterating in our encodings tuple and try to
    # decode the file
    for enc in encodings:
        try:
            # try to decode the file with the first encoding
            # from the tuple.
            # if it succeeds then it will reach break, so we
            # will be out of the loop (something we want on
            # success).
            # the data variable will hold our decoded text
            data = f.decode(enc)
            break
        except Exception:
            # if the first encoding fail, then with the continue
            # keyword will start again with the second encoding
            # from the tuple an so on.... until it succeeds.
            # if for some reason it reaches the last encoding of
            # our tuple without success, then exit the program.
            if enc == encodings[-1]:
                sys.exit(1)
            continue
 
    # now get the absolute path of our filename and append .bak
    # to the end of it (for our backup file)
    fpath = os.path.abspath(filename)
    newfilename = fpath + '.bak'
    # and make our backup file with shutil
    shutil.copy(filename, newfilename)
 
    # and at last convert it to utf-8
    f = open(filename, 'w')
    try:
        f.write(data.encode('utf-8'))
    except Exception, e:
        print e
    finally:
        f.close()