import unittest
from unittest import mock

from typer.testing import CliRunner

from test.fixtures import TRELLO_BOARDS_FIXTURE, TRELLO_COLUMNS_FIXTURE
from trellocli.trello_utils import TrelloClient

runner = CliRunner()


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    mocked_trello_api = {
        TrelloClient.API_DOMAIN + TrelloClient.API_BOARDS: TRELLO_BOARDS_FIXTURE,
        TrelloClient.API_DOMAIN + TrelloClient.API_BOARD_COLUMNS.format(board_id='123'): TRELLO_COLUMNS_FIXTURE,
    }

    # Arguments of requests method are: (http_status, url_path, params)
    if args[1] in mocked_trello_api.keys():
        return MockResponse(mocked_trello_api[args[1]], 200)
    return MockResponse(None, 404)


class TestCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.test_key = 'TEST-TRELLO-API-KEY'
        self.test_token = 'TEST-TRELLO-API-TOKEN'
        self.trello_client = TrelloClient(self.test_key, self.test_token)

    def test_client_init(self) -> None:
        client = self.trello_client
        self.assertEqual(client.key, self.test_key)
        self.assertEqual(client.token, self.test_token)

    @mock.patch('trellocli.trello_utils.requests.sessions.Session.request', side_effect=mocked_requests)
    def test_get_board_list(self, mock_get) -> None:
        # Test that the Trello client is returning the Board objects loaded from the fixture
        board_list = self.trello_client.get_board_list()
        for board in board_list:
            self.assertEqual(board.id, '123')
            self.assertEqual(board.name, 'Test Board Name')
            self.assertEqual(board.description, 'Test Board Desc')
            self.assertFalse(board.closed)
        # Test that mocked request was called with the right params
        self.assertEqual(list(mock_get.call_args)[0][0], 'GET')
        self.assertEqual(list(mock_get.call_args)[0][1], self.trello_client.API_DOMAIN + self.trello_client.API_BOARDS)
        self.assertEqual(list(mock_get.call_args)[1]['params']['key'], self.test_key)
        self.assertEqual(list(mock_get.call_args)[1]['params']['token'], self.test_token)

    @mock.patch('trellocli.trello_utils.requests.sessions.Session.request', side_effect=mocked_requests)
    def test_get_board_columns(self, mock_get) -> None:
        # Test that the Trello client is returning the Column objects loaded from the fixture
        column_list = self.trello_client.get_board_columns('123')
        for column in column_list:
            self.assertEqual(column.id[:4], 'abc-')
            self.assertEqual(column.board_id, '123')
            self.assertEqual(column.name, 'Col Name')
            self.assertIsInstance(column.pos, int)
        # Test that mocked request was called with the right params
        self.assertEqual(list(mock_get.call_args)[0][0], 'GET')
        self.assertEqual(
            list(mock_get.call_args)[0][1],
            self.trello_client.API_DOMAIN + self.trello_client.API_BOARD_COLUMNS.format(board_id='123'),
        )
        self.assertEqual(list(mock_get.call_args)[1]['params']['cards'], 'none')
        self.assertEqual(list(mock_get.call_args)[1]['params']['filter'], 'open')
        self.assertEqual(list(mock_get.call_args)[1]['params']['key'], self.test_key)
        self.assertEqual(list(mock_get.call_args)[1]['params']['token'], self.test_token)
