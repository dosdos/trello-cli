from typing import Optional

import typer

from . import __app_name__, __app_version__, config
from .trello_utils import TrelloClient

app = typer.Typer()


def get_trello_connector() -> TrelloClient:
    if not config.TRELLO_API_KEY:
        typer.secho(
            'Trello API key not found. Please, set the TRELLO_API_KEY value in the .env file.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if not config.TRELLO_API_TOKEN:
        typer.secho(
            'Trello API token not found. Please, set the TRELLO_API_TOKEN value in the .env file.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    return TrelloClient(config.TRELLO_API_KEY, config.TRELLO_API_TOKEN)


@app.command(name='list-boards')
def list_boards() -> None:
    """Get the list of Trello boards with name and ID."""
    trello_connector = get_trello_connector()
    board_list = trello_connector.get_board_list()

    if len(board_list) == 0:
        typer.secho('No boards found.', fg=typer.colors.YELLOW)
        raise typer.Exit()

    columns = (
        '#  ',
        '| Board ID                   ',
        '| Board Name                 ',
        '| Closed  ',
    )
    headers = ''.join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho('-' * len(headers), fg=typer.colors.BLUE)
    for idx, board in enumerate(board_list, 1):
        typer.secho(
            f'{idx}{(len(columns[0]) - len(str(idx))) * " "}'
            f'| [{board.id}] '
            f'| {board.name[:27]}{(len(columns[2]) - len(str(board.name)) - 2) * " "}'
            f'| {board.closed}',
            fg=typer.colors.BLUE,
        )
    typer.secho('-' * len(headers) + '\n', fg=typer.colors.BLUE)


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
