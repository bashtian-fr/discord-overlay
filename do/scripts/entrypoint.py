import logging
import signal
import sys
import click

from do.app import App
from do import (
    APPLICATION_NAME,
    ORGANIZATION_DOMAIN,
)

# To manage CTRL+C from terminal
signal.signal(signal.SIGINT, signal.SIG_DFL)

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


@click.command()
@click.option('--debug', is_flag=True, default=False)
def main(debug=False):
    if debug:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    app = App(
        organization_domain=ORGANIZATION_DOMAIN,
        application_name=APPLICATION_NAME
    )
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
