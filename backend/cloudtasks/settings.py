import os
from pathlib import Path

# Registrar PyMySQL como reemplazo de mysqlclient ANTES de cualquier
# uso del backend de base de datos.
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga variables desde backend/.env si existe (solo en local)
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key-change-in-prod")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "tasks",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cloudtasks.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "cloudtasks.wsgi.application"

# Base de datos. Prioriza variables MYSQL* del plugin de Railway,
# luego DB_* del .env local, y si nada existe cae a SQLite.
if os.environ.get("MYSQLDATABASE") or os.environ.get("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("MYSQLDATABASE") or os.environ.get("DB_NAME"),
            "USER": os.environ.get("MYSQLUSER") or os.environ.get("DB_USER", "root"),
            "PASSWORD": os.environ.get("MYSQLPASSWORD") or os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("MYSQLHOST") or os.environ.get("DB_HOST", "127.0.0.1"),
            "PORT": os.environ.get("MYSQLPORT") or os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            "CONN_MAX_AGE": 600,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": None,
}

# CORS: en producción restringe al dominio del frontend (Vercel) si defines FRONTEND_URL.
_frontend = os.environ.get("FRONTEND_URL", "").strip()
if _frontend:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _frontend.split(",") if o.strip()]
    CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)
else:
    CORS_ALLOW_ALL_ORIGINS = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

_railway_host = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()
if _railway_host and _railway_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_railway_host)
    CSRF_TRUSTED_ORIGINS = locals().get("CSRF_TRUSTED_ORIGINS", []) + [f"https://{_railway_host}"]

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"