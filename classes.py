from enum import IntEnum

import discord
from discord.embeds import Embed
from discord.ext.commands.context import Context
from discord.ui import Button, View
from discord import Interaction

__all__ = [
    "ChoiceButton", "ChoiceView",
    "Colours", "Messages"
]


class ChoiceButton(Button):
    def __init__(self, label: str | None, correct: bool = False) -> None:
        self.correct = correct
        super().__init__(label=label)

    async def callback(self, interaction: Interaction) -> None:
        if self.view.id != interaction.user.id: return

        self.style = discord.ButtonStyle.green if self.correct \
            else discord.ButtonStyle.red

        self.view.success = self.correct

        for child in self.view.children:
            child.disabled = True
            if child.correct and child != self:
                child.style = discord.ButtonStyle.blurple

        self.view.stop()
        await interaction.response.edit_message(view=self.view)


class ChoiceView(View):
    def __init__(
        self,
        items: list[str],
        correct_item: str,
        user_id: int
    ) -> None:

        super().__init__(timeout=5)
        self.success = False
        self.id = user_id
        for item in items:
            self.add_item(ChoiceButton(item, item == correct_item))

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
            if child.correct:
                child.style = discord.ButtonStyle.blurple

        self.stop()
        await self.message.edit(view=self)


class Colours(IntEnum):
    RED = 0xFF4A08
    ORANGE = 0xFF6B21
    YELLOW = 0xFFF826
    GREEN = 0x95E600
    BLUE = 0x0F63FF
    PURPLE = 0xA20DFF


def create_message_sender(colour: int):
    @staticmethod
    async def message_sender(
        ctx: Context,
        title: str | None = None,
        description: str | None = None
    ) -> None:

        embed = Embed(
            title=title,
            description=description,
            colour=colour
        )
        await ctx.send(embed=embed)
    return message_sender


class Messages:
    warning = create_message_sender(Colours.RED)
    mistake = create_message_sender(Colours.ORANGE)
    success = create_message_sender(Colours.GREEN)
    default = create_message_sender(Colours.BLUE)
