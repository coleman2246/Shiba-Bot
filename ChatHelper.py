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
import asyncio
import re
import textdistance
import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import urllib
from skimage.metrics import structural_similarity as ssim
from scipy.spatial.distance import euclidean
import requests
import time
import unidecode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

class ChatCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.info = Info.ServerInformation("Data Files/server_info.json")
        
        self.counter = {}
        self.counter_locks = {}
        
        for channel in self.info.server_info["scam_channels"]:
            self.counter[channel] = 0
            self.counter_locks[channel] = asyncio.Lock()

        self.board_lock = asyncio.Lock()
        self.white_list_lock = asyncio.Lock()
        

        client = self.info.server_info["twitch_client"]
        sec = self.info.server_info["twitch_secret"]
        
        
        response = requests.post(f"https://id.twitch.tv/oauth2/token"
                                        f"?client_id={client}"
                                        f"&client_secret={sec}"
                                        "&grant_type=client_credentials")
        
        if response.status_code == 200:
            self.bearer_token = response.json()['access_token']

            self.headers = { "client-id": self.info.server_info["twitch_client"],
                        "Authorization": "Bearer "+self.bearer_token
            }

        self.notify_channels = self.info.server_info["twtich_watchlist"]
        self.notify_times = {}
        self.notify_times_lock = {}


        for i in self.notify_channels:
            self.notify_times[i] = {}
            self.notify_times[i]["time-last-online"] = np.inf
            self.notify_times[i]["already-notified"] = False
            #self.notify_times_lock[i] =  asyncio.Lock()



    @tasks.loop(seconds=60,reconnect=True)
    async def notify_twitch_live(self):
        await self.bot.wait_until_ready()
        notify_channel = await self.bot.fetch_channel(844468484036493352)
        for i in self.notify_channels:
            live = self.is_live(i)

            if live:
                self.notify_times[i]["time-last-online"] = int(time.time())
                if not self.notify_times[i]["already-notified"]:
                    await notify_channel.send("{} is streaming on https://twitch.tv/{}".format(i,i))
                    self.notify_times[i]["already-notified"] = True

            else:  
                if int(time.time()) - self.notify_times[i]["time-last-online"] > 600:
                    self.notify_times[i]["already-notified"] = False


        

    def is_live(self,channel):
        if self.bearer_token == None:
            raise ValueError("Bearer Token has not been set")
        end_point = "https://api.twitch.tv/helix/search/channels?query={}".format(channel)

        r = requests.get(end_point, headers=self.headers)

        if r.status_code == 200:
            return r.json()["data"][0]["is_live"]
        else:
            raise ValueError("Bearer token was not authenicated by twitch")

    @commands.command()
    async def whitelist(self,ctx,member):
        await self.bot.wait_until_ready()

        if(not self.is_staff_member(ctx.author)):
            await ctx.channel.send("Only staff members can use this command.")
            return 
    
        try:
            member_string = member
            user_obj = await ctx.guild.fetch_member(int(member_string))

            await self.white_list_lock.acquire()
        
            with open('Data Files/whitelist.json', 'r') as f:
                white_list = json.load(f)
        
            white_list["whitelist"].append(int(user_obj.id))
            
            with open('Data Files/whitelist.json', 'w') as f:
                json.dump(white_list,f,indent=4)

            
            await ctx.channel.send("{} Added to the whiltelist".format(user_obj.mention))

        except:
            await ctx.channel.send("Invalid User Passed. Example usage is $whitelist userid")
            print("Invalid User passed.")
            return 
        self.white_list_lock.release()




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
    async def bone_price_bot(self,ctx):
        await self.bot.wait_until_ready()

        message = "Bone Price Tracker discord link - " + self.info.server_info["bone_price_link"]
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
    
        await self.board_lock.acquire()
        
        with open('Data Files/data.json', 'r') as f:
            channel_data = json.load(f)
        
        self.board_lock.release()
        
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
        await self.board_lock.acquire()
            
        
        with open('Data Files/data.json', 'r') as f:
            channel_data = json.load(f)
        
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
            self.board_lock.release()
            return

 

        await self.send_board_embed(ctx,channel_data)

        with open('Data Files/data.json', 'w') as f:
            json.dump(channel_data,f,indent=4)


        self.board_lock.release()
 
    
    @tasks.loop(seconds=60*10,reconnect=True)
    async def imposter(self):
        await self.bot.wait_until_ready()

        notify_channel = await self.bot.fetch_channel(844468484036493352)

        guild = self.bot.get_guild(740287152843128944)
        members = await guild.chunk()
        print(len(members),guild.member_count,guild.name)        
        staff_members = []

        for role_id in self.info.server_info["staff_roles"]:
            curr_role = guild.get_role(role_id)

            staff_members += curr_role.members

        staff_names = []
        staff_pics = {}

        print("Getting Staff Images")



 
        for i in staff_members:
            if i.nick == None:
                staff_names.append(i.name)
            else:
                staff_names.append(i.nick)
            
            img = await i.avatar_url_as(static_format="jpg",size=32).read()
            stream = io.BytesIO(img)


            img = Image.open(stream).convert('RGB') 
            #img.show(command='fim')
            
            open_cv_image = np.array(img) 
            open_cv_image = open_cv_image[:, :, ::-1].copy() 
            gray = cv.cvtColor(open_cv_image,cv.COLOR_BGR2GRAY)
            
            #kp, des = sift.detectAndCompute(gray,None)
            staff_pics[i.id] = gray  

        print("Started loop")
        similar_names = []

        banned_words = ["admin","mod","support"]

        await self.white_list_lock.acquire()
    
        with open('Data Files/whitelist.json', 'r') as f:
            white_list = json.load(f)["whitelist"]
        self.white_list_lock.release()

        for memeber_depth,member in enumerate(members):
            effective_name = unidecode.unidecode(member.name)

            if member.id not in white_list:                        
                status = member.activity
                if(status != None and isinstance(status,discord.CustomActivity) and status.name != None ):
                    for word in banned_words:
                        if word.upper() in status.name.upper():
                            await notify_channel.send("Forbidden Status Words: {} Member: {} Status: {}".format(word,member.mention,status.name))      

                for i,staff in enumerate(staff_members):
                        
                    if staff.id != member.id:
                        staff_start = staff_names[i].split()[0]
                        
                        if(staff_start.upper()[:3] in effective_name.upper()):
                            
                            distance = textdistance.levenshtein(staff_names[i].upper(),effective_name.upper())
                            if(distance < 8):
                                member_pic = await member.avatar_url_as(static_format="jpg",size=32).read()

                                stream = io.BytesIO(member_pic)


                                img = Image.open(stream).convert('RGB') 
                                #img.show(command='fim')
                                
                                open_cv_image = np.array(img) 
                                open_cv_image = open_cv_image[:, :, ::-1].copy() 
                                gray = cv.cvtColor(open_cv_image,cv.COLOR_BGR2GRAY)
                                dim = (32, 32)
                                gray = cv.resize(gray,dim,interpolation = cv.INTER_AREA)

                                s = ssim(gray,staff_pics[staff.id])
                                #print(("Staff: {} Member: {} Name Distance: {} Picture Similairty: {}".format(staff_names[i],member.mention,distance,s)))
                                if(s > .25 or (distance < 3 and s > .15)  ):
                                    await notify_channel.send("Staff: {} Member: {} Name Distance: {} Picture Similairty: {}".format(staff_names[i],member.mention,distance,s))
              
        print("Done Loop")
    
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
                print(auth_string)
                user_obj = await ctx.guild.fetch_member(int(auth_string))
            except:
                await ctx.channel.send("Invalid User Passed. Example usage is $assign #channel @user")
                print("Invalid User passed.")
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

        await member.send(data)

        staff_members = []
        staff_pics = {}
        shib_server = self.bot.get_guild(740287152843128944)

        for role_id in self.info.server_info["staff_roles"]:
            curr_role = shib_server.get_role(role_id)

            staff_members += curr_role.members
        
        for i in staff_members:
            img = await i.avatar_url_as(static_format="jpg",size=32).read()
            stream = io.BytesIO(img)


            img = Image.open(stream).convert('RGB') 
            
            open_cv_image = np.array(img) 
            open_cv_image = open_cv_image[:, :, ::-1].copy() 
            gray = cv.cvtColor(open_cv_image,cv.COLOR_BGR2GRAY)
            
            staff_pics[i.id] = gray  



        staff_names = []

        for i in staff_members:
            if i.nick == None:
                staff_names.append(i.name)
            else:
                staff_names.append(i.nick)
            
        effective_name = unidecode.unidecode(member.name)

        for i,staff in enumerate(staff_members):
                    
            if staff.id != member.id:
                staff_start = staff_names[i].split()[0]
                
                if(staff_start.upper()[:3] in effective_name.upper()):
                    
                    distance = textdistance.levenshtein(staff_names[i].upper(),effective_name.upper())
                    if(distance < 5):
                        member_pic = await member.avatar_url_as(static_format="jpg",size=32).read()

                        stream = io.BytesIO(member_pic)


                        img = Image.open(stream).convert('RGB') 
                        #img.show(command='fim')
                        
                        open_cv_image = np.array(img) 
                        open_cv_image = open_cv_image[:, :, ::-1].copy() 
                        gray = cv.cvtColor(open_cv_image,cv.COLOR_BGR2GRAY)
                        dim = (32, 32)
                        gray = cv.resize(gray,dim,interpolation = cv.INTER_AREA)

                        s = ssim(gray,staff_pics[staff.id])
                        #print(("Staff: {} Member: {} Name Distance: {} Picture Similairty: {}".format(staff_names[i],member.mention,distance,s)))
                        if(s > .25 or distance < 3):
                            await member.send("You have been kicked due to your name being too similar to a staff memebers")
                            #await ctx.channel.send("Staff: {} Member: {} Name Distance: {} Picture Similairty: {}".format(staff_names[i],member.mention,distance,s))
                            break


    @commands.Cog.listener()
    async def on_message(self, ctx):
        await self.bot.wait_until_ready()
        
        if(ctx.channel.id in self.info.server_info["scam_channels"] and int(ctx.author.id) != 842892223162089503):
            
            await self.counter_locks[ctx.channel.id].acquire()
            count = self.counter[ctx.channel.id]

            if( count >=  self.info.server_info["scam_channels_counts"][str(ctx.channel.id)] ):    
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
        
            self.counter_locks[ctx.channel.id].release()

    
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