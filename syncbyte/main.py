import click
import uvicorn

from syncbyte.scheduler import schedule
from syncbyte.config import settings


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    pass


@cli.command()
@click.option("--port", "-p", type=int, default=settings.UVICORN_PORT)
def run(port):
    uvicorn.run(app="app:web_app", host="0.0.0.0", port=port)


@cli.command()
def run_schedule():
    schedule()


if __name__ == "__main__":
    cli()
