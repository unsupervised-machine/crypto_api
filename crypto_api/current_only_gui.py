from nicegui import ui
from crypto_api import database

currencies = database.get_all_records(database.current_only)


