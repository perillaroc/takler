import typer

from takler.client.service_client import TaklerServiceClient


app = typer.Typer()


@app.command()
def init(
        task_id: str = typer.Option(...),
        node_path: str = typer.Option(...),
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
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
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_command_complete(node_path=node_path)
    client.shutdown()


@app.command()
def show(
        host: str = typer.Option(None, help="takler service host"),
        port: int = typer.Option(None, help="takler service port"),
):
    client = TaklerServiceClient(host=host, port=port)
    client.start()
    client.run_request_show()
    client.shutdown()
