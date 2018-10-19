import shlex
import aiohttp
import discord
import discord.ext
import logging
import argparse
import commands
import datetime
from cmd_manager import dispatcher
from config import config
from cmd_manager.bot_args import parser, HelpException, UnkownCommandException
from utils.handle_messages import send_message, delete_message

client = discord.Client()
commands.load_commands()

@client.event
async def on_ready():
    logging.info(f'Logged in as\nUsername: {client.user.name}\nID: {client.user.id}\nAPI Version: {discord.__version__}')
    gameplayed = discord.Game(name=config.MAIN.get("gameplayed", "Awaiting Spoiler"))
    await client.change_presence(activity=gameplayed)


@client.event
async def on_message(message):
    await handle_commands(message)


@client.event
async def on_message_edit(_, message):
    await handle_commands(message)


async def handle_commands(message):
    if isinstance(message.channel, discord.abc.GuildChannel):
        server_name = message.guild.name
        channel_name = message.channel.name
    else:
        server_name = "Private Message"
        channel_name = None

    if not message.content.startswith(">>"):
        return

    if len(message.content) == 2:
        return

    today = datetime.datetime.today().strftime("%a %d %b %H:%M:%S")
    logging.info(f"Date: {today} User: {message.author} Server: {server_name} Channel: {channel_name} "
                 f"Command: {message.content[:50]}")

    arg_string = message.clean_content[2:]
    try:
        arg_string = shlex.split(arg_string)
    except ValueError as err:
        return await send_message(message.author, f"```{str(err)}```")

    try:
        args = parser.parse_args(arg_string)
    except HelpException as err:
        return await send_message(message.author, f"```{str(err)}```")
    except (UnkownCommandException, argparse.ArgumentError) as err:
        if arg_string[0] == "spoiler":
            await delete_message(message)
        if arg_string[0] in dispatcher.commands:
            return await send_message(message.author, f"```{str(err)}```")
        return

    return await dispatcher.handle(args.command, client, message, args)


def main():
    while True:
        try:
            client.run(config.MAIN.login_token)
        except aiohttp.client_exceptions.ClientConnectorError:
            continue
        except KeyboardInterrupt:
            return client.close()


if __name__ == "__main__":
    main()
