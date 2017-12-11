import logging
import os

print(os.path.abspath(__file__))
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='{}/test_logging.log'.format(os.path.dirname(os.path.abspath(__file__))),
                    filemode='a+')
logger = logging.getLogger('log')

logger.debug("i am debug")
logger.info("i am info")
logger.warning("i am warning")
logger.error("i am error")



