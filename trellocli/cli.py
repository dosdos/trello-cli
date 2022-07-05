from typing import Optional

import typer

from . import __app_name__, __app_version__

app = typer.Typer()


def _version_callback(val: bool) -> None:
    if val:
        typer.echo(f'{__app_name__} v{__app_version__}')
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            '--version',
            '-v',
            help='Echo the app version and exit.',
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
