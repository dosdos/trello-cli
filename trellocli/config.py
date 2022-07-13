import os

from dotenv import load_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv('TRELLO_API_KEY', default=None)
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN', default=None)


# Messages
MSG_API_KEY_NOT_FOUND = 'Trello API key not found. Please, set the TRELLO_API_KEY value in the .env file.'
MSG_API_TOKEN_NOT_FOUND = 'Trello API token not found. Please, set the TRELLO_API_TOKEN value in the .env file.'
MSG_BOARDS_FOUND = 'No boards found.'
MSG_COLUMNS_FOUND = 'No columns found for this board.'
MSG_COL_ID_HELP = 'The ID of the column where the card will be added.'
MSG_NAME_PROMPT = 'The name is the title of the card.'
MSG_NAME_HELP = 'Add the title of the new card'
MSG_COMMENT_PROMPT = 'Add a comment to the new card.'
MSG_COMMENT_HELP = 'The comment is added to the new cards.'
MSG_LABELS_PROMPT = 'Add a list of labels separated by spaces.'
MSG_LABELS_HELP = 'Ensure the label is done by a single word.'
MSG_NEW_CARD_ADDED = 'A new Trello card has been created with ID %.'
MSG_ECHO_VERSION = 'Echo the app version.'
