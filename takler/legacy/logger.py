import logging
import sys

SERVER_LOG_FORMAT = "%(asctime)s [%(module)s] [%(levelname)s]: %(message)s"
CLIENT_LOG_FORMAT = "%(asctime)s [%(module)s] [%(levelname)s]: %(message)s"


def create_server_logger():
    server_log_handler = logging.StreamHandler()
    server_log_handler.setLevel(logging.INFO)
    server_log_handler.setFormatter(logging.Formatter(SERVER_LOG_FORMAT))
    server_logger = logging.getLogger('takler-server')
    server_logger.setLevel(logging.INFO)
    server_logger.addHandler(server_log_handler)
    return server_logger


def create_client_logger():
    client_log_handler = logging.StreamHandler()
    client_log_handler.setLevel(logging.WARNING)
    client_log_handler.setFormatter(logging.Formatter(CLIENT_LOG_FORMAT))
    client_logger = logging.getLogger('takler-client')
    client_logger.setLevel(logging.INFO)
    client_logger.addHandler(client_log_handler)
    return client_logger


server_logger = create_server_logger()
client_logger = create_client_logger()