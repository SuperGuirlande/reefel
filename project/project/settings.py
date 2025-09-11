from pathlib import Path
import environ
import os


BASE_DIR = Path(__file__).resolve().parent.parent

# ENVIRON #
env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / 'project' / '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tailwind',
    'django_ckeditor_5',
    'theme',

    'accounts',
    'main',
    'blog',
    'shop',

    'contact_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'project/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'contact_management.context_processor.contact_infos_context',
                'accounts.context_processor.get_active_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }   
    }

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

# TIMEZONE
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA #
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'main' / 'static',
    BASE_DIR / 'accounts' / 'static',
    BASE_DIR / 'blog' / 'static',
    BASE_DIR / 'shop' / 'static',
    BASE_DIR / 'ckeditor_config' / 'static',
    ]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# TAILWIND #
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'
TAILWIND_APP_NAME = 'theme'

# USER MODEL #
AUTH_USER_MODEL = 'accounts.CustomUser'

# LOGIN
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:my_account'

# # EMAIL SETTINGS #
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('SMTP_HOST')
# EMAIL_PORT = 465
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = env('SMTP_PASS')
# DEFAULT_FROM_EMAIL = 'contact@agencecodemaster.com'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# CKEDITOR #
customColorPalette = [
        # Variantes Minsk
        {
            'color': '#edf1ff',
            'label': 'Minsk 50'
        },
        {
            'color': '#dfe5ff',
            'label': 'Minsk 100'
        },
        {
            'color': '#c5cfff',
            'label': 'Minsk 200'
        },
        {
            'color': '#a1afff',
            'label': 'Minsk 300'
        },
        {
            'color': '#7c84fd',
            'label': 'Minsk 400'
        },
        {
            'color': '#5f5df7',
            'label': 'Minsk 500'
        },
        {
            'color': '#4f40eb',
            'label': 'Minsk 600'
        },
        {
            'color': '#4332d0',
            'label': 'Minsk 700'
        },
        {
            'color': '#372ba8',
            'label': 'Minsk 800'
        },
        {
            'color': '#362f92',
            'label': 'Minsk 900'
        },
        {
            'color': '#1e194d',
            'label': 'Minsk 950'
        },
        
        # Noir et Blanc
        {
            'color': '#000000',
            'label': 'Noir'
        },
        {
            'color': '#ffffff',
            'label': 'Blanc'
        },
        {
            'color': '#6b7280',
            'label': 'Gris'
        },
        
        # Couleurs primaires
        {
            'color': '#ef4444',
            'label': 'Rouge'
        },
        {
            'color': '#22c55e',
            'label': 'Vert'
        },
        {
            'color': '#3b82f6',
            'label': 'Bleu'
        },
        {
            'color': '#eab308',
            'label': 'Jaune'
        },
        {
            'color': '#f97316',
            'label': 'Orange'
        },
        {
            'color': '#a855f7',
            'label': 'Violet'
        },
        {
            'color': '#ec4899',
            'label': 'Rose'
        },
        {
            'color': '#06b6d4',
            'label': 'Cyan'
        },
    ]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': ['heading', '|', 'bold', 'italic', 'link',
                        'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
                    }

    },
    # Blog
    'blog': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'language': 'fr',
        'htmlSupport': {
            'allow': [
                {
                    'name': 'h4',
                    'attributes': True,
                    'classes': True,
                    'styles': True
                }
            ]
        },
        'toolbar': {
            'items': ['heading', '|', 'outdent', 'indent', 'alignment', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',
                    ],
            'shouldNotGroupWhenFull': 'true'
        },
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h2', 'title': 'Titre', 'class': 'ck-heading_heading2' },
                { 'model': 'heading2', 'view': 'h3', 'title': 'Sous-Titre 1', 'class': 'ck-heading_heading3' },
                { 'model': 'heading3', 'view': 'h4', 'title': 'Sous-Titre 2', 'class': 'ck-heading_heading4' }
            ]
        },
        'fontColor': {
            'colors': customColorPalette
        },
        'highlight': {
            'options': [
                {
                    'model': 'yellowMarker',
                    'class': 'marker-yellow',
                    'title': 'Surligneur jaune',
                    'color': '#ffff00',
                    'type': 'marker'
                },
                {
                    'model': 'pinkMarker',
                    'class': 'marker-pink',
                    'title': 'Surligneur rose',
                    'color': '#ff69b4',
                    'type': 'marker'
                },
                {
                    'model': 'greenMarker',
                    'class': 'marker-green',
                    'title': 'Surligneur vert',
                    'color': '#90ee90',
                    'type': 'marker'
                },
                {
                    'model': 'blueMarker',
                    'class': 'marker-blue',
                    'title': 'Surligneur bleu',
                    'color': '#87ceeb',
                    'type': 'marker'
                },
                {
                    'model': 'redMarker',
                    'class': 'marker-red',
                    'title': 'Surligneur rouge',
                    'color': '#ff6b6b',
                    'type': 'marker'
                }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}