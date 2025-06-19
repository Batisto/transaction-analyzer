import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%m:%s"
)

logger = logging.getLogger("transaction-analyzer")
