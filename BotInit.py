import discord
from discord.ext import commands
import BotCommands
import ChatHelper 
import Info


class BotAuth:
    def __init__(self):
        self.bot = commands.Bot(command_prefix='$')
        self.info = Info.ServerInformation("Data Files/server_info.json")
    

class PriceUpdateBotUSD(BotAuth):
    def __init__(self):
        super().__init__()
        print("Starte usd price update")
        self.bot.add_cog(ChatHelper.ChatCommands(self.bot))


        self.bot.add_cog(BotCommands.UpdatePriceUSD(self.bot))
        self.bot.get_cog("UpdatePriceUSD").update_username.start()


        self.key = self.info.server_info["usd_bot_api_key"]
        
class HourVolumeUpdate(BotAuth):
    def __init__(self):
        super().__init__()
        print("Started Hour Update")

        self.bot.add_cog(BotCommands.UpdateVolumeHourly(self.bot))
        self.bot.get_cog("UpdateVolumeHourly").update_username.start()
    

        self.key = self.info.server_info["vol_bot_api_key"]
        
        self.bot.help_command = None

class GasPriceUpdate(BotAuth):
    def __init__(self):
        super().__init__()

        print("Started Gas Updates")
        self.bot.add_cog(BotCommands.UpdateGasPrice(self.bot))
        self.bot.get_cog("UpdateGasPrice").update_username.start()
    

        self.key = self.info.server_info["eth_gas_bot_key"]
        
        self.bot.help_command = None

