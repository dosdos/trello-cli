import unittest
from unittest import mock

from typer.testing import CliRunner

from test.fixtures import TRELLO_BOARD_FIXTURE
from trellocli.trello_utils import TrelloClient

runner = CliRunner()


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[1] == TrelloClient.API_DOMAIN + TrelloClient.API_BOARDS:
        return MockResponse(TRELLO_BOARD_FIXTURE, 200)
    return MockResponse(None, 404)


class TestCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.test_key = 'TEST-TRELLO-API-KEY'
        self.test_token = 'TEST-TRELLO-API-TOKEN'
        self.trello_client = TrelloClient(self.test_key, self.test_token)
        self.fake_board_id = '123'
        self.trello_url_api_domain = 'https://api.trello.com/1/'
        self.trello_url_api_boards = 'members/me/boards/'
        self.trello_url_api_columns = f'boards/{self.fake_board_id}/lists/'

    def test_client_init(self) -> None:
        client = self.trello_client
        self.assertEqual(client.key, self.test_key)
        self.assertEqual(client.token, self.test_token)

    @mock.patch('trellocli.trello_utils.requests.sessions.Session.request', side_effect=mocked_requests)
    def test_get_board_list(self, mock_get) -> None:

        # Test that the Trello client is returning the objects loaded from the fixture
        board_list = self.trello_client.get_board_list()
        for board in board_list:
            self.assertEqual(board.id, self.fake_board_id)
            self.assertEqual(board.name, 'Test Board Name')
            self.assertEqual(board.description, 'Test Board Desc')
            self.assertFalse(board.closed)

        # Test that mocked request was called with the right params
        self.assertEqual(list(mock_get.call_args)[0][0], 'GET')
        self.assertEqual(list(mock_get.call_args)[0][1], self.trello_client.API_DOMAIN + self.trello_client.API_BOARDS)
        self.assertEqual(list(mock_get.call_args)[1]['params']['key'], self.test_key)
        self.assertEqual(list(mock_get.call_args)[1]['params']['token'], self.test_token)
