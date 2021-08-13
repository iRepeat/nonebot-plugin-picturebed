from abc import abstractmethod, ABCMeta


class PictureBed(metaclass=ABCMeta):
    """图床抽象类"""

    @staticmethod
    def upload_fail(error_info) -> dict:
        return {
            "code": "1",
            "msg": "上传失败",
            "data": {
                "error_info": error_info,
                "url": ""
            }
        }

    @staticmethod
    def upload_success(url) -> dict:
        return {
            "code": "0",
            "msg": "上传成功",
            "data": {
                "error_info": "",
                "url": url
            }
        }

    @abstractmethod
    def __init__(self, config: dict):
        """
        在这里初始化图床的配置信息.
        :param config: config.py中对应图床的配置信息
        """
        pass

    @abstractmethod
    async def upload(self, url: str) -> dict:
        """
        上传图片.
        :param url: 图片地址
        :returns: 上传结果信息,合法的返回值请参照upload_fail(error_info)或upload_success(url),可直接使用
        """
        pass
