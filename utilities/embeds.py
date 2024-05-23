from datetime import datetime
from typing import Any
from discord import Colour, Embed


class ErrorEmbed(Embed):
    def __init__(self, *, reason: str = 'none given.'):
        super().__init__(colour = Colour.red(), title = 'Error', type='rich', description= f'An error has occured: \n{reason}', timestamp = datetime.now())
    
class SuccessEmbed(Embed):
    def __init__(self, *, description: str):
        super().__init__(colour=Colour.green(), title='Success', type='rich', description=description, timestamp=datetime.now())
        
class InfoEmbed(Embed):
    def __init__(self, *, description: str):
        super().__init__(colour=Colour.blurple(), title='Info', type='rich', description=description, timestamp=datetime.now())