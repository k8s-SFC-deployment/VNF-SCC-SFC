import time
import subprocess
from multiprocessing import cpu_count

from src.config import config
from src.model import ProcessingLoad, ProcessingLoadV2

def get_cpu_limit():
  with open("/sys/fs/cgroup/cpu/cpu.cfs_quota_us") as fp:
    cfs_quota_us = int(fp.read())
  with open("/sys/fs/cgroup/cpu/cpu.cfs_period_us") as fp:
    cfs_period_us = int(fp.read())
  container_cpus = cfs_quota_us // cfs_period_us
  # For physical machine, the `cfs_quota_us` could be '-1'
  cpus = cpu_count() if container_cpus < 1 else container_cpus
  return cpus

max_core = get_cpu_limit()

# ! well work, but when we limit process cpu performance with `cpulimit`,
# ! process wander every cpu cores. <-- I don't know it's influences.
def stress(processingLoad: ProcessingLoad):
  if processingLoad.cpu_core > max_core:
    raise ValueError(f"core({processingLoad.cpu_core}) is bigger than max core({max_core}).")
  vm = cpu = processingLoad.cpu_core
  vm_bytes = processingLoad.mem_mb // vm
  limit = processingLoad.percentage
  timeout = processingLoad.duration_sec
  
  if vm_bytes == 0:
    stress_ng_script = f'stress-ng --cpu {cpu} --limit {limit} --timeout {timeout}'
    cpulimit_script = ""
  else: 
    stress_ng_script = f'stress-ng --vm {vm} --vm-bytes {vm_bytes}M --timeout {timeout}'
    cpulimit_script = """PIDS=$(ps -ef | grep stress-ng | awk '{ print $2 }')
CPU_IN_USES=$(ps -ef | grep stress-ng | awk '{ print $4 }')
TARGET=()
while IFS= read -r -u3 pid; IFS= read -r -u4 usage; do 
  if [ "$usage" != "0" ]; then
    cpulimit --limit %d --pid $pid &
  fi
done 3<<<"$PIDS" 4<<<"$CPU_IN_USES"
""" % limit
  
  p1 = subprocess.Popen(stress_ng_script, shell=True, executable="/bin/bash")
  time.sleep(0.1) # waiting 'stress-ng' process ready
  p2 = subprocess.Popen(cpulimit_script, shell=True, executable="/bin/bash")
  p1.wait()
  p2.wait()

import asyncio

async def run_async(script):
  return await asyncio.create_subprocess_shell(script, shell=True, executable="/bin/bash")

async def stress_v2(processingLoad: ProcessingLoadV2):
    scripts = []
    if processingLoad.cpu:
        scripts.append(f'stress-ng --cpu {processingLoad.cpu.worker} --cpu-ops {processingLoad.cpu.ops} --cpu-load {processingLoad.cpu.limit}')
    if processingLoad.mem:
        scripts.append(f'stress-ng --vm {processingLoad.mem.worker} --vm-ops {processingLoad.mem.ops} --vm-bytes {processingLoad.mem.bytes}b')
    if processingLoad.dio:
        scripts.append(f'stress-ng --io {processingLoad.dio.worker} --io-ops {processingLoad.dio.ops} --hdd-bytes {processingLoad.dio.bytes}b')

    return await asyncio.gather(*[run_async(script) for script in scripts])

if __name__ == "__main__":
  p_load = config.processingLoad
  stress(p_load)
