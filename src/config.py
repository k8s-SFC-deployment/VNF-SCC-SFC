from src.model import Config, ConfigV2, ProcessingLoad, ProcessingLoadV2, CPULoad, MEMLoad, DIOLoad

global config

config = Config(
    processingLoad=ProcessingLoad(
        cpu_core=1,
        percentage=50,
        mem_mb=256,
        duration_sec=3,
    )
)

import os

cpu_ops=int(float(os.getenv("CPU_OPS", 1000)))
cpu_worker=int(float(os.getenv("CPU_WORKER", 1)))
cpu_limit=int(float(os.getenv("CPU_LIMIT", 50)))

mem_ops=int(float(os.getenv("MEM_OPS", 1000)))
mem_worker=int(float(os.getenv("MEM_WORKER", 1)))
mem_bytes=int(float(os.getenv("MEM_BYTES", 10000)))

dio_ops=int(float(os.getenv("DIO_OPS", 1000)))
dio_worker=int(float(os.getenv("DIO_WORKER", 1)))
dio_bytes=int(float(os.getenv("DIO_BYTES", 10000000)))

global config_v2

config_v2 = ConfigV2(
    processingLoad=ProcessingLoadV2(
        cpu=CPULoad(ops=cpu_ops,worker=cpu_worker,limit=cpu_limit),
        mem=MEMLoad(ops=mem_ops,worker=mem_worker,bytes=mem_bytes),
        dio=DIOLoad(ops=dio_ops,worker=dio_worker,bytes=dio_bytes),
    )
)
