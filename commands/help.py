from cmd_manager.bot_args import parser
from utils.handle_messages import send_message
from cmd_manager.decorators import register_command


@register_command('help', description='Post the help message.')
async def help_str(client, message, args):
    await send_message(message.author, parser.format_help())
    await send_message(message.author, "You can also use >>COMMAND -h/--help")
