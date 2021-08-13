from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from utils.image_utils import extract_images
from .PBGitee import PBGitee
from .PBSMMS import PBSMMS
from .PictureBed import PictureBed
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

# 在这里注册图床类
picture_beds = {
    "gitee": PBGitee(config.gitee),
    "smms": PBSMMS(config.smms)
}
picture_bed: PictureBed = picture_beds[config.use]

upload = on_command('upload', permission=SUPERUSER)
switch = on_command('图床', permission=SUPERUSER)


@upload.handle()
async def _(bot: Bot, event: Event, state: T_State):
    message = event.get_message()
    images = await extract_images(message, http_like=True)

    if len(images) != 0:
        state["message"] = message


@upload.got("message", "无图你说个锤子?")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    message = state["message"]
    images = await extract_images(message, http_like=True)

    if len(images) == 0:
        await upload.finish("告辞" + MessageSegment.face(39) + MessageSegment.reply(event.message_id))

    await bot.send(message=f"检测到疑似{len(images)}张图片，开始上传...", event=event)

    urls= []
    for image in images:
        url = image.data["url"] if image.get("type", None) == "image" else image.data["text"]
        # 上传图片到图床
        res = await picture_bed.upload(url)

        if res["code"] != '0':
            await bot.send(event, res["data"]["error_info"])
        else:
            urls.append(res["data"]["url"])

    await bot.send(event, "成功上传%s张图片!" % len(urls))
    for url in urls:
        # 发送分享链接
        await bot.send(event, MessageSegment.share(url, title="点击查看图片", image=url))


@switch.handle()
async def _(bot: Bot, event: MessageEvent):
    global picture_bed
    pb = str(event.get_message()).strip()
    if not pb:
        return

    if pb not in config.dict().keys():
        await switch.finish(f"图床不存在: {pb}")

    picture_bed = picture_beds[pb]
    await switch.finish(f"图床已切换: {pb}")
