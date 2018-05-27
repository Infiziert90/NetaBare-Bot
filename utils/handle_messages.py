import discord
import logging


async def send_message(destination, content, file=None):
    try:
        await destination.send(content=content, file=file)
    except (discord.Forbidden, discord.HTTPException) as err:
        logging.info(f"Exception while sending a message: {err}")


async def delete_message(message):
    try:
        await message.delete()
    except (discord.Forbidden, discord.NotFound) as err:
        logging.info(f"Exception while deleting a message: {err}")

