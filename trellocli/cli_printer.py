import typer

from . import config


class CliPrinter:
    """A simple tool to print results nicely on the CLI."""

    def __init__(self, color: dict) -> None:
        self.color = color

    def print_boards(self, boards):
        table_labels = (
            '#  ',
            '| Board ID                   ',
            '| Board Name                 ',
            '| Closed  ',
        )
        headers = ''.join(table_labels)
        typer.secho(headers, fg=self.color, bold=True)
        typer.secho('-' * len(headers), fg=self.color)
        for idx, board in enumerate(boards, 1):
            typer.secho(
                f'{idx}{(len(table_labels[0]) - len(str(idx))) * " "}'
                f'| [{board.id}] '
                f'| {board.name[:27]}{(len(table_labels[2]) - len(str(board.name)) - 2) * " "}'
                f'| {board.closed}',
                fg=self.color,
            )
        typer.secho('-' * len(headers) + '\n', fg=self.color)

    def print_columns(self, columns):
        table_labels = (
            '#  ',
            '| Column ID                  ',
            '| Column Name       ',
        )
        headers = ''.join(table_labels)
        typer.secho(headers, fg=self.color, bold=True)
        typer.secho('-' * len(headers), fg=self.color)
        for idx, col in enumerate(columns, 1):
            typer.secho(
                f'{idx}{(len(table_labels[0]) - len(str(idx))) * " "}'
                f'| [{col.id}] '
                f'| {col.name[:27]}{(len(table_labels[2]) - len(str(col.name)) - 2) * " "}',
                fg=self.color,
            )
        typer.secho('-' * len(headers) + '\n', fg=self.color)

    def print_card(self, card):
        typer.secho(config.MSG_NEW_CARD_ADDED % card.id, fg=self.color, bold=True)
        typer.secho('-' * 67, fg=self.color)
        card_fields = ('board_id', 'column_id', 'name', 'comment', 'comment_id', 'pos', 'short_url', 'labels', 'label_ids')
        for idx, field in enumerate(card_fields, 1):
            typer.secho(
                f'{idx}  '
                f'| {field}{(11 - len(field)) * " "}'
                f'| {getattr(card, field)}{(33 - len(field)) * " "}',
                fg=self.color,
            )
        typer.secho('-' * 67, fg=self.color)
