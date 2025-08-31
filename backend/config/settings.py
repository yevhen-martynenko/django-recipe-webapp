import os
from pathlib import Path
import environ


# load environment
env = environ.Env()
env_file_path = os.path.join(os.path.dirname(__file__), '../.env')
environ.Env.read_env(env_file_path)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Use environment variables
DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env('SECRET_KEY', default='default-secret-key')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition
INSTALLED_APPS = [
    # local
    'apps.core',
    'apps.users',
    'apps.recipes',

    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'rest_framework',
    'manifest_loader',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'corsheaders',
]

MIDDLEWARE = [
    # custom
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    # default
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'config.urls'
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database' / 'db.sqlite3',
    }
}


# Password validation
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


CSRF_TRUSTED_ORIGINS = [
    "https://alpaca-quick-satyr.ngrok-free.app",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

CORS_ALLOWED_ORIGINS = [
    "https://alpaca-quick-satyr.ngrok-free.app",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom
AUTH_USER_MODEL = "users.User"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7


MANIFEST_LOADER = {
    'manifest_file': os.path.join(BASE_DIR, 'static/manifest.json'),
}
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


auth_classes = [
    'rest_framework.authentication.SessionAuthentication',
    'apps.users.authentication.TokenAuthentication',
]
if DEBUG:
    auth_classes = [
        'rest_framework.authentication.SessionAuthentication',
        'apps.users.authentication.TokenAuthentication',
    ]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '6/hour',
    },
}

FRONTEND_AFTER_GOOGLE_LOGIN_URL = env('FRONTEND_AFTER_GOOGLE_LOGIN_URL')
ACTIVATION_LINK_URL = env('ACTIVATION_LINK_URL')
PASSWORD_RESET_URL = env('PASSWORD_RESET_URL')


# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_TIMEOUT = 60
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
SERVER_EMAIL = env('EMAIL_HOST_USER')


# Google
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_LOGIN_METHODS = {'email'}
# ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*']

GOOGLE_OAUTH2_CLIENT_ID = env('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = env('GOOGLE_OAUTH2_CLIENT_SECRET')
GOOGLE_OAUTH2_CALLBACK_URL = env('GOOGLE_OAUTH2_CALLBACK_URL')


# Allauth
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APPS': [
            {
                'client_id': GOOGLE_OAUTH2_CLIENT_ID,
                'secret': GOOGLE_OAUTH2_CLIENT_SECRET,
                'key': '',
            },
        ],
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    }
}
SITE_ID = 1
