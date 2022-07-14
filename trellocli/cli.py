import os
from typing import Optional

import typer
from dotenv import load_dotenv

from . import __app_name__, __app_version__, messages
from .cli_printer import CliPrinter
from .trello_utils import TrelloClient

load_dotenv()
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


class TrelloConnector:
    """
    A simple class that initializes and returns a Trello client.

    The class tries to initialize a Trello client from environment variables first, and then from the given params.
    If nothing is found, a configuration exception is raised.

    The needed environment variables are two:
     - TRELLO_API_KEY
     - TRELLO_API_TOKEN
    A sample template is available in the ´trellocli/.env.template´ file.
    """
    def __init__(self, trello_api_key: str = None, trello_api_token: str = None):
        self.trello_api_key = os.getenv('TRELLO_API_KEY', default=trello_api_key)
        self.trello_api_token = os.getenv('TRELLO_API_TOKEN', default=trello_api_token)
        if not self.trello_api_key:
            typer.secho(messages.MSG_API_KEY_NOT_FOUND, fg=RED)
            raise typer.Exit(code=MISSING_CONFIGURATION_CODE)
        if not self.trello_api_token:
            typer.secho(messages.MSG_API_TOKEN_NOT_FOUND, fg=RED)
            raise typer.Exit(code=MISSING_CONFIGURATION_CODE)
        self.client = TrelloClient(self.trello_api_key, self.trello_api_token)


@app.command(name='list-boards')
def list_boards() -> None:
    """Get the list of Trello boards with name and ID."""
    trello = TrelloConnector()
    try:
        board_list = trello.client.get_board_list()
    except Exception as e:
        typer.secho(e, fg=RED)
        raise typer.Exit(code=GENERIC_ERROR_CODE)

    if len(board_list) == 0:
        typer.secho(messages.MSG_BOARDS_FOUND, fg=YELLOW)
        raise typer.Exit(code=GENERIC_ERROR_CODE)
    printer = CliPrinter(color=BLUE)
    printer.print_boards(boards=board_list)


@app.command(name='list-columns')
def list_columns_by_board_id(board_id: str = typer.Argument(...)) -> None:
    """Get the list of columns by board ID."""
    trello = TrelloConnector()
    try:
        board_columns = trello.client.get_board_columns(board_id)
    except Exception as e:
        typer.secho(e, fg=RED)
        raise typer.Exit(code=GENERIC_ERROR_CODE)

    if len(board_columns) == 0:
        typer.secho(messages.MSG_COLUMNS_FOUND, fg=YELLOW)
        raise typer.Exit(code=SUCCESS_CODE)
    printer = CliPrinter(color=BLUE)
    printer.print_columns(columns=board_columns)


@app.command(name='create-card')
def create_card_by_column_id(
        column_id: str = typer.Option(..., '--column', '-c', help=messages.MSG_COL_ID_HELP),
        name: str = typer.Option(..., prompt=messages.MSG_NAME_PROMPT, help=messages.MSG_NAME_HELP),
        comment: str = typer.Option(..., prompt=messages.MSG_COMMENT_PROMPT, help=messages.MSG_COMMENT_HELP),
        labels: str = typer.Option(..., prompt=messages.MSG_LABELS_PROMPT, help=messages.MSG_LABELS_HELP),
) -> None:
    """Create a new Trello card given the the board column ID."""
    trello = TrelloConnector()
    try:
        card = trello.client.create_card(column_id, name, comment, labels.split())
    except Exception as e:
        typer.secho(e, fg=RED)
        raise typer.Exit(code=GENERIC_ERROR_CODE)
    printer = CliPrinter(color=BLUE)
    printer.print_card(card=card)


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            '--version',
            '-v',
            help=messages.MSG_ECHO_VERSION,
            is_eager=True,
        ),
) -> None:
    if version:
        typer.echo(f'{__app_name__} v{__app_version__}')
    return
