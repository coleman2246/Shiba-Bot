from discord.ext import commands, tasks
import discord.utils
import discord
import Info
import re
import Warnings
import pandas as pd
from discord.utils import get
import requests
import CoinInfo
import json
import aiofiles
import re
import textdistance

class ChatCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.info = Info.ServerInformation("Data Files/server_info.json")
        
        self.counter = {}

        for channel in self.info.server_info["scam_channels"]:
            self.counter[channel] = 0


    @commands.command()
    async def chartex(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        message = self.info.server_info["chartex"]
        await ctx.send(message)

    @commands.command()
    async def twitter(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        message = self.info.server_info["twitter"]
        await ctx.send(message)

    @commands.command()
    async def contract(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()
        message = self.info.server_info["contract"]
        await ctx.send(message)

    @commands.command()
    async def website(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()
        message = self.info.server_info["website"]
        await ctx.send(message)

    @commands.command()
    async def leash_chart(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()
        message = self.info.server_info["leash_chart"]
        await ctx.send(message)


    @commands.command()
    async def leash_contract(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()
        message = self.info.server_info["leash_contract"]
        await ctx.send(message)

    @commands.command()
    async def market_cap(self,ctx):
        await self.bot.wait_until_ready()
        
        await ctx.send("This Command has been removed. Look at the online users to see marketcap")
        '''
        self.info.update()
        
        circ_supply = 1e15

        try:
            value = CoinInfo.get_shib_price_usd()
            await ctx.send("Current Shib Marketcap is ${}".format(f"{round(value*circ_supply):,}" ))
        except:
            print('Error getting price data')
        '''


    @commands.command()
    async def reddit(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        message = self.info.server_info["reddit"]
        await ctx.send(message)

    @commands.command()
    async def gas(self,ctx):
        await self.bot.wait_until_ready()
        self.info.update()

        try:
            gas =CoinInfo.CoinQuery().get_gas().split()
            message = "Fastest: {} Fast: {} Normal: {} ".format(gas[0],gas[1],gas[2])
        except:
            message = "Cannot get prices from https://ethgasstation.info/"

        await ctx.send(message)
    '''
    @commands.command()
    async def warn(self,ctx,user,*,reason):
        await self.bot.wait_until_ready()

        author = ctx.message.author

        guild = self.bot.get_guild(self.info.server_info["guild_id"])

        admin_role = guild.get_role(self.info.server_info["admin_id"])
        mod_role = guild.get_role(self.info.server_info["moderator_id"])
    

        if admin_role in author.roles or mod_role in author.roles:
                if user is None:
                    await ctx.send("This Command requires a user to warn")
                    return 
                #<@!114939079384104969>
                try:
                    user_id =  int(re.findall(r'\d+',user)[0])

                    user_obj = self.bot.get_user(user_id)
                except:
                    await ctx.send("Couldn't Find User")
                    return 

                if reason is None:
                    await ctx.send("Please Specifiy a reason for the warning")
                    return 
                

                db = Warnings.DataBaseManagement()

                db.insert_user_warnings(user_id,reason)
            
                df = db.query_user_warnings(user_id)

                warnings = df.shape[0]

                await ctx.send(str(df[["time","reason"]].head(15)))

                await ctx.send(user+ " You Have "+str(warnings)+ " warnings. For every warning you get past 2 messages you get muted for 2^warnings hours" )


                if warnings >= 2:
                    length = 2 ** warnings

                    try:
                        db.insert_user_muted(user_id,mute_length=length)
                    except:
                        await ctx.send("This User is already muted. This warn will count the next time they are warned.")
                        return 

                    await ctx.send(user+" You Have Been muted for "+str(length)+" hours")
                    
                    muted_role =  guild.get_role(self.info.server_info["mute_id"])
                    
                    try:
                        member = await guild.fetch_member(user_id)
                    except:
                        await ctx.send("This user could not be retreived")
                    
                    try:   
                        await member.add_roles(muted_role)
                    except:
                        await ctx.send("This user is already muted")
                    

        else:
            await ctx.send("Only Admins or Mods can use this command")
        '''

    def get_json(self,enpoint,request_type = "get",params = None):
        r = requests.Session()
        if(request_type == "get"):
            p = r.get(enpoint,json=params)
        else:
            p = r.post(enpoint,json=params)
        
        return p.json()

    @commands.command()
    async def leash_market_cap(self,ctx):
        await self.bot.wait_until_ready()
        
        URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"

        params = {
            "query" : "{ pair(id: \"0x874376be8231dad99aabf9ef0767b3cc054c60ee\"){   \n token1Price  }}"
        }         

        ETH_PARAM = {            
            "query": "{	pair(id: \"0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc\"){    token0Price  }}"
        } 
        circ_supply = 107646.849

        try:
            #json = CoinInfo.get_holders()
            #message = "Current Holders: "+str(json)
            price_in_eth = float(self.get_json(URL,request_type="post",params=params)["data"]["pair"]["token1Price"])
            eth_price = float(self.get_json(URL,request_type="post",params=ETH_PARAM)["data"]["pair"]["token0Price"])

            
             
            message = "This current leash Marketcap is ${}".format(f"{round(eth_price*circ_supply*eth_price):,}" )
        except:
            message = "Cannot get holders, likely api limitation by ethplorer.io"

        await ctx.send(message)

    @commands.command()
    async def leash_price_bot(self,ctx):
        await self.bot.wait_until_ready()

        message = "Leash Price Tracker discord link - " + self.info.server_info["leash_price_link"]
        await ctx.send(message)


    @commands.command()
    async def leash_holder_bot(self,ctx):
        await self.bot.wait_until_ready()

        message = "Leash Holder Tracker discord link - " + self.info.server_info["leash_holder_link"]
        await ctx.send(message)

    @commands.command()
    async def shib_pricer_bot(self,ctx):
        await self.bot.wait_until_ready()

        message = "Shib Price Tracker discord link - " + self.info.server_info["shib_pricer_bot_link"]
        await ctx.send(message)


    @commands.command()
    async def gas_tracker_bot(self,ctx):
        await self.bot.wait_until_ready()

        message = "Gas Tracker discord link - " + self.info.server_info["gas_price_link"]
        await ctx.send(message)

    @commands.command()
    async def shib_holder_bot(self,ctx):
        await self.bot.wait_until_ready()

        message = "Shib Holder Tracker bot discord link - " + self.info.server_info["shid_holder_bot"]
        await ctx.send(message)


    @commands.command()
    async def github(self,ctx):
        await self.bot.wait_until_ready()

        message = "https://github.com/coleman2246/Shiba-Bot"
        await ctx.send(message)

    @commands.command()
    async def market_crab(self,ctx):
        await self.bot.wait_until_ready()

        message = "<:crabbe:834946109809098753>"
        await ctx.send(message)

    @commands.command()
    async def board(self,ctx):
        if(not self.is_staff_member(ctx.author)):
            await ctx.channel.send("Only staff members can use this command.")
            return 
        
        async with aiofiles.open('Data Files/data.json', mode='r') as f:
            contents = await f.read()
        channel_data = json.loads(contents)
        await self.send_board_embed(ctx,channel_data)

    
    async def send_board_embed(self,ctx,channel_data):
        embed_dict = {}
        embed_dict["title"] = "Shib Staff Board"
        embed_dict["fields"] = []

        for curr_channel in channel_data.keys():
            if(len(channel_data[curr_channel]) != 0):
                
                chan_obj = await self.bot.fetch_channel(curr_channel)
                temp = {}
                temp["name"] = "**"+chan_obj.name+"**"

                temp["value"] = ""
                for member in channel_data[curr_channel]:
                    member_name = await ctx.guild.fetch_member(member)
                    temp["value"] += " **"+member_name.mention+"** "
                embed_dict["fields"].append(temp)
        

        await ctx.channel.send("",embed=discord.Embed.from_dict(embed_dict))

    async def assign_user(self,ctx,channel,user):
        
        async with aiofiles.open('Data Files/data.json', mode='r') as f:
            contents = await f.read()
        channel_data = json.loads(contents)

        try:
            channel = channel[2:-1]

            channel = await self.bot.fetch_channel(channel)

            if(int(user.id) in channel_data[str(channel.id)] ):
                channel_data[str(channel.id)].remove(int(user.id))
                await ctx.channel.send("User Removed from Channel")

            else:
                await ctx.channel.send("User Added to Channel")
                channel_data[str(channel.id)].append(user.id)
        except:
            await ctx.channel.send("Please Enter Valid Channel")
            return 



        await self.send_board_embed(ctx,channel_data)

        async with aiofiles.open('Data Files/data.json', mode='w') as f:
            await f.write(json.dumps(channel_data,indent=4))




    @commands.command()
    async def assign(self,ctx,channel,author=None):
        await self.bot.wait_until_ready()

        if(not self.is_staff_member(ctx.author)):
            await ctx.channel.send("Only staff members can use this command.")
            return 
        if(author == None):
            await self.assign_user(ctx,channel,ctx.author)
        else:
            try:
                auth_string = author[3:-1]
                user_obj = await ctx.guild.fetch_member(auth_string)
                print(user_obj)
            except:
                await ctx.channel.send("Invalid User Passed")
                return 

            await self.assign_user(ctx,channel,user_obj)



    @commands.command()
    async def members(self,ctx):
        shib_server = self.bot.get_guild(740287152843128944)
        await ctx.channel.send("There is Currently **{}** members in {}".format(shib_server.member_count,shib_server.name))


    @commands.Cog.listener()
    async def on_member_join(self,member):
        await self.bot.wait_until_ready()

        with open("Data Files/join_message") as f:
            data = f.read()

        print(member.name)
        await member.send(data)
        admins = ["LC","CAT","Trophias"]
        for admin in admins:
            regex = '(?i)^{}*'.format(admin)
            regexp = re.compile(regex)
            if regexp.search(member.name):

                await member.send("You have been kicked due to your name being too similar to a staff memebers")
                await member.kick(reason="You have been kicked due to your name being too similar to a staff memebers")
                break

        non_regex = "Bioluminescent Government Agents".upper()
        if(textdistance.levenshtein(non_regex,member.name.upper()) < 4):
            await member.send("You have been kicked due to your name being too similar to a staff memebers")
            await member.kick(reason="You have been kicked due to your name being too similar to a staff memebers")
        

    @commands.Cog.listener()
    async def on_message(self, ctx):
        await self.bot.wait_until_ready()
        
        if(ctx.channel.id in self.info.server_info["scam_channels"] and int(ctx.author.id) != 842892223162089503):
            
            if(self.counter[ctx.channel.id] >=  self.info.server_info["scam_channels_counts"][str(ctx.channel.id)] ):    
                #print(self.info.server_info["scam_channels_counts"][str(ctx.channel.id)])    
                
                name = "Scam Warning"
                
                admin_message = "Click on the mentions in the message to get in contact with admin.\n <@"
                actualDict = {"Warning" : self.info.server_info["scam_message"]}
                message = makeEmbed(name=name, values=actualDict)
                print(ctx.channel.name)
                await ctx.channel.send("",embed=message)
                
                self.counter[ctx.channel.id] = 0
            else:
                self.counter[ctx.channel.id] += 1

    
    def is_staff_member(self,user):
        user_roles = user.roles

        for curr_user_role in user_roles:
            if(int(curr_user_role.id) in self.info.server_info["staff_roles"]):
                return True

        return False


def makeEmbed(*, name=None, icon=None, colour=0xEB4034, values={}):
    '''Creates an embed messasge with specified inputs'''

    # Create an embed object with the specified colour
    embedObj = discord.Embed(colour=colour)

    # Set the author and URL
    embedObj.set_author(name=name)

    # Create all of the fields
    for i in values:
        if values[i] == '':
            values[i] = 'None'
        embedObj.add_field(name=i, value='{}'.format(values[i]))

    # Return to user
    return embedObj