# VNF-SCC-SFC

VNF Simulating Container Considering SFC with HTTP

This project implement VNF simulator for stressing environment with `stress-ng`.
And each VNF can call another VNF with message.

First, user send message (that has recursive format).
And then, VNF consume outer message and resend inner message to another VNF until inner message become `null`.

## Goals

- [x] Relaying
  - We can call next sfc with recursive message.
- [x] stressing
  - [x] CPU
  - [x] Memory
  - [x] Bandwidth
- [x] setting up configuration when container start with envs

## APIS

- (post) `/loadv2`: provide load to VNF with message. VNF consume this message and resend its inner message to next VNF. It's load based on operation count.
- (post) `/load`(deprecated) : provide load to VNF with message. VNF consume this message and resend its inner message to next VNF. It's load based on time.
- (get) `/config` : get default load config.

If you want to show detail, go below and past [`/asstes/openapi.json`](/assets/openapi.json).

- https://editor.swagger.io/

## Run

```bash
$ docker build -t vnf-scc-sfc -f ./Dockerfile.prod . # Dockerfile.dev only has an additional --reload tag when run.
$ docker run -it --rm --cpus 1 -p 7000:7000 vnf-scc-sfc
```

If you want to run this with k8s environment, check [`/k8s/`](/k8s/)

### For development

```bash
$ docker build -t vnf-scc-sfc -f ./Dockerfile.dev . # Dockerfile.dev only has an additional --reload tag when run. (for hot-reload)
$ docker run -it --rm -v $(pwd):/app --cpus 1 -p 7000:7000 vnf-scc-sfc
```

### Enviroment Variables

- `CPU_OPS` : default number of cpu operation
- `CPU_WORKER` : default number of cpu worker
- `CPU_LIMIT` : default cpu limit (%)
- `MEM_OPS` : default number of memory operation
- `MEM_WORKER` : default number of memory worker
- `MEM_BYTES` : default memory bytes to allocate (bytes) 
- `DIO_OPS` : default number of disk IO operation
- `DIO_WORKER` : default number of disk IO worker
- `DIO_BYTES` : default hdd bytes to allocate (bytes)

### Reference

- docker hub : https://hub.docker.com/repository/docker/euidong/vnf-scc-sfc
