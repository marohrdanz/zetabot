import logging


## configure logging
UNDERLINE = '\033[4m'
END = '\033[0m'
YELLOW = '\033[93m'
FORMAT = f"{UNDERLINE}%(lineno)4d{END} - {UNDERLINE}%(name)s{END} - {YELLOW}%(levelname)s{END} - %(message)s"
#FORMAT = f"{UNDERLINE}%(asctime)s{END} - {UNDERLINE}%(name)s{END} - {YELLOW}%(levelname)s{END} - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)
#logging.getLogger('httpcore').setLevel(logging.ERROR)
#logging.getLogger('httpx').setLevel(logging.ERROR)
#logging.getLogger('anthropic').setLevel(logging.ERROR)
