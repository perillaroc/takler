import os
from typing import Optional

import typer

from takler.client.service_client import TaklerServiceClient


TAKLER_HOST = "TAKLER_HOST"
TAKLER_PORT = "TAKLER_PORT"
TAKLER_NAME = "TAKLER_NAME"


app = typer.Typer()


# Child command -----------------------------------------------------


@app.command()
def init(
        task_id: str = typer.Option(...),
        node_path: str = typer.Option(None, help="node path"),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    host = get_host(host)
    port = get_port(port)
    node_path = get_node_path(node_path)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_init(node_path=node_path, task_id=task_id)
    client.shutdown()


@app.command()
def complete(
        node_path: str = typer.Option(None, help="node path"),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    host = get_host(host)
    port = get_port(port)
    node_path = get_node_path(node_path)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_complete(node_path=node_path)
    client.shutdown()


@app.command()
def abort(
        node_path: str = typer.Option(None, help="node path"),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
        reason: str = typer.Option("", help="abort reason")
):
    host = get_host(host)
    port = get_port(port)
    node_path = get_node_path(node_path)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_abort(node_path=node_path, reason=reason)
    client.shutdown()


@app.command()
def event(
        node_path: str = typer.Option(None, help="node path"),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
        event_name: str = typer.Option(..., help="event name"),
):
    host = get_host(host)
    port = get_port(port)
    node_path = get_node_path(node_path)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_event(node_path=node_path, event_name=event_name)
    client.shutdown()


@app.command()
def meter(
        node_path: str = typer.Option(None, help="node path"),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
        meter_name: str = typer.Option(..., help="meter name"),
        meter_value: str = typer.Option(..., help="meter value"),
):
    host = get_host(host)
    port = get_port(port)
    node_path = get_node_path(node_path)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_meter(node_path=node_path, meter_name=meter_name, meter_value=meter_value)
    client.shutdown()


# Control command --------------------------------------------------------

@app.command()
def requeue(
        node_path: str = typer.Option(None, help="node path"),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    host = get_host(host)
    port = get_port(port)
    node_path = get_node_path(node_path)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_requeue(node_path=node_path)
    client.shutdown()


# Show command --------------------------------------------------------


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


# ----------------------------


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


def get_node_path(node_path: Optional[str] = None) -> Optional[str]:
    if node_path is not None:
        return node_path
    if TAKLER_NAME in os.environ:
        return os.environ[TAKLER_NAME]
    return None
