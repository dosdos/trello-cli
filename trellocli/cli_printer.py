import typer

from . import messages


class CliPrinter:
    """A simple tool to print results nicely on the CLI."""
    MAX_FIELD_LEN = 27
    CARD_HEADER_LEN = 67
    CARD_FIELD_KEY_PADDING_LEN = 11
    CARD_FIELD_VALUE_PADDING_LEN = 33

    def __init__(self, color: dict) -> None:
        self.color = color

    def print_boards(self, boards, truncate_names_at=MAX_FIELD_LEN):
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
                f'| {board.name[:truncate_names_at]}{(len(table_labels[2]) - len(str(board.name)) - 2) * " "}'
                f'| {board.closed}',
                fg=self.color,
            )
        typer.secho('-' * len(headers) + '\n', fg=self.color)

    def print_columns(self, columns, truncate_names_at=MAX_FIELD_LEN):
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
                f'| {col.name[:truncate_names_at]}{(len(table_labels[2]) - len(str(col.name)) - 2) * " "}',
                fg=self.color,
            )
        typer.secho('-' * len(headers) + '\n', fg=self.color)

    def print_card(self, card):
        typer.secho(messages.MSG_NEW_CARD_ADDED % card.id, fg=self.color, bold=True)
        typer.secho('-' * self.CARD_HEADER_LEN, fg=self.color)
        card_attrs = ('board_id', 'column_id', 'name', 'comment', 'comment_id', 'short_url', 'labels', 'label_ids')
        for idx, field in enumerate(card_attrs, 1):
            typer.secho(
                f'{idx}  '
                f'| {field}{(self.CARD_FIELD_KEY_PADDING_LEN - len(field)) * " "}'
                f'| {getattr(card, field)}{(self.CARD_FIELD_VALUE_PADDING_LEN - len(field)) * " "}',
                fg=self.color,
            )
        typer.secho('-' * 67, fg=self.color)
