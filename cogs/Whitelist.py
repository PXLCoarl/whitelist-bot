from main import WhitelistBot
from discord import Object, app_commands, Interaction, ButtonStyle
from discord.ui import View, button, Button
from discord.ext import commands
from utilities import logger, check_username, ErrorEmbed, InfoEmbed, SuccessEmbed, MCClient, DataBaseUtils
import os

async def setup(bot: WhitelistBot) -> None:
    await bot.add_cog(Whitelist(bot), guild=Object(841127630564622366))
    
class ConfirmView(View):
    def __init__(self, *, new_name: str):
        super().__init__(timeout=None)
        self.new_name = new_name
        
    @button(label='Yes', style=ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: Button):
        db = DataBaseUtils()
        user = db.fetch_user(discord_id=interaction.user.id)
        if user == -1:
            await interaction.response.defer()
            return
        with MCClient() as client:
            client.run(f'whitelist remove {user.minecraft_name}')
            client.run(f'whitelist add {self.new_name}')
        with db.Session() as session:
            user.minecraft_name = self.new_name
            session.add(user); session.commit()
        embed = interaction.message.embeds[0]
        embed.description = f'Changed account to: {self.new_name}'
        await interaction.response.edit_message(embed=embed, view=None)
    
    @button(label='No', style=ButtonStyle.danger)
    async def refuse(self, interaction: Interaction, button: Button):
        db = DataBaseUtils()
        user = db.fetch_user(discord_id=interaction.user.id)
        if user == -1:
            await interaction.response.defer()
            return
        embed = interaction.message.embeds[0]
        embed.description = f'Kept account with username: {user.minecraft_name}'
        await interaction.response.edit_message(embed=embed, view=None)
        


class Whitelist(commands.Cog):
    def __init__(self, bot: WhitelistBot) -> None:
        super().__init__()
        self.bot = bot
        
    @app_commands.command(name='whitelist', description='create or edit your profile')
    async def whitelist(self, interaction: Interaction, minecraft_user_name: str):
        db = DataBaseUtils()
        name = check_username(minecraft_user_name)
        if not name:
            embed = ErrorEmbed(reason=f'No minecraft account with the name {minecraft_user_name} exists.')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            user = db.fetch_user(discord_id=interaction.user.id)
            if user == -1:
                embed = ErrorEmbed(reason=f'Something went wrong during a database operation.')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if user is False:
                state = db.insert_user(discord_id=interaction.user.id, discord_name=interaction.user.name, minecraft_name=name)
                try:
                    if not state:
                        raise Exception
                    
                    with MCClient() as client:
                        response = client.run('whitelist', 'add', name)
                        logger.info(response)
                    embed = SuccessEmbed(description=f'{name} has been added to the whitelist.\nHave fun playing :)')
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
                except Exception as error:
                    embed = ErrorEmbed(reason=f'can\'t connect to the server.\n{error = }')
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                
            else:
                embed = InfoEmbed(description=f'You already whitelisted an account with name: {user.minecraft_name}.\nDo you want to override that with account {name}?')
                view = ConfirmView(new_name=name)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)