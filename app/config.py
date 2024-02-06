class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/vending_machine'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-secret-key' #for auth
    
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
LOG_LEVEL = logging.INFO
LOG_FILENAME = 'app.log'

# Logger configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 1024 * 1024 * 10,  # 10MB per file
            'backupCount': 5,
            'formatter': 'standard',
            'level': LOG_LEVEL,
        },
    },
    'root': {
        'handlers': ['file_handler'],
        'level': LOG_LEVEL,
    },
}