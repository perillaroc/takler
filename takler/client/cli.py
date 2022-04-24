import os
from typing import Optional

import typer

from takler.client.service_client import TaklerServiceClient


TAKLER_HOST = "TAKLER_HOST"
TAKLER_PORT = "TAKLER_PORT"


app = typer.Typer()


@app.command()
def init(
        task_id: str = typer.Option(...),
        node_path: str = typer.Option(...),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_init(node_path=node_path, task_id=task_id)
    client.shutdown()


@app.command()
def complete(
        node_path: str = typer.Option(...),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_complete(node_path=node_path)
    client.shutdown()


@app.command()
def requeue(
        node_path: str = typer.Option(...),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_requeue(node_path=node_path)
    client.shutdown()


@app.command()
def show(
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_request_show()
    client.shutdown()


def get_host(host: Optional[str] = None) -> Optional[str]:
    if host is not None:
        return host
    if TAKLER_HOST in os.environ:
        return os.environ[TAKLER_HOST]
    return None


def get_port(port: Optional[int] = None) -> Optional[int]:
    if port is not None:
        return port
    if TAKLER_PORT in os.environ:
        return int(os.environ[TAKLER_PORT])
    return None
