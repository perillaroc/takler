import socket
from pathlib import Path
from typing import Union

import yaml
from pydantic import BaseModel


TAKLER_CONNECT_FILE = "TAKLER_CONNECT_FILE"


class Address(BaseModel):
    hostname: str
    ip: str
    port: str


class Server(BaseModel):
    address: Address


class ConnectConfig(BaseModel):
    server: Server


def generate_connect_config() -> ConnectConfig:
    hostname = socket.gethostname()
    ip = get_ip()
    port = str(get_port())

    c = ConnectConfig(
        server=Server(
            address=Address(
                hostname=hostname,
                ip=ip,
                port=port,
            )
        )
    )
    c.dict()
    return c


def save_connect_config(config: ConnectConfig, file_path: Union[str, Path]):
    d = config.model_dump()
    with open(file_path, "w") as f:
        yaml.safe_dump(d, f)


def load_connect_config(file_path: Union[str, Path]) -> ConnectConfig:
    with open(file_path, "r") as f:
        d = yaml.safe_load(f)
        c = ConnectConfig(**d)
        return c


def get_ip() -> str:
    """
    get ip address

    References
    -----------
    https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-a-nic-network-interface-controller-in-python

    Returns
    -------
    str
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_port():
    """
    get an available port.

    References
    ----------
    https://stackoverflow.com/questions/1365265/on-localhost-how-do-i-pick-a-free-port-number

    Returns
    -------
    int
    """
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]
