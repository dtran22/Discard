import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv

from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass

from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
#from discord.ext.tasks import loop

#Make debug commands here

class DebugCog(commands.Cog):
    """Commands for testing the system goes here."""
    @commands.command()
    async def add_exp(self, ctx, *args): #A example command.
        '''
        syntax: add_exp
        Add 10 exp to the user who invokes this command.

        '''
        bot=ctx.bot #The refrence to the bot object. https://discordpy.readthedocs.io/en/latest/ext/commands/api.htm?highlight=bot#bot
        author=ctx.message.author;  #The refrence to the message author.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=user#user
        channel=ctx.message.channel; #the refrence to the channel this message was sent in.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=textchannel#textchannel
        SingleUser=SingleUserProfile("arg") #Singleton Object that gets a user based on their id.

        user_id=author.id
        profile=SingleUser.getByID(user_id)
        await channel.send("Old EXP="+str(profile.get_exp()))
        profile.set_exp(profile.get_exp()+10)
        profile=SingleUser.getByID(user_id)
        await channel.send("New EXP="+str(profile.get_exp()))
        SingleUser.save_all()
        #await channel.send(str(newcard))

    @commands.command()
    async def add_coins(self, ctx, *args):
        #increase the coins in user's account by the amount passed in the argument
        #if no argument is passed, then increase the coins by 4
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(len(args) > 1):
            await channel.send("Please enter either the command only or the command with 1 other integer only.")
        else:
            if(len(args) == 0):
                profile.set_coins(profile.get_coins() + 4)
                await channel.send("4 coins have been added to your account.\nCoins = " + str(profile.get_coins()))
            else:
                if(args[0].isdigit() == True):
                    profile.set_coins(profile.get_coins() + int(args[0]))
                    await channel.send("{} coins have been added to your account.\nCoins = ".format(int(args[0], profile.get_coins())))
                else:
                    await channel.send("Invalid input.")
        SingleUser.save_all()

    @commands.command()
    async def increase_stars(self, ctx):
        #increase the amount of the user's stars by 1 if their coins are greater than or equal to 20
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(profile.get_coins() >= 20):
            await channel.send("Old Stars = " + str(profile.get_stars()))
            await channel.send("Old Coins = " + str(profile.get_coins()))
            profile.set_stars(profile.get_stars() + 1)
            profile.set_coins(profile.get_coins() - 20)
            await channel.send("New Stars = " + str(profile.get_stars()))
            await channel.send("New Coins = " + str(profile.get_coins()))
        SingleUser.save_all()

    @commands.command()
    async def increase_level(self, ctx):
        #increase the user's level by 1 if their exp is greater than or equal to 100
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(profile.get_exp() >= 100):
            await channel.send("Old Level = " + str(profile.get_level()))
            await channel.send("Old EXP = " + str(profile.get_exp()))
            profile.set_level(profile.get_level() + 1)
            profile.set_exp(profile.get_exp() - 100)
            await channel.send("New Level = " + str(profile.get_level()))
            await channel.send("New EXP = " + str(profile.get_exp()))
        SingleUser.save_all()

    @commands.command()
    async def add_card(self, ctx, *args):
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        card_id=args[0]
        if(CardRetrievalClass().getByID(int(card_id, 16)) == False):
            channel.send("Card does not exist")
        else:
            profile.add_card(card_id)
        SingleUser.save_all()