import time
import subprocess
from multiprocessing import cpu_count

from src.config import config
from src.model import ProcessingLoad

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


if __name__ == "__main__":
  p_load = config.processingLoad
  stress(p_load)
