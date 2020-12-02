import aiohttp
import asyncio


class Effect:
    """Without This, there's no strategy!"""
    def __init__(self, time, context, function, function_arg, disable_condition, disable_arg, level=0, description=""):
        """
        time is when the Effect is triggered.  Can be "before", "during", or "after"
        context is where the skill will trigger.
        function is a passed in method of what it will do.
        function arg is a arg for it.
        disable_condition is how it will disable.  Right now the only condition is "times_used"
        disable_arg is a modifier for disable_condition
        """
        self.times_used=0
        self.time=time
        self.context=context
        self.function=function
        self.arg=function_arg
        #list = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', result)
        self.disable_condition=disable_condition
        self.disable_arg=disable_arg
        self.level=level
        self.disableprompt=" wore off"
        self.description=description
        self.turns=0
    def check_trigger(self, time, context):
        print("Checked Trigger.")
        if time==self.time and context==self.context:
            return True
        return False
    async def execute(self, dictionary, game_ref):
        diction=await self.function(dictionary, game_ref, self.arg)
        self.times_used = self.times_used + 1
        return diction
    def add_turn(self):
        self.turns=self.turns + 1
    def disable_check(self):
        if self.disable_condition == 'times_used':
            if self.times_used >= int(self.disable_arg):
                return True
        elif self.disable_condition == 'turns_passed':
            print(self.disable_arg, self.turns)
            if self.turns >= int(self.disable_arg):
                return True
        else:
            return False
    def get_disableprompt(self):
        return self.disableprompt
