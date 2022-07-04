import os
from typing import Optional, List, Union

import typer

from takler.client.service_client import TaklerServiceClient
from takler.constant import DEFAULT_HOST, DEFAULT_PORT


TAKLER_HOST = "TAKLER_HOST"
TAKLER_PORT = "TAKLER_PORT"
TAKLER_NAME = "TAKLER_NAME"
NO_TAKLER = "NO_TAKLER"

HOST_HELP_STRING = f"takler service host, or use env var {TAKLER_HOST}"
PORT_HELP_STRING = f"takler service port, or use env var {TAKLER_PORT}"


app = typer.Typer()


# Child command -----------------------------------------------------


@app.command()
def init(
        task_id: str = typer.Option(..., help="task id (TAKLER_RID)."),
        node_path: str = typer.Option(..., envvar=TAKLER_NAME, help="node path."),
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
):
    if NO_TAKLER in os.environ:
        typer.echo("ignore because NO_TAKLER is set.")
        return
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_init(node_path=node_path, task_id=task_id)
    client.shutdown()


@app.command()
def complete(
        node_path: str = typer.Option(..., envvar=TAKLER_NAME, help="node path."),
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
):
    if NO_TAKLER in os.environ:
        typer.echo("ignore because NO_TAKLER is set.")
        return
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_complete(node_path=node_path)
    client.shutdown()


@app.command()
def abort(
        node_path: str = typer.Option(..., envvar=TAKLER_NAME, help="node path."),
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        reason: str = typer.Option("", help="abort reason")
):
    if NO_TAKLER in os.environ:
        typer.echo("ignore because NO_TAKLER is set.")
        return
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_abort(node_path=node_path, reason=reason)
    client.shutdown()


@app.command()
def event(
        node_path: str = typer.Option(..., envvar=TAKLER_NAME, help="node path."),
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        event_name: str = typer.Option(..., help="event name"),
):
    if NO_TAKLER in os.environ:
        typer.echo("ignore because NO_TAKLER is set.")
        return
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_event(node_path=node_path, event_name=event_name)
    client.shutdown()


@app.command()
def meter(
        node_path: str = typer.Option(..., envvar=TAKLER_NAME, help="node path."),
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        meter_name: str = typer.Option(..., help="meter name"),
        meter_value: str = typer.Option(..., help="meter value"),
):
    if NO_TAKLER in os.environ:
        typer.echo("ignore because NO_TAKLER is set.")
        return
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_meter(node_path=node_path, meter_name=meter_name, meter_value=meter_value)
    client.shutdown()


# Control command --------------------------------------------------------


@app.command()
def requeue(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        node_path: List[str] = typer.Argument(..., help="node paths"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_requeue(node_path=node_path)
    client.shutdown()


@app.command()
def suspend(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        node_path: List[str] = typer.Argument(..., help="node paths"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_suspend(node_path=node_path)
    client.shutdown()


@app.command()
def resume(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        node_path: List[str] = typer.Argument(..., help="node paths"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_resume(node_path=node_path)
    client.shutdown()


@app.command()
def run(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        node_path: List[str] = typer.Argument(..., help="node paths"),
        force: bool = typer.Option(False, help="force run"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_run(node_path=node_path, force=force)
    client.shutdown()


@app.command()
def force(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        recursive: bool = typer.Option(True, help="recursive"),
        state: str = typer.Argument(..., help="state"),
        variable_path: List[str] = typer.Argument(..., help="variable paths"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_force(variable_paths=variable_path, state=state, recursive=recursive)
    client.shutdown()


# Show command --------------------------------------------------------


@app.command()
def show(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_request_show()
    client.shutdown()


# ----------------------------


def get_host(host: Optional[str] = None) -> Optional[str]:
    """
    Get takler server's host. If ``host`` is ``None``, check environment variable ``TAKLER_HOST``.

    Parameters
    ----------
    host

    Returns
    -------
    Optional[str]
    """
    if host is not None:
        return host
    if TAKLER_HOST in os.environ:
        return os.environ[TAKLER_HOST]
    return DEFAULT_HOST


def get_port(port: Optional[Union[str, int]] = None) -> Optional[str]:
    """
    Get takler server's port. If ``port`` is ``None``, check environment variable ``TAKLER_PORT``.

    Parameters
    ----------
    port

    Returns
    -------
    Optional[str]
    """
    if port is not None:
        return str(port)
    if TAKLER_PORT in os.environ:
        return os.environ[TAKLER_PORT]
    return DEFAULT_PORT


def get_node_path(node_path: Optional[str] = None) -> Optional[str]:
    """
    Get node path. If ``node_path`` is ``None``, check environment variable ``TAKLER_NAME``.

    Parameters
    ----------
    node_path

    Returns
    -------
    Optional[str]
    """
    if node_path is not None:
        return node_path
    if TAKLER_NAME in os.environ:
        return os.environ[TAKLER_NAME]
    return None
