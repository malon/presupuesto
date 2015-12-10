# ENVIRONMENT-SPECIFIC SETTINGS
#

ENV = {

  'THEME': 'theme-caba',

  'DEBUG': True,
  'TEMPLATE_DEBUG': True,

  # Database
  'DATABASE_NAME': 'presupuestos_caba',
  'DATABASE_USER': 'postgres',
  'DATABASE_PASSWORD': 'postgres',
  'DATABASE_URL': 'postgres://postgres:postgres@localhost:5432/presupuestos_caba',
#  'SEARCH_CONFIG': 'unaccent_spa',

  # Caching
 'CACHES': {
     'default': {
         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
         'LOCATION': '/tmp'
     }
 }

}
