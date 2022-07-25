import os
import time

from dotenv import load_dotenv, find_dotenv
from logging import Formatter, Logger, StreamHandler
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union

# Extensions formats for Tesseract
allowed_ext = {'png', 'pdf', 'jpeg', 'jpg'}
# Extensions formats for Barcodes
allowed_ext_barcode_qr = {'tiff', 'tif'}
allowed_ext_barcode_pdf417 = {'png', 'jpeg', 'jpg'}

basedir = os.path.abspath(os.path.dirname(__file__))




# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Config(BaseSettings):
    load_dotenv(os.path.join(basedir, '.env'))
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "phresh:auth")
    JWT_TOKEN_PREFIX = os.getenv("JWT_TOKEN_PREFIX", "Bearer")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = "postgresql://" + os.getenv('POSTGRES_USER', 'root') \
                                             + ":" + os.getenv('POSTGRES_PASSWORD', 'password') \
                                             + "@" + os.getenv('POSTGRES_URL', '172.18.0.2') \
                                             + ":5432/" + os.getenv('POSTGRES_DB', 'bookstore')

    FIRST_SUPERUSER: EmailStr = "admin@recipeapi.com"
    FIRST_SUPERUSER_PW: str = "CHANGEME"

    KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', '172.18.0.4')
    DETECTIONS_TOPIC = os.getenv('DETECTIONS_TOPIC', '172.18.0.4')

    class Config:
        case_sensitive = True


config = Config()


def get_logger(name):
    level = os.getenv("LOGGING_LEVEL", "DEBUG")

    message_format = "[%(asctime)s] [%(levelname)s] %(message)s"
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

    formatter = Formatter(fmt=message_format, datefmt=timestamp_format)
    formatter.converter = time.gmtime

    handler = StreamHandler()
    handler.setFormatter(formatter)

    logger = Logger(name, level=level)
    logger.addHandler(handler)

    return logger


class TestConfig(Config):
    # For flask to run in a testing context
    TESTING = False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext


def allowed_file_barqr(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext_barcode_qr


def allowed_file_bar417(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext_barcode_pdf417


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        'my.packg': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

N_PARALLEL = 8

log_path = './'
LOGGING_CONFIG_ = {
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(levelname)s - %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_path,
                'maxBytes': 1024,
                'backupCount': 3
            }
        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['console']
            }
        },
        'disable_existing_loggers': False
    }
