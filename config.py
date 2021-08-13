from pydantic import BaseSettings


class Config(BaseSettings):
    use = "gitee"  # 默认图床
    gitee = {
        "message": "",  # 提交时的信息
        "owner": "",
        "repo": "",
        "path": "",
        "access_token": "",
    }
    smms = {
        "Authorization": ""
    }

    class Config:
        extra = "ignore"
