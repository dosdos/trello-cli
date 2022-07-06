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


class ResourceUnavailable(Exception):
    def __init__(self, msg, http_response):
        Exception.__init__(self)
        self._msg = msg
        self._status = http_response.status_code

    def __str__(self):
        return "Resource not available (%s)" % self._msg


class Unauthorized(ResourceUnavailable):
    def __str__(self):
        return "Client not authorized (%s)" % self._msg


class TrelloClient:
    API_DOMAIN = 'https://api.trello.com/1/'
    API_BOARDS = 'members/me/boards/'
    API_BOARD_COLUMNS = 'boards/{board_id}/lists/'
    API_CARDS = 'cards/'
    API_COMMENTS = 'cards/{card_id}/actions/comments/'
    API_LABELS = 'cards/{card_id}/labels/'

    def __init__(self, api_key: str, token: str) -> None:
        self.session = requests.Session()
        self.session.headers.update({'content-type': 'application/json'})
        self.key = api_key
        self.token = token

    def api_request(self, path: str, method: str = 'GET', **extra_params) -> Any:
        url = f'{self.API_DOMAIN}{path}'
        params = {'key': self.key, 'token': self.token}
        params.update(**extra_params)
        response = self.session.request(method, url, params=params)
        if response.status_code == 401:
            raise Unauthorized(response.text, response)
        if response.status_code // 100 != 2:
            raise ResourceUnavailable("%s at %s" % (response.text, path), response)
        return response.json()

    def get_board_list(self) -> List[Board]:
        """Get the full list of Trello boards (both open and closed)."""
        response = self.api_request(path=self.API_BOARDS)
        return [Board(json_obj) for json_obj in response]

    def get_board_columns(self, board_id: str) -> List[Column]:
        query_params = {'cards': 'none', 'filter': 'open'}
        url = self.API_BOARD_COLUMNS.format(board_id=board_id)
        response = self.api_request(path=url, **query_params)
        return [Column(json_obj) for json_obj in response]

    def create_card(self, column_id: str, name: str, comment: str, labels: List[str]) -> Card:

        # Call Trello API to create a new card
        query_params = {'name': name, 'idList': column_id}
        response = self.api_request(
            path=self.API_CARDS,
            method='POST',
            **query_params,
        )
        card = Card(response)
        card.comment = comment
        card.labels = list(set(labels))  # Remove duplicates

        # Call Trello API to associate a new comment to that card
        query_params = {'text': comment}
        response = self.api_request(
            path=self.API_COMMENTS.format(card_id=card.id),
            method='POST',
            **query_params,
        )
        card.comment_id = response['id']
        card.label_ids = response['id']

        # Call Trello API to associate the list of new labels to that card
        label_ids = []
        for label in card.labels:
            query_params = {'color': 'lime', 'name': label}
            response = self.api_request(
                path=self.API_LABELS.format(card_id=card.id),
                method='POST',
                **query_params,
            )
            label_ids.append(response['id'])
        card.label_ids = label_ids

        return card
