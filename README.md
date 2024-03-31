# VNF Simulating container considering SFC

VNF container with HTTP.

This project implement VNF simulator for stressing environment.
And each VNF can call another VNF with message.

First, user send message (that has recursive format).
And then, VNF consume outer message and resend inner message to another VNF until inner message become `null`.

### Goals

- [x] Relaying
  - We can call next sfc with recursive message.
- [x] stressing
  - [x] CPU
  - [x] Memory
  - [x] Bandwidth


### APIS

- (post) `/load` : provide load to VNF with message. VNF consume this message and resend this inner message to another VNF.
- (get) `/config` : get default load config.
- (post) `/config` : update default load config.

If you want show detail, go below and past [`/asstes/openapi.json`](/assets/openapi.json).

- https://editor.swagger.io/

### Run

```bash
$ docker build -t sfc-simulator -f ./Dockerfile.prod # Dockerfile.dev only has an additional --reload tag when run.
$ docker run -it --rm --cpus 1 -p 7000:7000 sfc-simulator
```
