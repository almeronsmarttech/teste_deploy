import os
from pathlib import Path
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#configuração de carregamento do arquivo
load_dotenv(os.path.join(BASE_DIR,'.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = os.environ.get("DEBUG","False") == True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps externas
    'tailwind',
    'theme',
    'django_browser_reload',
    'django_htmx',
    #'django_bootstrap5',
        # Allauth
        # Add these
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # minhas apps
    'apps.app',
    'apps.calculadora',
    'apps.menu1',
    'apps.menu2',
    'apps.loginapp',
]

#ALLOWED_HOSTS = ["almeronsmarttech.com.br","www.almeronsmarttech.com.br","almeron.com.br","www.almeron.com.br","sea-lion-app-zxare.ondigitalocean.app"]
#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS","*").split(" ")
#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS","*").split(",")
ALLOWED_HOSTS = []
# Application definition

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #Allauth
    # This one
    "allauth.account.middleware.AccountMiddleware",
    # htmx
    'django_htmx.middleware.HtmxMiddleware',
    # reload tailwindo
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'src.urls'

TAILWIND_APP_NAME = 'theme'

#NPM_BIN_PATH = "/usr/local/bin/npm"
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #BASE_DIR / "templates"
            BASE_DIR / 'src' / 'templates',
            os.path.join(BASE_DIR, "theme", "static"),  # Inclui o caminho do Tailwind
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # AllAuth
                # This one
               'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
   # Needed to login by user in admin, regardless of `allauth`
   'django.contrib.auth.backends.ModelBackend',

   # This one
   'allauth.account.auth_backends.AuthenticationBackend',
]
# AllAuth
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
   'google': {
       'APP': {
            'client_id': os.environ.get('CLIENT_ID_GOOGLE'),
            'secret': os.environ.get('SECRET_GOOGLE'),
           'key' : ''
           #'key': os.environ.get('API_KEY'),
       }
   }
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# AllAuth settings
SITE_ID = 1

SITE_URL = 'almeronsmarttech.com.br'
#USE_X_FORWARDED_HOST = True
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ACCOUNT_LOGIN_REDIRECT_URL ="/"
ACCOUNT_LOGOUT_REDIRECT_URL ="/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
ACCOUNT_LOGOUT_ON_GET = True

SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_LOGIN_ON_GET=True
SOCIALACCOUNT_AUTO_SIGNUP = True

WSGI_APPLICATION = 'src.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
DB_SLUG = os.environ.get("DB_SLUG","sqlite")

if DB_SLUG == "postgres":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME'),
                'USER': os.environ.get('DB_USERNAME'),
                'PASSWORD': os.environ.get('DB_PASSWORD'),
                'HOST': os.environ.get('DB_HOST'),
                'PORT': os.environ.get('DB_PORT'),
            }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticroot'
STATICFILES_DIRS = [BASE_DIR / 'static/',]

#TAILWIND_CSS_PATH = "static/css/dist/styles.css"  # Local onde o Tailwind salva o CSS gerado
#TAILWIND_CSS_PATH = "../theme/static/css/dist"  # Local onde o Tailwind salva o CSS gerado
TAILWIND_CSS_PATH = "css/dist/styles.css"  # O caminho relativo dentro do diretório static

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CAMPOS NECESSÁRIOS PARA A CUSTOMIZAÇÃO DOS USUÁRIOS

# Set custom user model as the active one
AUTH_USER_MODEL = 'app.MyCustomUser'

# Configure AllAuth username related management, because we are
# using the e-mail as username. See:
# https://docs.allauth.org/en/latest/account/advanced.html
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

#SESSION_COOKIE_AGE = 180 # 3 minutes. "1209600(2 weeks)" by default
SESSION_COOKIE_AGE = 7200 # 20 minutes. "1209600(2 weeks)" by default
SESSION_SAVE_EVERY_REQUEST = True # "False" by default

# CONFIGURAÇÕES DE E-MAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =  os.environ.get('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =  os.environ.get('EMAIL_SENHA')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

