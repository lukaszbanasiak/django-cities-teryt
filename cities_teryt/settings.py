from django.conf import settings

from os.path import abspath, dirname, join, normpath

APP_ROOT = dirname(abspath(__file__))
IMPORT_ROOT = normpath(join(APP_ROOT, 'import'))

IMPORT_DIR = getattr(settings, 'CITIES_TERYT_IMPORT_DIR', IMPORT_ROOT)
