import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

from ..discordhelper.tiebreaker import *

class DPIOS:
    #Fil in later.
    def __init__(self, textchannel, user, bot):
        self.textchannel=textchannel #Text channel to send input to.
        self.user=user
        self.bot=bot

        self.input_buffer=[]
        print("tbd")
        #THE MESSAGES.
        self.image_msg=None
        self.player_msg=None
        self.current_msg=None
        self.image_embed=embed=discord.Embed(title="place", colour=discord.Colour(0x7289da))
        self.player_embed=embed=discord.Embed(title="place", colour=discord.Colour(0x7289da))
        self.current_embed=embed=discord.Embed(title="place", colour=discord.Colour(0x7289da))

    def has_something_in_buffer(self):
        if len(self.input_buffer)>0:
            return True
        return False
    def get_avatar_url(self):
        """returns the avatar url of the user"""
        return self.user.avatar_url

    #INPUT
    async def get_user_choice(self, choice_list, prompt="Select a choice."):
        #get command from user.
        """select a choice from a list.  Same as Tiebreaker.
        choice_list is a single list of strings.  prompt is a possible prompt.
        """
        choices=[]
        numberlist=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        defchoice=["back",[""], '🔙']
        choices.append(defchoice)
        outputString=""
        for i in range(0,len(choice_list)):
            name=choice_list[i]
            namelist=[name]
            emoji=numberlist[i]
            choices.append([choice_list[i], namelist, emoji])
            outputString=outputString + " {}[{}] ".format(emoji, name)
        messagecontent="{}\n{}".format(prompt, outputString)
        result, self.input_buffer=await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result
    async def get_user_card(self, choice_list, prompt=""):
        """select a cardobject from a list of card objects.  Same as Tiebreaker.
        choice_list is a single list of cardobjects.  prompt is a possible prompt.
        """
        choices=[]
        numberlist=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        defchoice=["back",[""], '🔙']
        choices.append(defchoice)
        outputString=""
        for i in range(0,len(choice_list)):
            name=choice_list[i].get_name()
            namelist=[name]
            emoji=numberlist[i]
            choices.append([choice_list[i], namelist, emoji])
            outputString=outputString + " {}[{}] ".format(emoji, name)
        messagecontent="{}\n{}".format(prompt, outputString)
        result, self.input_buffer=await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result
    async def get_user_piece(self, choice_list, prompt=""):
        """select a piece from a list of piece objects.  Same as Tiebreaker.
        choice_list is a single list of cardobjects.  prompt is a possible prompt.
        """
        choices=[]
        numberlist=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        defchoice=["back",[""], '🔙']
        choices.append(defchoice)
        outputString=""
        for i in range(0,len(choice_list)):
            name=choice_list[i].get_name()
            namelist=[name]
            emoji=numberlist[i]
            choices.append([choice_list[i], namelist, emoji])
            outputString=outputString + " {}[{}] ".format(emoji, name)
        messagecontent="{}\n{}".format(prompt, outputString)
        result, self.input_buffer=await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result
    async def get_user_command(self, actions, prompt="ENTER COMMAND:"):
        """get command from user.  Same as Tiebreaker.
        actions is a single list of strings.  Prompt is the prompt.
        """
        choices=[]
        local_commands=["OVERVIEW", "BOARD", "PLAYER", "CURRENT"]
        numberlist=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        defchoice=["exit",[""], '🔚']
        choices.append(defchoice)
        outputString=""
        if(len(actions)==1):
            #return the first action if there is no need.
            return actions[0]
        for i in range(0,len(actions)):
            name=actions[i]
            emoji=numberlist[i]
            choices.append([actions[i], [str(name)], emoji])
            outputString=outputString + " {}[{}] ".format(emoji, name)
        for comm in local_commands:
            choices.append([comm, [comm], None])
        messagecontent="{}\n{}".format(prompt, outputString)
        result, self.input_buffer=await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result

    #OUTPUT
    async def send_order(self, p=True, i=True, c=True):
        if p:
            self.player_msg = await self.textchannel.send("Player", embed=self.player_embed)
        if i:
            self.image_msg = await self.textchannel.send("Image", embed=self.image_embed)
        if c:
            self.current_msg = await self.textchannel.send("Current", embed=self.current_embed)
    async def send_announcement(self, announcement):
        await self.textchannel.send(announcement)
    async def update_current_message(self, embed):
        #For the current creature's turn.
        self.current_embed = embed
        if(self.current_msg==None):
            self.current_msg=await self.textchannel.send("Newly_sent", embed=embed)
        else:
            await self.current_msg.edit(content="$", embed=embed)
    async def update_player_message(self, embed):
        self.player_embed=embed
        if(self.player_msg==None):
            self.player_msg=await self.textchannel.send("Newly_sent", embed=embed)
        else:
            await self.player_msg.edit(content="$", embed=embed)
    async def update_grid_message(self, embed):
        #updates the grid image.
        #embed=discord.Embed(title="Map", colour=discord.Colour(0x7289da), description="Round: {}".format(round))
        #embed.set_image(url="{imgurl}".format(imgurl=iurl))
        self.image_embed=embed
        if(self.image_msg==None):
            self.image_msg=await self.textchannel.send("Newly_sent", embed=embed)
        else:
            await self.image_msg.edit(content="$", embed=embed)

    async def send_pil_image(self, pil):
        #sends pil image, but saves it to a image_binary first
        #returns message
        image_mes=None
        with io.BytesIO() as image_binary:
            pil.save(image_binary, 'PNG') #Returns pil object.
            image_binary.seek(0)
            image_mes=await self.textchannel.send(content="Preview:", file=discord.File(fp=image_binary, filename='image.png'))
        return image_mes
