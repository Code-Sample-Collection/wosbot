# NoneBot.adapters.bilirec 模块

## BiliRec WebHook 协议适配

协议详情参见: [Webhook - 文档 - B站录播姬](https://rec.danmuji.org/docs/desktop/webhook/)


`bilirec.bot` 模块
------------------

## *class* `Bot`

基类：`nonebot.adapters._base.Bot`

BiliRec WebHook 协议适配。继承属性参考 BaseBot 。

### *property* `type`
+ 返回: "bilirec"

### *async classmethod* `check_permission(driver, connection_type, headers, body)`
+ **说明**: webhook 事件合法性检查

### `bilirec.config` 模块

无需传参

