from discord.ext import commands
from discord import Object, app_commands, Interaction
from main import WhitelistBot
from utilities import MCClient, SuccessEmbed



async def setup(bot: WhitelistBot) -> None:
    await bot.add_cog(Say(bot), guilds=[Object(841127630564622366), Object(1218637404194214020), Object(1019608824023371866)])
    
    
class Say(commands.Cog):
    def __init__(self, bot: WhitelistBot) -> None:
        super().__init__()
        self.bot = bot
        
    @app_commands.command(name='broadcast', description='say something in the serverchat')
    async def broadcast(self, interaction: Interaction, message: str):
        with MCClient() as client:
            response = client.run(f'say [§2{interaction.user.name}§r]: {message}')
        embed = SuccessEmbed(description=f'Sent message:\n{message}')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    