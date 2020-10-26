import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass

from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
#from discord.ext.tasks import loop

#Primary area with commands.

class CardCog2(commands.Cog):
    """Commands for testing system goes here."""
    @commands.command()
    async def add_exp_old(self, ctx, *args): #Add card.
        '''
        syntax: cardGet [CardId] CustomId]
        Gets a random genre out of the character-info channel.  Exlcusively for Sakura Beat.
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.
        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        SingleUser=SingleUserProfile("New.")
        profile=SingleUser.getByID(auth.id)
        await channel.send("Old EXP="+str(profile.get_exp()))
        profile.set_exp(profile.get_exp()+10)
        profile=SingleUser.getByID(auth.id)
        await channel.send("New EXP="+str(profile.get_exp()))
        SingleUser.save_all()
        #await channel.send(str(newcard))
class CardCog(commands.Cog):
    """Commands for cards."""
    @commands.command(pass_context=True, aliases=['stampV'])
    async def stamp(self, ctx, *args):
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
    @commands.command(pass_context=True)
    async def numbertoimage(self, ctx, *args):
            bot=ctx.bot
            auth=ctx.message.author;
            channel=ctx.message.channel;
            leng=len(args)
            number=None
            if(leng==1):
                number=int(args[0])
            if(number!=None):
                with io.BytesIO() as image_binary:
                    makeNumber(number).save(image_binary, 'PNG') #Returns pil object.
                    image_binary.seek(0)
                    await channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(pass_context=True)
    async def my_profile(self, ctx, *args):
        """Returns the User's Profile.""""
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;

        user_id=author.id
        leng=len(args)
        profile=SingleUserProfile("B").getByID(user_id)
        diction_profile=profile.to_dictionary()
        number=None
        embed = discord.Embed(title=author.name, colour=discord.Colour(0xce48e9), description=" I dunno what should be the description.  Stuff I guess.  Makes it look a bit WIIIDER.", timestamp=datetime.datetime.today())
        embed.set_image(url=author.avatar_url)
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_author(name="profile", icon_url=author.avatar_url)
        embed.set_footer(text="myprofile command", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Coins", value= str(profile.get_coins()), inline=False)
        embed.add_field(name="Stars", value=str(profile.get_stars()), inline=False)
#embed.add_field(name="custom", value="Custom was applied.",)
        embed.add_field(name="Exp", value=str(profile.get_exp()), inline=True)
        embed.add_field(name="Level", value=str(profile.get_level()), inline=True)


        mess=await channel.send(content="", embed=embed)

    @commands.command(pass_context=True, aliases=['cardtest'])
    async def getimage(self, ctx, *args):
        """Get a image and return it."""
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        with io.BytesIO() as image_binary:
            make_summon_cost(1,1,1).save(image_binary, 'PNG') #Returns pil object.
            image_binary.seek(0)
            await channel.send(file=discord.File(fp=image_binary, filename='image.png'))



    @commands.command(pass_context=True)
    async def cardGet(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: cardGet [CardId] CustomId]
        Gets a random genre out of the character-info channel.  Exlcusively for Sakura Beat.
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.

        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        if(leng>=1):
            id=args[0]
            newcard=CardRetrievalClass().getByID(int(id, 16))
            await channel.send(str(newcard))
            if newcard!=False and leng>=2:
                text=await CustomRetrievalClass().getByID(args[1], bot)

                print(text.toCSV())

                newcard.apply_custom(custom=text)
            #    print(text)
                await channel.send(str(newcard))

                text.name="Daikon 02"
                await CustomRetrievalClass().updateCustomByID(text, bot)
