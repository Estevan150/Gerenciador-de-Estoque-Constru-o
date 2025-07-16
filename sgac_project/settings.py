# sgac_project/settings.py - Versão Completa e Final

from pathlib import Path
from decouple import config
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

INSTALLED_APPS = [
    'jazzmin',
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'usuarios.User'
AUTHENTICATION_BACKENDS = ['usuarios.backends.StatusCheckBackend']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- CONFIGURAÇÕES DE LOGIN E REDIRECIONAMENTO ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'


# --- CONFIGURAÇÕES DO TEMA JAZZMIN ---
# (no final do seu settings.py)

# --- CONFIGURAÇÕES AVANÇADAS DO TEMA JAZZMIN ---
# sgac_project/settings.py

# --- CONFIGURAÇÕES FINAIS DO TEMA JAZZMIN ---

JAZZMIN_SETTINGS = {
    "site_title": "SGAC Admin",
    "site_header": "SGAC-CRPJ",
    "site_brand": "",  # Deixamos em branco para mostrar apenas o logo
    "site_logo": "images/logo.png",
    "welcome_sign": "Bem-vindo ao Painel de Controle SGAC",
    "copyright": "CRPJ Empreendimentos",
    "order_with_respect_to": ["estoque", "usuarios", "auth"],
    "custom_css": "css/admin_custom.css", 
    "icons": {
        "auth": "fas fa-users-cog",
        "usuarios.User": "fas fa-user",
        "estoque.Material": "fas fa-box",
        "estoque.NotaFiscalEntrada": "fas fa-file-invoice-dollar",
        "estoque.SaidaMaterial": "fas fa-dolly",
        "estoque.Requisicao": "fas fa-clipboard-list",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "brand_colour": "#8B2E2E",
    "accent": "#E8B655",
    "primary": "#E8B655",
    "secondary": "#6c757d",
    "info": "#8B2E2E", # Usando o vermelho da marca para os botões "Modificar"
    "success": "#E8B655", # Usando o dourado para os botões "Adicionar"
    "warning": "#ffc107",
    "danger": "#dc3545",
    "rounded_corners": True,
}
