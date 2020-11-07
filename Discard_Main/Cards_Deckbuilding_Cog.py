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
from .classes.discordhelper.tiebreaker import make_tiebreaker, card_multimatch
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.Cards.DeckBuilding import *
#from discord.ext.tasks import loop

#Primary area with commands.


class DeckCog(commands.Cog):
    """Commands for deck management."""
    @commands.command(pass_context=True)
    async def createDeck(self, ctx, *args):
        '''
        syntax: createDeck [Name]
        [Name]: The name of the new deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(len(args) == 1):
            deckName = args[0]
            deck = Deck()
            deck.set_deck_name(deckName)
            for i in profile.get_decks():
                if(i.get_deck_name() == deckName):
                    await channel.send(str("A deck with that name already exist."))
                    return
            print(str(deck))
            profile.add_deck(deck)
        else:
            await channel.send(str("Please enter the command along with a deck name."))

    @commands.command(pass_context=True)
    async def renameDeck(self, ctx, *args):
        '''
        syntax: renameDeck [Name][New_Deck_Name]
        [Name]: The current name of the deck
        [New_Deck_Name]: The new name of the deck you would like to change to

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")
        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(len(args) == 2):
            deckName = args[0]
            new_deckName = args[1]
            for j in profile.get_decks():
                if(j.get_deck_name() == new_deckName):
                    await channel.send(str("A deck with that name already exist."))
                    return
            for i in profile.get_decks():
                if(i.get_deck_name() == deckName):
                    i.set_deck_name(new_deckName)
                    return
            await channel.send(str("The deck does not exist."))
        else:
            await channel.send(str("Please enter the command with the deck name along with a new deck name."))


    @commands.command(pass_context=True)
    async def deleteDeck(self, ctx, *args):
        '''
        syntax: deleteDeck [Name]
        [Name]: The current name of the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(len(args) == 1):
            deckName = args[0]
            for i in profile.get_decks():
                if(i.get_deck_name() == deckName):
                    profile.get_decks().remove(i)
                    break
            await channel.send(str("The deck does not exist."))
        else:
            await channel.send(str("Please enter the command with the deck name."))


    @commands.command(pass_context=True)
    async def changeDeckDescription(self, ctx, arg1, *, arg2):
        '''
        syntax: changeDescription [Name][New_Deck_Description]
        [Name]: The current name of the deck
        [New_Deck_Description]: The new description for the deck you would like to change

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg1
        new_deckDescription = arg2
        for i in profile.get_decks():
            if(i.get_deck_name() == deckName):
                i.set_deck_description(new_deckDescription)
                return
        await channel.send(str("The deck does not exist."))

    @commands.command(pass_context=True)
    async def addCardToDeck(self, ctx, *args): #check if card exist in inventory, args can have custom name, card id, and card name
        '''
        syntax: addCard [Name_of_deck][Card in inventory]
        [Name_of_deck]: The current name of the deck
        [Card in inventory]: The card you would like to add

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if (len(args) == 2):
            deckName = args[0]

            card = args[1]
            deck = None
            multimatched=card_multimatch(profile, card)

            if (multimatched != None): #check if card exist in player's inventory.
                cardvalue=multimatched[0]
                if(len(multimatched)>1):# Tiebreaker is needed here.
                    print("Place Tiebreaker Here.")#do tiebreaker.
                for i in profile.get_decks():
                    if(i.get_deck_name() == deckName):
                        deck = i
                        break
                if(deck.inDeck(cardvalue) == False):
                    deck.addToDeck(cardvalue) #to be updated when card_multimatch is finished, looks for the unique card_id if given either the same card name. *Use tiebreaker
                else:
                    await channel.send("Hang on, This card is already in your deck!")
            else:
                await channel.send("This card was not found in your inventory.")


    @commands.command(pass_context=True)
    async def removeCardFromDeck(self, ctx, *args):
        '''
        syntax: removeCard [Name_of_deck][Card in deck]
        [Name_of_deck]: The current name of the deck
        [Card in deck]: The card you would like to remove

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if (len(args) == 2):
            deckName = args[0]
            card = args[1]
            deck = None
            multimatched=card_multimatch(profile, card)
            if(multimatched != None):
                for i in profile.get_decks():
                    if(i.get_deck_name() == deckName):
                        deck = i
                        break
                cardvalue=multimatched[0]
                if(len(multimatched)>1):# Tiebreaker is needed here.
                    print("Place Tiebreaker Here.")#do tiebreaker.
                if(deck.inDeck(cardvalue) == True):
                    deck.removeFromDeck(cardvalue)
                else:
                    await channel.send("The card is not in your deck.")
            else:
                await channel.send("The card is not in your deck.")


    @commands.command(pass_context=True)
    async def multiAddToDeck(self, ctx, arg1, *, arg2):
        '''
        syntax: multi_add [Name_of_deck][Card in inventory 1][Card in inventory 2]...[Card in inventory n]
        [Name_of_deck]: The current name of the deck
        [Card in inventory]...[Card in inventory n]: The n cards you would like to add to the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg1
        cards = arg2.split()
        does_not_exist = []
        deck = None
        for j in cards:
            if(card_multimatch(profile, j) == None): #use card_multimatch to check if the cards exist in the inventory
                does_not_exist.append(j)
                cards.remove(j)
        for i in profile.get_decks():
            if(i.get_deck_name() == deckName):
                deck = i
                break
        deck.addListToDeck(cards)
        if(len(does_not_exist) != 0):
            await channel.send("The following cards does not exist in your inventory: {}".format(does_not_exist))


    @commands.command(pass_context=True)
    async def multiRemoveFromDeck(self, ctx, arg1, *, arg2):
        '''
        syntax: multi_remove [Name_of_deck][Card in inventory 1][Card in inventory 2]...[Card in inventory n]
        [Name_of_deck]: The current name of the deck
        [Card in inventory]...[Card in inventory n]: The n cards you would like to remove from the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg1
        cards = arg2.split()
        does_not_exist = []
        deck = None
        counter = 0
        for j in profile.get_decks():
            if(j.get_deck_name() == deckName):
                deck = j
                break
        for i in cards: #converts all cards regardless of identifier to card_id
            if(card_multimatch(profile, i) == None):
                cards.remove(i)
            else:
                cards[counter] = card_multimatch(profile, i)[0]["card_id"]
            counter = counter + 1
        deck.removeListFromDeck(cards)

    @commands.command(pass_context=True)
    async def viewAllDecks(self, ctx):
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        list = []
        for i in profile.get_decks():
            list.append(i.get_deck_name())
        message_content=""
        for j in list:
            message_content=message_content+str(j)+"\n"
        if(len(list)==0):
            await channel.send("NO DECKS IN USER PROFILE.")
        else:
            await channel.send(content=message_content)

    @commands.command(pass_context=True)
    async def viewDescription(self, ctx, arg):
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg
        for i in profile.get_decks():
            if(i.get_deck_name() == deckName):
                await channel.send(str(i.get_deck_description()))
                return

    @commands.command(pass_context=True)
    async def viewCardsInDeck(self, ctx, arg):
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg
        deck = None
        list = []
        for i in profile.get_decks():
            if(i.get_deck_name() == deckName):
                deck = i
                break
        for card in deck.get_deck_cards():
            card = CardRetrievalClass().getByID(int(card["card_id"], 16))
            list.append(card)
        message_content=""
        for j in list:
            message_content=message_content+str(j)+"\n"
        if(len(list)==0):
            await channel.send("NO CARDS IN DECK.")
        else:
            await channel.send(content=message_content)
