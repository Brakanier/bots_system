from dotenv import load_dotenv
load_dotenv()

from os import getenv
API_ID = int(getenv('API_ID'))
API_HASH = str(getenv('API_HASH'))

__all__ = ['API_ID', 'API_HASH']