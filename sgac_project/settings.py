# sgac_project/settings.py

from pathlib import Path
from decouple import config
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURAÇÃO DE SEGURANÇA COM DECOUPLE ---
# A SECRET_KEY e o DEBUG agora são lidos do arquivo .env ou do ambiente do servidor.
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
# ---------------------------------------------

# --- CONFIGURAÇÃO DE PRODUÇÃO: ALLOWED_HOSTS ---
# Lê os hosts permitidos do .env. No servidor (Render), vamos adicionar o endereço do nosso site.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
# ---------------------------------------------


# Application definition
INSTALLED_APPS = [
    'usuarios',
    'estoque',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # --- CONFIGURAÇÃO DE PRODUÇÃO: WHITENOISE ---
    # O Whitenoise deve vir logo após o SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ---------------------------------------------
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sgac_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sgac_project.wsgi.application'

# --- CONFIGURAÇÃO DE PRODUÇÃO: BANCO DE DADOS ---
# Usa a biblioteca dj_database_url para ler a configuração do banco
# a partir da variável de ambiente DATABASE_URL.
# Para desenvolvimento local, ele usará o nosso db.sqlite3 como padrão.
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
# -----------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True

# --- CONFIGURAÇÃO DE PRODUÇÃO: ARQUIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Diretório para onde o comando 'collectstatic' irá copiar todos os arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Configuração de armazenamento do Whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# ----------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'usuarios.User'
AUTHENTICATION_BACKENDS = ['usuarios.backends.StatusCheckBackend']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'