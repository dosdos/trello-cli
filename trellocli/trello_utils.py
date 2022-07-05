from typing import Any, List

import requests


class Board:
    """
    Trello Boards.
    The Board ID and name are required fields.
    Docs: https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-group-boards
    """
    def __init__(self, json_obj: dict) -> None:
        self.id = json_obj['id']  # required
        self.name = json_obj['name']  # required
        self.url = json_obj.get('url')
        self.description = json_obj.get('desc')
        self.closed = json_obj.get('closed')
        self.starred = json_obj.get('starred')

    def __repr__(self) -> str:
        return f'Board {self.name} [ID: {self.id}]'


class Column:
    """
    The columns in a Trello Board are called "Lists" in the API doc.
    The parent Board, the Column ID and the Column name are required fields.
    Docs: https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-lists-get
    """
    def __init__(self, json_obj: dict) -> None:
        self.id = json_obj['id']  # required
        self.board_id = json_obj['idBoard']  # required (from the parent Board)
        self.name = json_obj['name']  # required
        self.pos = json_obj.get('pos')

    def __repr__(self) -> str:
        return f'Column {self.name} [Board ID {self.board_id}]'


class Card:
    """
    Trello Cards.
    The parent Column, the Card ID and the Card name are required fields.
    Docs: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-group-cards
    """
    def __init__(self, json_obj: dict) -> None:
        self.id = json_obj['id']  # required
        self.board_id = json_obj['idBoard']  # required (from the parent Board)
        self.column_id = json_obj['idList']  # required (from the parent List)
        self.name = json_obj.get('name')
        self.comment = ''
        self.comment_id = None
        self.pos = json_obj.get('pos')
        self.short_url = json_obj.get('shortUrl')
        self.labels = []
        self.label_ids = []

    def __repr__(self) -> str:
        return f'Card "{self.name}" [Board ID {self.board_id}]'


class TrelloClient:
    API_DOMAIN = 'https://api.trello.com/1/'
    API_BOARDS = 'members/me/boards/'

    def __init__(self, api_key: str, token: str) -> None:
        self.session = requests.Session()
        self.key = api_key
        self.token = token

    def api_request(self, path: str, method: str = 'GET') -> Any:
        url = f'{self.API_DOMAIN}{path}'
        params = {'key': self.key, 'token': self.token}
        response = self.session.request(method, url, params=params)
        return response.json()

    def get_board_list(self) -> List[Board]:
        """Get the full list of Trello boards (both open and closed)."""
        response = self.api_request(path=self.API_BOARDS)
        return [Board(json_obj) for json_obj in response]
