from nonebot.log import logger
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.exception import RequestDenied
import json


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

    @classmethod
    @overrides(BaseBot)
    async def check_permission(cls, driver: "Driver", connection_type: str,
                               headers: dict, body: Optional[bytes]) -> str:
        """连接鉴权，消息检查合法性。

        Parameters
        ----------
        + `driver :: Driver`: Driver 对象
        + `connection_type :: str`: 连接类型 `[http | websocket]`
        + `headers :: dict`: 请求头
        + `body :: Optional[bytes]`: 请求数据

        Returns
        -------
        + `str`: 连接合法，返回连接唯一标识符（消息的 UUID）

        Raises
        ------
        + `RequestDenied`: 连接不合法，抛出异常
        """
        logger.debug(f'[{connection_type}] {headers}; {body}')
        # 'user-agent: BililiveRecorder/1.2.2.0-815189c6'
        content_type = headers.get("content-type")
        ua = headers.get("user-agent")

        # 检查连接方式
        # NOTE: 405 Method Not Allowed
        if connection_type not in ["http"]:
            raise RequestDenied(
                405, "Unsupported connection type: '{connection_type}', available type: `http`")

        # 检查内容格式
        # NOTE: 400 Bad Request
        if content_type not in ["application/json"]:
            raise RequestDenied(
                400, "Unsupported content type: '{content_type}', available type: `application/json`")

        # 检查 UA
        if 'BililiveRecorder' not in ua:
            raise RequestDenied(
                400, 
                "Unsupported user-agent type: '{ua}', available type: `BililiveRecorder/-version-githash`"
            )

        # 检查 body 长度
        if len(body) == 0:
            raise RequestDenied(400, "Empty body")

        # 返回唯一的消息 UUID
        return json.loads(body.decode())["EventRandomId"]
  
