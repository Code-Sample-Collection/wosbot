from nonebot.log import logger
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.exception import RequestDenied


class Bot(BaseBot):
    """
    BiliRec WebHook 协议适配。继承属性参考 BaseBot
    """

    def __init__(self, connection_type: str, self_id: str, **kwargs):
        """类初始化
        Parameters
        ----------
        + `connection_type :: str`: http 或者 websocket
        + `self_id :: str`: 机器人 ID
        """
        super().__init__(connection_type, self_id, **kwargs)

    @property
    def type(self) -> str:
        """
        Returns
        -------
        + `"bilirec" :: str`: 类类型
        """
        return "bilirec"

    @classmethod
    def register(cls, driver: "Driver", config: "Config"):
        """初始化相关配置。
        在 `driver.register_adapter` 时被调用

        Parameters
        ----------
        + `driver :: Driver`: 
        + `config :: Config`: 
        """
        super().register(driver, config)

