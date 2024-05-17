import json

import os
import requests
from fastapi import FastAPI, File, UploadFile, Depends, BackgroundTasks

from src.config import config, config_v2
from src.utils.stress import stress, stress_v2
from src.utils.parsing import load_json_one_depth_v2
from src.model import LoadPostRequest, Next, ProcessingLoad, TransmittingLoad, ProcessingLoadV2

app = FastAPI(title="VNF-SCC-SFC", root_path=os.getenv("ROOT_PATH", default=None))


def request_next(target_url, files, data):
    requests.post(target_url, headers={'accept': 'application/json'}, files=files, params=data)

# Example
# processingLoad={
#     "cpu_core": 1, 
#     "percentage": 70, 
#     "mem_mb": 512, 
#     "duration_sec": 5
# }
# transmittingLoad={"mb": 10}
# next={
#     "target_url":"http://localhost:7000/load",
#     "message": {
#         "processingLoad": {
#             "cpu_core": 1, 
#             "percentage": 70, 
#             "mem_mb": 512, 
#             "duration_sec": 10
#         }, 
#         "transmittingLoad": null, 
#         "next": {
#             "target_url": "http://localhost:7000/load", "message": null
#         }
#     }
# }

@app.post("/load")
async def load(file: UploadFile = File(...), load_req: LoadPostRequest = Depends(), bg_tasks: BackgroundTasks = None):
    try:
        json_dict = load_json_one_depth_v2(load_req.next, ["message"])
        next = Next(**json_dict)
    except Exception as e:
        print(e)
        next = None
    try:
        processingLoad = ProcessingLoad(**json.loads(load_req.processingLoad))
    except Exception as e:
        print(e)
        processingLoad = None
    try:
        transmittingLoad = TransmittingLoad(**json.loads(load_req.transmittingLoad))
    except Exception as e:
        transmittingLoad = None
    
    print(f"processingLoad: {processingLoad}\ntransmittingLoad: {transmittingLoad}\nnext: {next}")
    
    if processingLoad == None:
        processingLoad = config.processingLoad
    

    stress(processingLoad)
    
    if next is None:
        # Nothing
        return None
    elif transmittingLoad is None:
        next_files = { "file": (file.filename, file.file.read(), file.content_type) }
    else:
        next_files = { "file": ("file", bytes(transmittingLoad.mb * 1024 * 1024), "binary/octet-stream") }
    
    target_url = next.target_url
    if next.message is not None:
        data = load_json_one_depth_v2(next.message, ["processingLoad", "transmittingLoad", "next"])
    else:
        data = None
    bg_tasks.add_task(request_next, target_url, next_files, data)
    
    return "Ok"

# Example
# processingLoad={"cpu":{"ops":5000, "worker": 1, "limit": 50}, "mem": {"ops":5000, "worker": 1, "bytes": 10000}, "dio": {"ops":5000, "worker": 1, "bytes": 10000000}}
# transmittingLoad={"mb": 10}
# next={"target_url": "http://localhost:7000/loadv2","message": {"processingLoad": {"cpu": {"ops": 5000,"worker": 1,"limit": 50},"mem": {"ops": 5000,"worker": 1,"bytes": 10000},"dio": {"ops": 5000,"worker": 1,"bytes": 10000000}},"transmittingLoad": null,"next": {"target_url": "http://localhost:7000/loadv2","message": null}}}
@app.post("/loadv2")
async def loadv2(file: UploadFile = File(...), load_req: LoadPostRequest = Depends(), bg_tasks: BackgroundTasks = None):
    try:
        json_dict = load_json_one_depth_v2(load_req.next, ["message"])
        next = Next(**json_dict)
    except Exception as e:
        next = None
    try:
        processingLoad = ProcessingLoadV2(**json.loads(load_req.processingLoad))
    except Exception as e:
        processingLoad = None
    try:
        transmittingLoad = TransmittingLoad(**json.loads(load_req.transmittingLoad))
    except Exception as e:
        transmittingLoad = None
    
    print(f"processingLoad: {processingLoad}\ntransmittingLoad: {transmittingLoad}\nnext: {next}")
    
    if processingLoad == None:
        processingLoad = config_v2.processingLoad
    
    await stress_v2(processingLoad)
    
    if next is None:
        # Nothing
        return None
    elif transmittingLoad is None:
        next_files = { "file": (file.filename, file.file.read(), file.content_type) }
    else:
        next_files = { "file": ("file", bytes(transmittingLoad.mb * 1024 * 1024), "binary/octet-stream") }
    
    target_url = next.target_url
    if next.message is not None:
        data = load_json_one_depth_v2(next.message, ["processingLoad", "transmittingLoad", "next"])
    else:
        data = None
    bg_tasks.add_task(request_next, target_url, next_files, data)
    
    return "Ok"

@app.get("/config")
def get_config():
    return { "v1": config, "v2": config_v2 }

@app.get("/")
def root():
    return "VNF SCC SFC"