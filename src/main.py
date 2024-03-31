import json

import requests
from fastapi import FastAPI, File, UploadFile, Depends, BackgroundTasks

from src.config import config
from src.utils.stress import stress
from src.utils.parsing import load_json_one_depth_v2
from src.model import SetupPostLoadRequest, LoadPostRequest, Next, ProcessingLoad, TransmittingLoad


app = FastAPI()


def request_next(target_url, files, data):
    requests.post(target_url, headers={'accept': 'application/json'}, files=files, params=data)

# Example
# processingLoad: {
#     "cpu_core": 1, 
#     "percentage": 70, 
#     "mem_mb": 512, 
#     "duration_sec": 5
# }
# transmittingLoad: {"mb": 10}
# next: {
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
#             { "target_url": "http://localhost:7000/load", "message": null }
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


@app.get("/config")
def get_config():
    return config

@app.post("/config")
def post_config(setup_load: SetupPostLoadRequest):
    global config
    config = setup_load.config
    return config
