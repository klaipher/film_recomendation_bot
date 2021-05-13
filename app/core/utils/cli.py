import click
from aiogram.__main__ import SysInfo


@click.group()
def cli():
    from app import misc
    from app.core.utils import logging

    logging.setup()
    misc.setup()


@cli.command()
def version():
    """
    Get application version
    """
    click.echo(SysInfo())


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
def polling(skip_updates: bool):
    """
    Start application in polling mode
    """

    from app.core.utils.executor import runner

    runner.skip_updates = skip_updates
    runner.start_polling(reset_webhook=True)
