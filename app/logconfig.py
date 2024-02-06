# logconfig.py

import logging
from logging.config import dictConfig
from app.config import LOGGING_CONFIG

# Configure the logging system with the configuration defined in config.py
dictConfig(LOGGING_CONFIG)

# Create a logger for this file
logger = logging.getLogger(__name__)