from asyncio import sleep

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import BadArgument
from discord import Embed

from core import *
from database import *
from classes import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", help_command=None, intents=intents)


@bot.event
async def on_ready() -> None:
    print("===========================")
    print("Username:", bot.user)
    print("ID:", bot.user.id)
    print("===========================")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name='>help'
        )
    )

HELP_DESC = """
**help** - shows the help page
**ping** - shows the bot latency (ms)

**topic** - shows all the available topics
**q** [list] - do 1 multiple choice from [list]
**quiz** [list] [20] - do [20] multiple choice questions from [list]
**spell** [list] [1] - do [1] spelling sessions from [list]

Use **help** [command] for more information about a command.
"""


@bot.command()
async def help(ctx: Context, command: str | None = None) -> None:
    '''I think you know what this does'''
    if command is None:
        await Messages.default(ctx, "Help", HELP_DESC)
    else:
        c = bot.get_command(command)
        msg = c.help if c else "Command not found."
        await Messages.default(ctx, command, msg)


@bot.command()
async def ping(ctx: Context) -> None:
    '''Shows the bot latency (ms).'''
    await ctx.send(f"pong {round(bot.latency * 1000)}ms")


@bot.command()
async def test(ctx: Context) -> None:
    '''Sends a message in different colours.'''
    for colour in Colours:
        await ctx.send(embed=Embed(title="Hi", color=colour))
        await sleep(0.2)


@bot.command()
async def topic(ctx: Context) -> None:
    '''Shows all the available topics.'''
    desc = []
    for i, j in enumerate(vocabtitle):
        desc.append(f"**{i:>3}**\t{j}")
    await Messages.default(ctx, "Topics", "\n".join(desc))


async def error_list(ctx: Context) -> None:
    desc = ["Try using one of these instead:"]
    for i, j in enumerate(vocabtitle):
        desc.append(f"**{i:>3}**\t{j}")
    await Messages.warning(ctx, "Invalid topic!", "\n".join(desc))


async def check_range(ctx: Context, inp: str, start: int, stop: int) -> int:
    try:
        inp = int(inp)
        if inp not in range(start, stop + 1):
            raise BadArgument
        return inp
    except (BadArgument, ValueError) as e:
        await Messages.warning(
            ctx,
            "Invalid number!",
            f"Please enter a number between {start}-{stop}."
        )
        raise e


@bot.command()
async def spell(
    ctx: Context,
    topic: str | None = None,
    rounds: str = "1"
) -> None:
    '''Asks you to spell things.'''

    try:  # Check if number of rounds is correct
        rounds = await check_range(ctx, rounds, 1, 20)
    except (BadArgument, ValueError):
        return 2

    try:
        mcq(n=rounds, name=topic)
    except (IndexError, KeyError):
        await error_list(ctx)
        return 2

    is_answer = lambda m: m.author == ctx.message.author

    for _ in range(rounds):
        pub, priv = mcq(n=rounds, name=topic)
        await Messages.default(ctx, pub[0])

        try:
            answer = await bot.wait_for("message", check=is_answer, timeout=10)
            answer = answer.content
        except TimeoutError:
            await Messages.mistake(
                ctx,
                "You ran out of time!",
                f"The answer was {priv}"
            )
            return 2

        if not is_correct(answer, priv):
            await Messages.mistake(
                ctx,
                "Wrong",
                f"The correct answer is {priv}"
            )
            return 2

        await Messages.success(ctx, "Correct!")


@bot.command()
async def q(ctx: Context, topic: str | None = None) -> None:
    '''Sends a multiple choice question.'''
    try:  # Check if title is correct
        pub, priv = mcq(name=topic)
    except (IndexError, KeyError):
        await error_list(ctx)
        return 2

    embed = Embed(title=pub[0], color=Colours.BLUE)
    view = ChoiceView(pub[1], priv, ctx.message.author.id)
    view.message = await ctx.send(embed=embed, view=view)
    return await view.wait()


@bot.command()
async def quiz(
    ctx: Context,
    topic: str | None = None,
    rounds: str = "20"
) -> None:
    '''Sends multiple multiple choice questions.'''

    try:  # Check if number of rounds is correct
        rounds = await check_range(ctx, rounds, 3, 50)
    except (BadArgument, ValueError):
        return 2

    try:  # Check if title is correct
        mcq(name=topic)
    except (IndexError, KeyError):
        await error_list(ctx)
        return 2

    losses = 0

    for counter in range(1, rounds + 1):
        pub, priv = mcq(name=topic)

        embed = Embed(
            title=f"{pub[0]} [{counter}/{rounds}]",
            color=Colours.BLUE
        )

        view = ChoiceView(pub[1], priv, ctx.message.author.id)
        view.message = await ctx.send(embed=embed, view=view)
        await view.wait()

        losses += not view.success
        if losses != 3:
            continue

        await Messages.warning(
            ctx,
            "You lost 3 times.",
            f"You managed {counter - losses} out of {rounds}."
        )
        return 1

    await Messages.success(
        ctx,
        "Congratulations!",
        f"You got [{rounds - losses}/{rounds}]",
    )


def main() -> None:
    from dotenv import dotenv_values

    token = dotenv_values().get("DISCORD_TOKEN")

    if token is None:
        print("Please supply a discord token into the .env file.")
        exit(1)

    bot.run(token, reconnect=True)


main()
