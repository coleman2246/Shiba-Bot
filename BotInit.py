import discord
from discord.ext import commands
import BotCommands
import ChatHelper 
import Info


class BotAuth:
    def __init__(self):
        self.bot = commands.Bot(command_prefix='$')
        self.info = Info.ServerInformation("Data Files/server_info.json")


class ShibInformer(BotAuth):
    def __init__(self):
        super().__init__()
        print("Starte shib informer")
        self.bot.add_cog(ChatHelper.ChatCommands(self.bot))
        self.key = self.info.server_info["shib_informer"]
        

class ShibPriceUpdates(BotAuth):
    def __init__(self):
        super().__init__()
        print("Starte shib usd price update")
        #self.bot.add_cog(ChatHelper.ChatCommands(self.bot))


        self.bot.add_cog(BotCommands.UpdateShibPrice(self.bot))
        self.bot.get_cog("UpdateShibPrice").do_task.start()
        #self.bot.get_cog("UpdateShibPrice").unmute_users.start()

        
        self.key = self.info.server_info["usd_bot_api_key"]
        self.bot.help_command = None
        
class HourVolumeUpdate(BotAuth):
    def __init__(self):
        super().__init__()
        print("Started shib Hour Update")

        self.bot.add_cog(BotCommands.UpdateVolumeHourly(self.bot))
        self.bot.get_cog("UpdateVolumeHourly").do_task.start()
    

        self.key = self.info.server_info["vol_bot_api_key"]
        
        self.bot.help_command = None

class GasPriceUpdate(BotAuth):
    def __init__(self):
        super().__init__()

        print("Started Gas Updates")
        self.bot.add_cog(BotCommands.UpdateGasPrice(self.bot))
        self.bot.get_cog("UpdateGasPrice").do_task.start()
    

        self.key = self.info.server_info["eth_gas_bot_key"]
        
        self.bot.help_command = None

class ShibHolderUpdates(BotAuth):
    def __init__(self):
        super().__init__()

        print("Started shib Holder Updates")
        self.bot.add_cog(BotCommands.UpdateShibHolders(self.bot))
        self.bot.get_cog("UpdateShibHolders").do_task.start()
    
        self.key = self.info.server_info["holders_bot_key"]
        
        self.bot.help_command = None


class LeashPriceUpdates(BotAuth):
    def __init__(self):
        super().__init__()

        print("Started Leash price Updates")
        self.bot.add_cog(BotCommands.UpdateLeashPriceUSD(self.bot))
        self.bot.get_cog("UpdateLeashPriceUSD").do_task.start()
    
        self.key = self.info.server_info["leash_bot_key"]
        
        self.bot.help_command = None

class LeashHolderUpdates(BotAuth):
    def __init__(self):
        super().__init__()

        print("Started Leash holder Updates")
        self.bot.add_cog(BotCommands.UpateLeashHolder(self.bot))
        self.bot.get_cog("UpateLeashHolder").do_task.start()
    
        self.key = self.info.server_info["leash_holder_key"]
        
        self.bot.help_command = None


class ShibMarketCapUpdates(BotAuth):
    def __init__(self):
        super().__init__()

        print("Started Shib Marketcap Updates")
        self.bot.add_cog(BotCommands.UpdateShibMarketCap(self.bot))
        self.bot.get_cog("UpdateShibMarketCap").do_task.start()
    
        self.key = self.info.server_info["shib_markt_cap"]
        
        self.bot.help_command = None

