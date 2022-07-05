import os

from dotenv import load_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv('TRELLO_API_KEY', default=None)
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN', default=None)
