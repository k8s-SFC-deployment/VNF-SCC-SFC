from src.model import Config, ProcessingLoad

global config

config = Config(
    processingLoad=ProcessingLoad(
        cpu_core=1,
        percentage=50,
        mem_mb=256,
        duration_sec=3,
    )
)