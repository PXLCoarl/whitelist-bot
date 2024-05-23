from rcon.source import Client
import os


class MCClient(Client):
    def __init__(self):
        super().__init__(os.getenv('RCON_ADDRESS'), int(os.getenv('RCON_PORT')), passwd = os.getenv('RCON_PW'), timeout=1.5)