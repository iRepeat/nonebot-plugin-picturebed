import json

import httpx

from utils.file_utils import generate_file_name
from utils.image_utils import image_to_b64
from .PictureBed import PictureBed


class PBGitee(PictureBed):

    def __init__(self, config: dict):
        super().__init__(config)
        self.message = config.get("message", None)
        self.owner = config.get("owner", None)
        self.repo = config.get("repo", None)
        self.path = config.get("path", None)
        self.access_token = config.get("access_token", None)

    @staticmethod
    async def submit_msg(base64_string, message, owner, repo, path, file_name, access_token):
        """ 向gitee提交信息. """

        url = "https://gitee.com/api/v5/repos/%s/%s/contents/%s/%s" % (owner, repo, path, file_name)
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        data = '{' \
               '"access_token":"%s",' \
               '"content":"%s","message":"%s"' \
               '}' % (access_token, base64_string, message)
        async with httpx.AsyncClient() as client:
            r = await client.post(url, headers=headers, data=data)

        r.encoding = "utf-8"
        dict_result = json.loads(r.text)
        return dict_result

    async def upload(self, url) -> dict:

        try:
            base64_string, extend = await image_to_b64(url, target_size=1023)
        except RuntimeError as e:
            # 目标地址不是图片或者过大
            return PictureBed.upload_fail("上传图片【%s】时出错了！%s" % (url, e.args[0]))

        file_name = await generate_file_name(extend)
        # 开始提交至gitee
        result = await self.submit_msg(base64_string, self.message, self.owner,
                                       self.repo, self.path, file_name, self.access_token)

        # 若键"commit"存在于提交结果,则上传成功
        if "commit" in result.keys():
            return PictureBed.upload_success(
                "https://gitee.com/%s/%s/raw/master/%s/%s" % (self.owner, self.repo, self.path, file_name))

        # 上传失败
        return PictureBed.upload_fail("上传图片【%s】时出错了！%s" % (url, result))
