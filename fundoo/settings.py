"""
Django settings for fundoo project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# from
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sze853$xnpyjr@2(z#t6bl+ub0d%ftlp*0v9b^ib&3t3lcsw9='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django_short_url',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'rest_framework_swagger',
    'rest_framework',
    'login',
    'note',
    'notes',
    'fun',
    'sociallogin',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.agave',
    # 'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.angellist',
    # 'allauth.socialaccount.providers.asana',
    # 'allauth.socialaccount.providers.auth0',
    # 'allauth.socialaccount.providers.authentiq',
    # 'allauth.socialaccount.providers.baidu',
    # 'allauth.socialaccount.providers.basecamp',
    # 'allauth.socialaccount.providers.bitbucket',
    # 'allauth.socialaccount.providers.bitbucket_oauth2',
    # 'allauth.socialaccount.providers.bitly',
    # 'allauth.socialaccount.providers.cern',
    # 'allauth.socialaccount.providers.coinbase',
    # 'allauth.socialaccount.providers.dataporten',
    # 'allauth.socialaccount.providers.daum',
    # 'allauth.socialaccount.providers.digitalocean',
    # 'allauth.socialaccount.providers.discord',
    # 'allauth.socialaccount.providers.disqus',
    # 'allauth.socialaccount.providers.douban',
    # 'allauth.socialaccount.providers.draugiem',
    # 'allauth.socialaccount.providers.dropbox',
    # 'allauth.socialaccount.providers.dwolla',
    # 'allauth.socialaccount.providers.edmodo',
    # 'allauth.socialaccount.providers.eveonline',
    # 'allauth.socialaccount.providers.evernote',
    # 'allauth.socialaccount.providers.exist',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.feedly',
    # 'allauth.socialaccount.providers.fivehundredpx',
    # 'allauth.socialaccount.providers.flickr',
    # 'allauth.socialaccount.providers.foursquare',
    # 'allauth.socialaccount.providers.fxa',
    'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.gitlab',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.hubic',
    # 'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.jupyterhub',
    # 'allauth.socialaccount.providers.kakao',
    # 'allauth.socialaccount.providers.line',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
    # 'allauth.socialaccount.providers.mailru',
    # 'allauth.socialaccount.providers.mailchimp',
    # 'allauth.socialaccount.providers.meetup',
    # 'allauth.socialaccount.providers.microsoft',
    # 'allauth.socialaccount.providers.naver',
    # 'allauth.socialaccount.providers.nextcloud',
    # 'allauth.socialaccount.providers.odnoklassniki',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.openstreetmap',
    # 'allauth.socialaccount.providers.orcid',
    # 'allauth.socialaccount.providers.paypal',
    # 'allauth.socialaccount.providers.patreon',
    # 'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.pinterest',
    # 'allauth.socialaccount.providers.reddit',
    # 'allauth.socialaccount.providers.robinhood',
    # 'allauth.socialaccount.providers.sharefile',
    # 'allauth.socialaccount.providers.shopify',
    # 'allauth.socialaccount.providers.slack',
    # 'allauth.socialaccount.providers.soundcloud',
    # 'allauth.socialaccount.providers.spotify',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.steam',
    # 'allauth.socialaccount.providers.strava',
    # 'allauth.socialaccount.providers.stripe',
    # 'allauth.socialaccount.providers.trello',
    # 'allauth.socialaccount.providers.tumblr',
    # 'allauth.socialaccount.providers.twentythreeandme',
    # 'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.untappd',
    # 'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.vimeo_oauth2',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.weibo',
    # 'allauth.socialaccount.providers.weixin',
    # 'allauth.socialaccount.providers.windowslive',
    # 'allauth.socialaccount.providers.xing',
    # 'allauth.socialaccount.providers.ynab',
    #
    # 'oauth2_provider',
    # 'authlib.little_auth',
    # 'social_django',
    # 'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'fundoo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'base.context_processors.add_variables_to_context',
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
            ],
        },
    },
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

WSGI_APPLICATION = 'fundoo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASS')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 'mysql.connector.django',#'django.db.backends.mysql',
        'NAME': 'fundoo',
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'autocommit': True,
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = "fundoo/static"
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')
                    ]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

# SWAGGER_SETTINGS = {
#     'USE_SESSION_AUTH': True,
#     'LOGIN_URL': 'rest_framework:login',
#     'LOGOUT_URL': 'rest_framework:logout',
#     'VALIDATOR_URL': None,
# }

# REST_FRAMEWORK = {
#     'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
# }

REST_FRAMEWORK = {
    # Parser classes priority-wise for Swagger
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE')


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'mysite/static'),
# ]
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


BASE_URL = os.getenv('BASE_URL')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_PORT = os.getenv('EMAIL_PORT')

# LOGIN_REDIRECTURL_URL = 'rest_framework:login'
# LOGOUT_URL = 'rest_framework:logout'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)
SITE_ID = 1
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
LOGIN_REDIRECT_URL = 'post'
LOGOUT_REDIRECT_URL = '/'
