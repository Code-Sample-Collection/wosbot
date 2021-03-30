from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID
from pathlib import Path
from datetime import datetime
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
VEDIO_ROOT = Path(config['bili.rec']['root_path'])

app = FastAPI()

"""
https://rec.danmuji.org/docs/desktop/webhook/

{
    "EventRandomId": "bc2d0a41-2711-4f9b-8619-e54104fe90d8",
    "RoomId": 14846654,
    "Name": "小司无常",
    "Title": "【跨界冥神】打mua将！",
    "RelativePath": "14846654/record/20210107/150616.flv",
    "FileSize": 3749098123,
    "StartRecordTime": "2021-01-07T15:06:16.1387156+08:00",
    "EndRecordTime": "2021-01-07T16:06:16.1693244+08:00"
}
"""
class BiliRecFinish(BaseModel):
    EventRandomId: UUID
    RoomId: int
    Name: str
    Title: str
    RelativePath: Path
    FileSize: int
    StartRecordTime: datetime
    EndRecordTime: datetime


@app.post("/bili_rec/")
async def rec_finish(msg: BiliRecFinish):
    print(msg)
    full_path = VEDIO_ROOT.joinpath(msg.RelativePath) 
    rec_duration = msg.EndRecordTime - msg.StartRecordTime
    print(full_path)
    print(f'isfile {full_path.is_file()}')
    print(rec_duration)
    return {"message": "Runing ffmpeg..."}
