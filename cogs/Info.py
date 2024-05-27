from main import WhitelistBot
from discord import app_commands, Object, Interaction
from discord.ext import commands
from rcon.source import Client
from utilities import InfoEmbed, ErrorEmbed, MCClient
import os

async def setup(bot: WhitelistBot) -> None:
    await bot.add_cog(Info(bot))
    
    
class Info(commands.Cog):
    def __init__(self, bot: WhitelistBot) -> None:
        super().__init__()
        self.bot = bot
        
        
    @app_commands.command(name='info', description='get server info')
    async def info(self, interaction: Interaction):
        try:
            with MCClient() as client:
                parts: list[str] = client.run('list').split(':')
        except Exception as error:
            embed = ErrorEmbed(reason=f'can\'t connect to the server.\n{error = }')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        if len(parts) > 1:
            player_list = parts[1].strip()
            players = player_list.split(', ') if player_list else []
        else:
            players = []
        
        embed = InfoEmbed(description=f'{parts[0]}:\n-{'\n-'.join(players)}\n\nIP: {os.getenv('SERVER_ADDRESS')}')
        await interaction.response.send_message(embed=embed, ephemeral=True)