import logging
import sys

formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)-8s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.addHandler(handler)