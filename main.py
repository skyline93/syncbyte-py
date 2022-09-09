import click
import uvicorn

from app.config import settings


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    pass


@cli.command()
@click.option("--port", "-p", type=int, default=settings.UVICORN_PORT)
def run(port):
    uvicorn.run(app="app:web_app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    cli()
