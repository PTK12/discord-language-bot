from enum import Enum

import discord
from discord.embeds import Embed
from discord.ext.commands.context import Context
from discord.ui import Button, View

__all__ = [
    "ChoiceButton", "ChoiceView",
    "Colours", "Messages"
]


class ChoiceButton(Button):
    def __init__(self, label, correct=False):
        self.correct = correct
        super().__init__(label=label)

    async def callback(self, interaction):
        if self.view.id:
            if self.view.id != interaction.user.id:
                return 1
        self.style = discord.ButtonStyle.red
        for child in self.view.children:
            child.disabled = True
            if child.correct:
                if self == child:
                    child.style = discord.ButtonStyle.green
                    self.view.success = True
                else:
                    child.style = discord.ButtonStyle.blurple
            self.view.stop()
        await interaction.response.edit_message(view=self.view)


class ChoiceView(View):
    def __init__(self, items, correct_label, user_id=None):
        super().__init__(timeout=5)
        self.success = False
        self.id = user_id
        for i in items:
            self.add_item(ChoiceButton(i, i == correct_label))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            if child.correct:
                child.style = discord.ButtonStyle.blurple
            self.stop()
        await self.message.edit(view=self)


class Colours(Enum):
    R = 0xFF4A08
    O = 0xFF6B21
    Y = 0xFFF826
    G = 0x95E600
    B = 0x0F63FF
    P = 0xA20DFF


class Messages:
    @staticmethod
    async def warning(ctx: Context, title=None, description=None):
        embed = Embed(
            title=title,
            description=description,
            color=Colours.R.value
        )
        await ctx.send(embed=embed)

    @staticmethod
    async def mistake(ctx: Context, title=None, description=None):
        embed = Embed(
            title=title,
            description=description,
            color=Colours.O.value
        )
        await ctx.send(embed=embed)

    @staticmethod
    async def success(ctx: Context, title=None, description=None):
        embed = Embed(
            title=title,
            description=description,
            color=Colours.G.value
        )
        await ctx.send(embed=embed)

    @staticmethod
    async def default(ctx: Context, title=None, description=None):
        embed = Embed(
            title=title,
            description=description,
            color=Colours.B.value
        )
        await ctx.send(embed=embed)
