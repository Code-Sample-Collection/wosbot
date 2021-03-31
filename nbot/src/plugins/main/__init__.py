# import nonebot
from nonebot import get_driver
from nonebot.adapters.mirai import Bot, MessageEvent
from nonebot.plugin import on_keyword, on_command
from nonebot.rule import to_me
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


message_test = on_keyword({'reply'}, rule=to_me())
@message_test.handle()
async def _message(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, text, at_sender=True)

command_test = on_command('miecho')
@command_test.handle()
async def _echo(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, text, at_sender=True)
