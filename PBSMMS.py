import json
from io import BytesIO

import httpx

from utils.image_utils import image_to_io, get_size
from .PictureBed import PictureBed


class PBSMMS(PictureBed):

    def __init__(self, config: dict):
        super().__init__(config)
        self.authorization = config.get("Authorization", None)

    @staticmethod
    async def post(authorization, io: BytesIO):
        """ 向SM.MS上传图片. """

        url = "https://sm.ms/api/v2/upload"
        headers = {
            'Authorization': authorization,
        }
        files = {
            'smfile': io
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(url, headers=headers, files=files)

        r.encoding = "utf-8"
        dict_result = json.loads(r.text)
        return dict_result

    async def upload(self, url) -> dict:

        try:
            io = await image_to_io(url)
            if (await get_size(io)) >= 5 * 1024 - 1:
                raise RuntimeError("图片过大!")
            result = await self.post(self.authorization, io)
        except RuntimeError as e:
            # 目标地址不是图片或者过大
            return PictureBed.upload_fail("上传图片【%s】时出错了！%s" % (url, e.args[0]))
        except httpx.ReadTimeout:
            # 免费账户可能发生请求超时
            return PictureBed.upload_fail("上传图片【%s】时出错了！请求超时!" % url)

        if result.get("success", False):
            return PictureBed.upload_success(result["data"]["url"])

        # 上传失败
        return PictureBed.upload_fail("上传图片【%s】时出错了！%s" % (url, result.get("message", "")))
