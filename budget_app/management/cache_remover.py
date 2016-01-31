# -*- coding: UTF-8 -*-
import shutil
from os.path import exists
from django.conf import settings


class CacheRemover:

    def remove(self):
        if exists(settings.CACHE_DIR):
            print "Borrando carpeta de cache en %s" %(settings.CACHE_DIR)
            shutil.rmtree(settings.CACHE_DIR)
        else:
            print "No se encuentra carpeta de cache %s" %(settings.CACHE_DIR)
