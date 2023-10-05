from pathlib import Path
import os
from utils.enviroment import parse_separar_virgula_str_to_list, get_env_variaveis

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSEGURO')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == 'S' else False

ALLOWED_HOSTS: list[str] = parse_separar_virgula_str_to_list(get_env_variaveis('ALLOWED_HOSTS'))
CSRF_TRUSTED_ORIGINS: list[str] = parse_separar_virgula_str_to_list(get_env_variaveis('CSRF_TRUSTED_ORIGINS'))

ROOT_URLCONF = 'receitas.urls'

WSGI_APPLICATION = 'receitas.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
