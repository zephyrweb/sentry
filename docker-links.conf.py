postgres = os.getenv('SENTRY_POSTGRES_HOST') or (os.getenv('POSTGRES_PORT_5432_TCP_ADDR') and 'postgres')
mysql = os.getenv('SENTRY_MYSQL_HOST') or (os.getenv('MYSQL_PORT_3306_TCP_ADDR') and 'mysql')
redis = os.getenv('SENTRY_REDIS_HOST') or (os.getenv('REDIS_PORT_6379_TCP_ADDR') and 'redis')
memcached = os.getenv('SENTRY_MEMCACHED_HOST') or (os.getenv('MEMCACHED_PORT_11211_TCP_ADDR') and 'memcached')
postfix = os.getenv('SENTRY_POSTFIX_HOST') or (os.getenv('POSTFIX_PORT_25_TCP_PORT') and 'postfix')

if postgres:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or os.getenv('POSTGRES_ENV_POSTGRES_USER')
                or 'postgres'
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or os.getenv('POSTGRES_ENV_POSTGRES_USER')
                or 'postgres'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or os.getenv('POSTGRES_ENV_POSTGRES_PASSWORD')
                or ''
            ),
            'HOST': postgres,
            'PORT': (
                os.getenv('SENTRY_POSTGRES_PORT')
                or ''
            ),
            'OPTIONS': {
                'autocommit': True,
            },
        },
    }
elif mysql:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or os.getenv('MYSQL_ENV_MYSQL_DATABASE')
                or ''
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or os.getenv('MYSQL_ENV_MYSQL_USER')
                or 'root'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or os.getenv('MYSQL_ENV_MYSQL_PASSWORD')
                or os.getenv('MYSQL_ENV_MYSQL_ROOT_PASSWORD')
                or ''
            ),
            'HOST': mysql,
            'PORT': (
                os.getenv('SENTRY_MYSQL_PORT')
                or ''
            ),
        },
    }
else:
    sqlite_path = (
        os.getenv('SENTRY_DB_NAME')
        or 'sentry.db'
    )
    if not os.path.isabs(sqlite_path):
        sqlite_path = os.path.join(CONF_ROOT, sqlite_path)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': sqlite_path,
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
    }

if memcached:
    memcached_port = (
        os.getenv('SENTRY_MEMCACHED_PORT')
        or '11211'
    )
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [memcached + ':' + memcached_port],
        }
    }

if redis:
    redis_port = (
        os.getenv('SENTRY_REDIS_PORT')
        or '6379'
    )
    redis_db = (
        os.getenv('SENTRY_REDIS_DB')
        or '0'
    )
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = {
        'hosts': {
            0: {
                'host': redis,
                'port': redis_port,
                'db': redis_db,
            },
        },
    }
    BROKER_URL = 'redis://' + redis + ':' + redis_port + '/' + redis_db
else:
    raise Exception('Error: REDIS_PORT_6379_TCP_ADDR (or SENTRY_REDIS_HOST) is undefined, did you forget to `--link` a redis container?')

if postfix:
    #EMAIL_BACKEND = os.getenv('SENTRY_EMAIL_BACKEND') or 'django.core.mail.backends.console.EmailBackend')
    EMAIL_HOST = (
        os.getenv('SENTRY_EMAIL_HOST')
        or os.getenv('POSTFIX_PORT_25_TCP_ADDR')
        or 'localhost'
    )
    EMAIL_HOST_PASSWORD = (
        os.getenv('SENTRY_EMAIL_HOST_PASSWORD')
        or os.getenv('POSTFIX_SMTP_PASSWORD')
        or ''
    )
    EMAIL_HOST_USER = (
        os.getenv('SENTRY_EMAIL_HOST_USER')
        or os.getenv('POSTFIX_SMTP_USER')
        or ''
    )
    EMAIL_PORT = (
        os.getenv('SENTRY_EMAIL_PORT')
        or os.getenv('POSTFIX_PORT_25_TCP_PORT')
        or 25
    )
    EMAIL_USE_TLS = os.getenv('SENTRY_EMAIL_USE_TLS')

# The email address to send on behalf of
SERVER_EMAIL = os.getenv('SENTRY_SERVER_EMAIL') or 'root@localhost'

SENTRY_URL_PREFIX = os.getenv('SENTRY_URL_PREFIX') or ''

SENTRY_ADMIN_EMAIL = os.getenv('SENTRY_ADMIN_EMAIL') or ''
