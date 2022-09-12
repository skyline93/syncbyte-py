import os
import click
import uvicorn

from alembic import command
from alembic.config import Config

from syncbyte.scheduler import schedule
from syncbyte.config import settings
from syncbyte.celery import app as celery_app


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    pass


@cli.group()
def db():
    pass


@cli.command()
@click.option("--port", "-p", type=int, default=settings.UVICORN_PORT)
def run_web(port):
    uvicorn.run(app="syncbyte:web_app", host="0.0.0.0", port=port)


@cli.command()
def run_schedule():
    schedule()


@cli.command()
@click.option("--queue", '-Q', required=True, type=str)
@click.option("--concurrency", "-c", type=int, default=4)
@click.option("--pool", "-P", type=str, default="eventlet")
@click.option("--logger_lever", "-l", type=str, default="info")
def run_worker(pool, concurrency, queue, logger_lever):
    celery_app.worker_main(argv=["worker", "-P", pool, "-c", concurrency, "-Q", queue, "-l", logger_lever])


@db.command()
@click.option("--message", "-m")
def revision(message):
    cfg = Config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "alembic.ini"))
    command.revision(cfg, message, autogenerate=True)


@db.command()
@click.option("--revision", "-v", type=str, default="head")
@click.option('--sql/--no-sql', default=False)
def upgrade(revision, sql):
    cfg = Config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "alembic.ini"))
    command.upgrade(cfg, revision, sql)


@db.command()
@click.option("--revision", "-v", type=str, required=True)
def downgrade(revision):
    cfg = Config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "alembic.ini"))
    command.downgrade(cfg, revision)


if __name__ == "__main__":
    cli()
