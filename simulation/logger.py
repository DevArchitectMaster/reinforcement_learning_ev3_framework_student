import logging, logging.config
import json

def createLogger(config, logger_name="__main__", logfile=None):
    with open(config) as json_file:
        logger_config = json.load(json_file)
        if (logfile is not None):
            logger_config['handlers']['file']['filename'] = logfile
        logging.config.dictConfig(logger_config)
    
    logger = logging.getLogger(logger_name)
    return logger