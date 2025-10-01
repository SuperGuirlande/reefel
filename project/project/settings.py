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
    'django.contrib.sites',

    'tailwind',
    'django_ckeditor_5',
    'theme',

    'accounts',
    'main',
    'blog',
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

# SITES FRAMEWORK
SITE_ID = 1

# STATIC & MEDIA #
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'main' / 'static',
    # BASE_DIR / 'accounts' / 'static',
    # BASE_DIR / 'blog' / 'static',
    # BASE_DIR / 'shop' / 'static',
    # BASE_DIR / 'ckeditor_config' / 'static',
    ]

MEDIA_URL = 'media/'

if DEBUG:
        STATIC_ROOT = BASE_DIR / 'staticfiles'
        MEDIA_ROOT = BASE_DIR / 'media'
else:
        STATIC_ROOT=env('STATIC_ROOT')
        MEDIA_ROOT=env('MEDIA_ROOT')

# TAILWIND #
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'
TAILWIND_APP_NAME = 'theme'

# USER MODEL #
AUTH_USER_MODEL = 'accounts.CustomUser'

# LOGIN
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:my_account'

# EMAIL SETTINGS #
EMAIL_BACKEND = 'accounts.backends.CustomEmailBackend'  # Backend personnalisé
EMAIL_HOST = env('SMTP_HOST')
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = env('SMTP_PASS')
DEFAULT_FROM_EMAIL = 'Site Web Reefel <contact@agencecodemaster.com>'

# Debug email en développement
if DEBUG:
    EMAIL_TIMEOUT = 30  # Timeout plus long pour debug
    print(f"Configuration EMAIL - Host: {env('SMTP_HOST', default='NON_DEFINI')}")
    print(f"Configuration EMAIL - Port: 465")
    print(f"Configuration EMAIL - User: apikey")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CKEDITOR #
customColorPalette = [
        # Palette Reefel Workshop - Dark Mode
        # Slate (Backgrounds)
        {
            'color': '#0f172a',
            'label': 'Slate 900'
        },
        {
            'color': '#1e293b',
            'label': 'Slate 800'
        },
        {
            'color': '#334155',
            'label': 'Slate 700'
        },
        {
            'color': '#475569',
            'label': 'Slate 600'
        },
        {
            'color': '#64748b',
            'label': 'Slate 500'
        },
        {
            'color': '#94a3b8',
            'label': 'Slate 400'
        },
        {
            'color': '#cbd5e1',
            'label': 'Slate 300'
        },
        {
            'color': '#e2e8f0',
            'label': 'Slate 200'
        },
        {
            'color': '#f1f5f9',
            'label': 'Slate 100'
        },
        
        # Cyan (Accent principal)
        {
            'color': '#22d3ee',
            'label': 'Cyan 400'
        },
        {
            'color': '#06b6d4',
            'label': 'Cyan 500'
        },
        {
            'color': '#0891b2',
            'label': 'Cyan 600'
        },
        {
            'color': '#0e7490',
            'label': 'Cyan 700'
        },
        
        # Blue (Accent secondaire)
        {
            'color': '#3b82f6',
            'label': 'Blue 500'
        },
        {
            'color': '#2563eb',
            'label': 'Blue 600'
        },
        {
            'color': '#1d4ed8',
            'label': 'Blue 700'
        },
        
        # Orange (Accent tertiaire)
        {
            'color': '#ea580c',
            'label': 'Orange 600'
        },
        {
            'color': '#f97316',
            'label': 'Orange 500'
        },
        {
            'color': '#fb923c',
            'label': 'Orange 400'
        },
        
        # Yellow (Accent quaternaire)
        {
            'color': '#eab308',
            'label': 'Yellow 500'
        },
        {
            'color': '#facc15',
            'label': 'Yellow 400'
        },
        
        # Texte
        {
            'color': '#ffffff',
            'label': 'Blanc'
        },
        {
            'color': '#f1f5f9',
            'label': 'Slate 100'
        },
        {
            'color': '#cbd5e1',
            'label': 'Slate 300'
        },
        {
            'color': '#94a3b8',
            'label': 'Slate 400'
        },
        
        # Couleurs d'alerte
        {
            'color': '#ef4444',
            'label': 'Rouge'
        },
        {
            'color': '#22c55e',
            'label': 'Vert'
        },
        {
            'color': '#f59e0b',
            'label': 'Amber'
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
        'ui': {
        },
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
        'fontFamily': {
            'options': [
                'default',
                'Poppins, sans-serif',
                'Montserrat, sans-serif',
                'Raleway, sans-serif',
                'Story Script, cursive',
                'Bebas Neue, sans-serif',
                'Caveat Brush, cursive',
                'Nosifer, sans-serif',
                'Red Hat Display, sans-serif',
                'Sedgwick Ave, cursive',
                'Zen Dots, sans-serif'
            ]
        },
        'fontColor': {
            'colors': customColorPalette
        },
        'highlight': {
            'options': [
                {
                    'model': 'cyanMarker',
                    'class': 'marker-cyan',
                    'title': 'Surligneur cyan',
                    'color': '#22d3ee',
                    'type': 'marker'
                },
                {
                    'model': 'blueMarker',
                    'class': 'marker-blue',
                    'title': 'Surligneur bleu',
                    'color': '#3b82f6',
                    'type': 'marker'
                },
                {
                    'model': 'orangeMarker',
                    'class': 'marker-orange',
                    'title': 'Surligneur orange',
                    'color': '#f97316',
                    'type': 'marker'
                },
                {
                    'model': 'yellowMarker',
                    'class': 'marker-yellow',
                    'title': 'Surligneur jaune',
                    'color': '#eab308',
                    'type': 'marker'
                },
                {
                    'model': 'greenMarker',
                    'class': 'marker-green',
                    'title': 'Surligneur vert',
                    'color': '#22c55e',
                    'type': 'marker'
                },
                {
                    'model': 'pinkMarker',
                    'class': 'marker-pink',
                    'title': 'Surligneur rose',
                    'color': '#ec4899',
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