from typing import Optional

import typer

from . import __app_name__, __app_version__, config
from .trello_utils import TrelloClient

app = typer.Typer()


def get_trello_connector() -> TrelloClient:
    if not config.TRELLO_API_KEY:
        typer.secho(config.MSG_API_KEY_NOT_FOUND, fg=typer.colors.RED)
        raise typer.Exit(1)
    if not config.TRELLO_API_TOKEN:
        typer.secho(config.MSG_API_TOKEN_NOT_FOUND, fg=typer.colors.RED)
        raise typer.Exit(1)
    return TrelloClient(config.TRELLO_API_KEY, config.TRELLO_API_TOKEN)


@app.command(name='list-boards')
def list_boards() -> None:
    """Get the list of Trello boards with name and ID."""
    trello_connector = get_trello_connector()
    try:
        board_list = trello_connector.get_board_list()
    except Exception as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    if len(board_list) == 0:
        typer.secho(config.MSG_BOARDS_FOUND, fg=typer.colors.YELLOW)
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


@app.command(name='list-columns')
def list_columns_by_board_id(board_id: str = typer.Argument(...)) -> None:
    """Get the list of columns by board ID."""
    trello_connector = get_trello_connector()
    try:
        board_columns = trello_connector.get_board_columns(board_id)
    except Exception as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    if len(board_columns) == 0:
        typer.secho(config.MSG_COLUMNS_FOUND, fg=typer.colors.YELLOW)
        raise typer.Exit()

    columns = (
        '#  ',
        '| Column ID                  ',
        '| Column Name       ',
    )
    headers = ''.join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho('-' * len(headers), fg=typer.colors.BLUE)
    for idx, col in enumerate(board_columns, 1):
        typer.secho(
            f'{idx}{(len(columns[0]) - len(str(idx))) * " "}'
            f'| [{col.id}] '
            f'| {col.name[:27]}{(len(columns[2]) - len(str(col.name)) - 2) * " "}',
            fg=typer.colors.BLUE,
        )
    typer.secho('-' * len(headers) + '\n', fg=typer.colors.BLUE)


@app.command(name='create-card')
def create_card_by_column_id(
        column_id: str = typer.Option(..., '--column', '-c', help=config.MSG_COL_ID_HELP),
        name: str = typer.Option(..., prompt=config.MSG_NAME_PROMPT, help=config.MSG_NAME_HELP),
        comment: str = typer.Option(..., prompt=config.MSG_COMMENT_PROMPT, help=config.MSG_COMMENT_HELP),
        labels: str = typer.Option(..., prompt=config.MSG_LABELS_PROMPT, help=config.MSG_LABELS_HELP),
) -> None:
    """Create a new Trello card given the the board column ID."""
    trello_connector = get_trello_connector()
    try:
        card = trello_connector.create_card(column_id, name, comment, labels.split())
    except Exception as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(config.MSG_NEW_CARD_ADDED % card.id, fg=typer.colors.BLUE, bold=True)
    typer.secho('-' * 67, fg=typer.colors.BLUE)
    card_fields = ('board_id', 'column_id', 'name', 'comment', 'comment_id', 'pos', 'short_url', 'labels', 'label_ids')
    for idx, field in enumerate(card_fields, 1):
        typer.secho(
            f'{idx}  '
            f'| {field}{(11 - len(field)) * " "}'
            f'| {getattr(card, field)}{(33 - len(field)) * " "}',
            fg=typer.colors.BLUE,
        )
    typer.secho('-' * 67, fg=typer.colors.BLUE)


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
