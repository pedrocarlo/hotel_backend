import logging
logger = logging.getLogger('uvicorn').getChild('api')
c_handler = logging.StreamHandler()
c_handler.setFormatter(logging.Formatter('%(name)s %(levelname)s - %(message)s'))
logger.addHandler(c_handler)
logger.setLevel(logging.INFO)

logger.info('test')