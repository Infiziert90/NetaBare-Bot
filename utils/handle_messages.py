import discord
import logging


async def send_message(destination, content, file=None):
    try:
        await destination.send(content=content, file=file)
    except discord.Forbidden:
        logging.debug("Not enough permissions")
    except discord.HTTPException:
        logging.debug("Exception while sending message")


async def delete_message(message):
    try:
        await message.delete()
    except discord.Forbidden:
        message.channel.send(content="Not enough permissions: Manage Messages")
        return logging.exception("Not enough permissions")
    except discord.errors.NotFound:
        pass
