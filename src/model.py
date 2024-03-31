from typing import Union
from pydantic import BaseModel


class ProcessingLoad(BaseModel):
    cpu_core: int
    percentage: int
    mem_mb: int
    duration_sec: float

class TransmittingLoad(BaseModel):
    mb: int

class Next(BaseModel):
    target_url: str
    message: Union[str, None]

class Config(BaseModel):
    processingLoad: ProcessingLoad

class SetupPostLoadRequest(BaseModel):
    config: Config

class LoadPostRequest(BaseModel):
    processingLoad: Union[str, None] = None
    transmittingLoad: Union[str, None] = None
    next: Union[str, None] = None

Next.update_forward_refs()
