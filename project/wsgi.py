"""
WSGI config for project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))
#production path to append
sys.path.append(os.path.join(BASE_DIR, '../../env_presupuestos/lib/python2.7/site-packages'))


os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from django.core.wsgi import get_wsgi_application
# HEROKU CONFIGURATION
# from dj_static import Cling

# application = Cling(get_wsgi_application())
application = get_wsgi_application()
