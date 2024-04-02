from typing import Union
from pydantic import BaseModel


class ProcessingLoad(BaseModel):
    cpu_core: int                   # core number to apply stress
    percentage: int                 # how much stress each cpu core
    mem_mb: int                     # how much stress memory
    duration_sec: float             # duration seconds

class TransmittingLoad(BaseModel):
    mb: int                         # transmitting bytes size (MB)

class Next(BaseModel):
    target_url: str                 # next target VNF url
    message: Union[str, None]       # message to send next VNF. It is the serialized LoadPostRequest
                                    # if not exist, mean next is the final VNF.

class Config(BaseModel):
    processingLoad: ProcessingLoad  # default processingLoad, when the load don't have processingLoad

class SetupPostLoadRequest(BaseModel):
    config: Config

class LoadPostRequest(BaseModel):
    processingLoad: Union[str, None] = None     # processingLoad, if not eixist, then use default configured processingLoad
    transmittingLoad: Union[str, None] = None   # transmittingLoad, if not exist, then just forward receieved file.
    next: Union[str, None] = None               # next target VNF

Next.update_forward_refs()
