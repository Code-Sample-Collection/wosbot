from pydantic import BaseSettings


class Config(BaseSettings):
    """BiliRec 配置类

    WebHook 无需配置
    """
    class Config:
        extra = "ignore"
