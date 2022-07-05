class Board:
    def __init__(self, json_obj: dict) -> None:
        self.id = json_obj['id']
        self.name = json_obj['name']
        self.url = json_obj.get('url')
        self.description = json_obj.get('desc')
        self.closed = json_obj.get('closed')
        self.starred = json_obj.get('starred')

    def __repr__(self) -> str:
        return f'Board {self.name} [ID: {self.id}]'


class Column:
    def __init__(self, json_obj: dict) -> None:
        self.id = json_obj['id']
        self.board_id = json_obj['idBoard']
        self.name = json_obj['name']
        self.pos = json_obj.get('pos')

    def __repr__(self) -> str:
        return f'Column {self.name} [Board ID {self.board_id}]'


class Card:
    def __init__(self, json_obj: dict) -> None:
        self.id = json_obj['id']
        self.board_id = json_obj['idBoard']
        self.column_id = json_obj['idList']
        self.name = json_obj.get('name')
        self.comment = ''
        self.comment_id = None
        self.pos = json_obj.get('pos')
        self.short_url = json_obj.get('shortUrl')
        self.labels = []
        self.label_ids = []

    def __repr__(self) -> str:
        return f'Card "{self.name}" [Board ID {self.board_id}]'
