import logging
import logging.config
import os
from datetime import datetime

def setup_logging():
    """Configure application logging."""
    
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': log_level,
                'formatter': 'detailed',
                'filename': f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': f'logs/error_{datetime.now().strftime("%Y%m%d")}.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file', 'error_file'],
                'level': log_level,
                'propagate': False
            }
        }
    }
    
    logging.config.dictConfig(logging_config)