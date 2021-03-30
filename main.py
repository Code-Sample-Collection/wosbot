from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from uuid import UUID
from pathlib import Path
from datetime import datetime
import configparser
import ffmpeg


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


def rec_flv2mp4(flv_path: Path):
    print(f'Handling {flv_path}')
    print(f'isfile {flv_path.is_file()}')
    out_fname = flv_path.stem + '.mp4'
    out_mp4 = flv_path.parent.joinpath(out_fname)
    (
        ffmpeg
        .input(flv_path)
        .output(filename=out_mp4, codec='copy')
        .overwrite_output()
        .run()
    )
    print(f'flv2mp4 finished: {out_fname}')


@app.post("/bili_rec/")
async def rec_finish(msg: BiliRecFinish, background_tasks: BackgroundTasks):
    print(msg)
    full_path = VEDIO_ROOT.joinpath(msg.RelativePath) 
    rec_duration = msg.EndRecordTime - msg.StartRecordTime
    print(rec_duration)
    background_tasks.add_task(rec_flv2mp4, full_path)
    return {"message": "Runing ffmpeg..."}
