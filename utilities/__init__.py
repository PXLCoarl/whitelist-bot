import logging
from .pycraft import check_username
from .embeds import ErrorEmbed, InfoEmbed, SuccessEmbed
from .rconclient import MCClient
from .database import DataBaseUtils, create_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger()

