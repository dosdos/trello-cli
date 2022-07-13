from typing import Optional

import typer

from . import __app_name__, __app_version__, config
from .trello_utils import TrelloClient

app = typer.Typer()

SUCCESS_CODE = 0
GENERIC_ERROR_CODE = 1
MISSING_CONFIGURATION_CODE = 2
JSON_ERROR_CODE = 3

ERROR_LABELS = {
    SUCCESS_CODE: "success",
    GENERIC_ERROR_CODE: "generic error",
    MISSING_CONFIGURATION_CODE: "missing configuration error",
    JSON_ERROR_CODE: "json codification error",
}

BLUE = typer.colors.BLUE
RED = typer.colors.RED
YELLOW = typer.colors.YELLOW


def get_trello_connector() -> TrelloClient:
    if not config.TRELLO_API_KEY:
        typer.secho(config.MSG_API_KEY_NOT_FOUND, fg=RED)
        raise typer.Exit(code=MISSING_CONFIGURATION_CODE)
    if not config.TRELLO_API_TOKEN:
        typer.secho(config.MSG_API_TOKEN_NOT_FOUND, fg=RED)
        raise typer.Exit(code=MISSING_CONFIGURATION_CODE)
    return TrelloClient(config.TRELLO_API_KEY, config.TRELLO_API_TOKEN)


@app.command(name='list-boards')
def list_boards() -> None:
    """Get the list of Trello boards with name and ID."""
    trello_connector = get_trello_connector()
    try:
        board_list = trello_connector.get_board_list()
    except Exception as e:
        typer.secho(e, fg=RED)
        raise typer.Exit(code=GENERIC_ERROR_CODE)

    if len(board_list) == 0:
        typer.secho(config.MSG_BOARDS_FOUND, fg=YELLOW)
        raise typer.Exit(code=GENERIC_ERROR_CODE)

    columns = (
        '#  ',
        '| Board ID                   ',
        '| Board Name                 ',
        '| Closed  ',
    )
    headers = ''.join(columns)
    typer.secho(headers, fg=BLUE, bold=True)
    typer.secho('-' * len(headers), fg=BLUE)
    for idx, board in enumerate(board_list, 1):
        typer.secho(
            f'{idx}{(len(columns[0]) - len(str(idx))) * " "}'
            f'| [{board.id}] '
            f'| {board.name[:27]}{(len(columns[2]) - len(str(board.name)) - 2) * " "}'
            f'| {board.closed}',
            fg=BLUE,
        )
    typer.secho('-' * len(headers) + '\n', fg=BLUE)


@app.command(name='list-columns')
def list_columns_by_board_id(board_id: str = typer.Argument(...)) -> None:
    """Get the list of columns by board ID."""
    trello_connector = get_trello_connector()
    try:
        board_columns = trello_connector.get_board_columns(board_id)
    except Exception as e:
        typer.secho(e, fg=RED)
        raise typer.Exit(code=GENERIC_ERROR_CODE)

    if len(board_columns) == 0:
        typer.secho(config.MSG_COLUMNS_FOUND, fg=YELLOW)
        raise typer.Exit(code=SUCCESS_CODE)

    columns = (
        '#  ',
        '| Column ID                  ',
        '| Column Name       ',
    )
    headers = ''.join(columns)
    typer.secho(headers, fg=BLUE, bold=True)
    typer.secho('-' * len(headers), fg=BLUE)
    for idx, col in enumerate(board_columns, 1):
        typer.secho(
            f'{idx}{(len(columns[0]) - len(str(idx))) * " "}'
            f'| [{col.id}] '
            f'| {col.name[:27]}{(len(columns[2]) - len(str(col.name)) - 2) * " "}',
            fg=BLUE,
        )
    typer.secho('-' * len(headers) + '\n', fg=BLUE)


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
        typer.secho(e, fg=RED)
        raise typer.Exit(code=GENERIC_ERROR_CODE)

    typer.secho(config.MSG_NEW_CARD_ADDED % card.id, fg=BLUE, bold=True)
    typer.secho('-' * 67, fg=BLUE)
    card_fields = ('board_id', 'column_id', 'name', 'comment', 'comment_id', 'pos', 'short_url', 'labels', 'label_ids')
    for idx, field in enumerate(card_fields, 1):
        typer.secho(
            f'{idx}  '
            f'| {field}{(11 - len(field)) * " "}'
            f'| {getattr(card, field)}{(33 - len(field)) * " "}',
            fg=BLUE,
        )
    typer.secho('-' * 67, fg=BLUE)


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            '--version',
            '-v',
            help=config.MSG_ECHO_VERSION,
            is_eager=True,
        ),
) -> None:
    if version:
        typer.echo(f'{__app_name__} v{__app_version__}')
    return
