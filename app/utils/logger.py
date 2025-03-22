
import logging
from typing import Optional

_FORMATTER = '%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(message)s |'

def setup_logging(
    log_file: Optional[str],
    level: int,  # Changed from logging._Level to int for broader compatibility
    notebook_mode: bool = False,  # Added default value,
):
    """
    Configures logging settings for an application.

    :param log_file: The path to the log file.
    :type log_file: Optional[str]
    :param level: Logging level.
    :type level: int
    :param include_host: Flag to include hostname in logs, defaults to False.
    :type include_host: bool, optional
    :param notebook_mode: Flag to indicate if running in notebook, defaults to False.
    :type notebook_mode: bool, optional
    """
    # Remove prexisting handlers by default
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set formatter and log level
    formatter = logging.Formatter(_FORMATTER)
    logging.root.setLevel(level)

    if log_file:
        file_handler = logging.FileHandler(filename=log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)

    if not notebook_mode:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logging.root.addHandler(stream_handler)

    # Set different level errors for each service
    dict_log_levels = {
        "azure" : logging.WARNING,
        "requests": logging.WARNING,
        "httpx": logging.WARNING,
        "openai" : logging.WARNING,
        "replicate": logging.WARNING,
        "stabilityai": logging.WARNING,
    }
    for service, log_level in dict_log_levels.items():
        logging.getLogger(service).setLevel(log_level)