from base64 import b64encode
from io import BytesIO
from typing import List

import httpx
from PIL import Image
from nonebot.adapters.cqhttp import MessageSegment, Message


async def extract_images(message, http_like=False) -> List[MessageSegment]:
    """ 提取消息中的图片 """
    if type(message) == str:
        message = Message(message)

    res = []

    for msg in message:
        if msg.type == "image":
            res.append(msg)
        elif msg.type == "text" and http_like:
            res.extend([MessageSegment.text(_) for _ in msg.data["text"].split() if _[:4] == "http"])

    return res


async def get_size(io: BytesIO):
    return len(io.getvalue()) / 1024


async def compress_image(io: BytesIO, target_size=999, step=5, quality=95) -> tuple:
    """
    不改变图片尺寸压缩到指定大小.
    :param io: 输入文件字节流.
    :param target_size: 压缩目标，KB.
    :param step: 每次调整的压缩比率.
    :param quality: 初始压缩比率.
    :returns: 压缩后文件的字节内容,图片格式.
    """

    bytes_content = io.read()
    image = Image.open(io)

    if await get_size(io) <= target_size:
        return bytes_content, image.format.lower()

    while True:
        temp_io = BytesIO()
        image.save(temp_io, quality=quality, format=image.format)
        if quality - step < 0:
            raise RuntimeError("图片过大！")
        quality -= step
        if await get_size(temp_io) <= target_size:
            bytes_content = temp_io.getvalue()
            break

    return bytes_content, image.format.lower()


async def image_to_io(file: str) -> BytesIO:
    if file[:4] == "http":  # 网络图片
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(file)
            except httpx.UnsupportedProtocol:
                raise RuntimeError("地址错误!")
        # 读取响应内容到字节流
        io = BytesIO(r.content)
    else:
        with open(file, mode="rb") as fp:
            content = fp.read()
            # 读取文件内容到字节流
            io = BytesIO(content)
    return io


async def image_to_b64(file: str, target_size=1023) -> tuple:
    """
    图片转为BASE64字符串.
    :param file: 图片的本地地址或URL.
    :param target_size: 压缩目标,KB.
    :returns : 图片的base64字符串和类型.
    :raise RuntimeError: 图片格式错误,图片过大或图片地址错误引起的异常.
    """
    io = await image_to_io(file)
    # 压缩图片
    try:
        bytes_content, img_format = await compress_image(io, target_size=target_size)
    except Exception:
        raise RuntimeError(f"请确保目标地址为图片！")
    # 把原始字节码编码成 base64 字节码
    base64_bytes = b64encode(bytes_content)
    # 将 base64 字节码解码成 utf-8 格式的字符串
    base64_string = base64_bytes.decode("UTF-8")

    return base64_string, img_format
