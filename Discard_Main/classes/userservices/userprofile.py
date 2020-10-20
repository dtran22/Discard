import discord
import operator
import csv
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from pathlib import Path
import json
directory="saveData"
class SingleUserProfile:
    class __SingleUserProfile: #Singleton Design.  Based on https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, arg="P."):
            self.val = arg
            self.buffer={} #A buffer of all.
        def setAll(self):
            #Update for all new cardclusters.
            print("tbd")
        def getIDinternal(self, id):
            if(self.checkforidinbuffer(id)):
                return self.buffer[str(id)]
            else: #ID is not in buffer.
                file=self.get_file_from_directory(id)
                if(file!= None):
                    f= file.open(mode='r');
                    string=f.read();
                    self.buffer[str(id)]=UserProfile(user_id==id, dictonary_to_use=json.loads(string))
                    f.close()
                    print("Should initalize new user profile with the dictonary_to_use param set to the translated contents of file, add that into buffer under user id.")
                    #Load contents of file into new UserProfile, add that into buffer.
                else:
                    self.buffer[str(id)]=UserProfile(user_id==id)
                    print("Should initalize new default user profile, add that into buffer under user id.")
                    #Initalize new file.
        def save_buffer_entry(self, id): #Saves the UserProfile object at id to a file.
            if(self.checkforidinbuffer(id)):
                filename="userprofile_id_"+str(id)+".json" #filename from json.
                file= Path(directory + "/"+ filename)
                f=file.open(mode="w+")

                string_to_write=json.dumps(self.buffer[str(id)].to_dictionary(), sort_keys=True, indent=4)
                f.write(string_to_write(string_to_write))
                f.close()
        def save_all_internal(self): #save everything in buffer.
            for i, v in self.buffer.items():
                self.save_buffer_entry(i)

        def checkforidinbuffer(self, id):
            key_to_lookup = str(id)
            if key_to_lookup in self.internal_Dictionary:
              return True
            else:
              return False
        def get_file_from_directory(self, id):
            filename="userprofile_id_"+str(id)+".json" #filename from json.
            file= Path(directory + "/"+ filename)
            if file.exists():#check if this file exists.
                return file
            else:
                return None
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):  #Internally, it keeps a single instance of the __SingleDictionary class in memory.
        if not SingleUserProfile.instance:
            SingleUserProfile.instance = SingleUserProfile.__SingleUserProfile(arg)
        else:
            SingleUserProfile.instance.val = arg
    def getByID(self, id):
        #Initial chekc
        return SingleUserProfile.instance.getIDinternal(id)
    def saveAll(self, id):

    def __getattr__(self, name):
        return getattr(self.instance, name)


class UserProfile:
    def __init__(self, user_id, dictonary_to_use=None):
        self.user_id=user_id
        self.cards=[] #List of ids. every entry in list is dictionary of format {"card_id":card_id, "custom":id_of_custom_applied}
        self.customs=[] #list of customs made by the user.
        #self.cards_customs={} #dictionary.  Key is card Id and
        self.exp=0
        self.level=0
        self.cardcount=0
        self.coins=0
        self.stars=0

        self.decks=[] #Max 99.

        if(dictonary_to_use!=None):
            for i, v in dictonary_to_use.items():
                if hasattr(self, i):
                    setattr(self, i, v)

    def to_dictionary(self):
        return vars(self)

    def get_cards(self):
        return self.cards

    def get_customs(self):
        return self.customs

    def add_card(self, card_id):
        self.cards.append({"card_id":card_id, "custom":None})

    def get_exp(self):
        return self.exp
    def set_exp(self, value):
        self.exp=value
