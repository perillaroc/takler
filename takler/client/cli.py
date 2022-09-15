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
    client.init(node_path=node_path, task_id=task_id)


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
    client.complete(node_path=node_path)


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
    client.abort(node_path=node_path, reason=reason)


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
    client.event(node_path=node_path, event_name=event_name)


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
    client.meter(node_path=node_path, meter_name=meter_name, meter_value=meter_value)


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
    client.requeue(node_path=node_path)


@app.command()
def suspend(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        node_path: List[str] = typer.Argument(..., help="node paths"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.suspend(node_path=node_path)


@app.command()
def resume(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        node_path: List[str] = typer.Argument(..., help="node paths"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.resume(node_path=node_path)


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
    client.run(node_path=node_path, force=force)


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
    client.force(variable_paths=variable_path, state=state, recursive=recursive)


@app.command()
def free_dep(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        dep_type: str = typer.Option(True, help="dependency type, [all, time, trigger]"),
        node_path: List[str] = typer.Argument(..., help="variable paths"),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.free_dep(node_paths=node_path, dep_type=dep_type)


# Show command --------------------------------------------------------


@app.command()
def show(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
        show_trigger: bool = typer.Option(False, help="show triggers"),
        show_parameter: bool = typer.Option(False, help="show parameters"),
        show_limit: bool = typer.Option(True, help="show limits"),
        show_event: bool = typer.Option(True, help="show events"),
        show_meter: bool = typer.Option(True, help="show meters"),
        show_all: bool = typer.Option(False, help="show all items, ignore other options."),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)

    if show_all:
        show_trigger = True
        show_parameter = True
        show_limit = True
        show_event = True
        show_meter = True

    client.show(
        show_trigger=show_trigger,
        show_parameter=show_parameter,
        show_limit=show_limit,
        show_event=show_event,
        show_meter=show_meter,
    )


@app.command()
def ping(
        host: str = typer.Option(None, help=HOST_HELP_STRING),
        port: str = typer.Option(None, help=PORT_HELP_STRING),
):
    host = get_host(host)
    port = get_port(port)
    client = TaklerServiceClient(host=host, port=port)
    client.ping()

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
