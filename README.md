# PYZZA
Linux desktop app using Glade, GTK+ and Python for managing Docker images and containers

## DEVELOPMENT

clone this repo

```bash
git clone https://github.com/0xd00bed00bed00/pyzza
```

install required packages (Manjaro)

```bash
pamac install gtk3 vte3
```

check python version

```bash
which python3
python -V
```

create virtual environment (optional)

```bash
python3 -m venv .venv
```

activate environment

```bash
source .venv/bin/activate
```

install dependencies

```bash
pip install -r requirements.txt
```

run

```
./launch
```

## BUILD

```bash
./scripts/build
```
This will generate a single binary that includes all dependencies causing its file size to be large.

## DEBUG

```bash
./scripts/debug
```
This will generate an uncompressed debug build under `.debug`

## USER INTERFACE

To edit UI files in `src/ui` Glade must be installed in your system


## DOCKER

By default the port used is `2376` (rootless). If you want to connect to the Docker Engine daemon process change `DOCKER_HOST` in the `config.py`

A script `scripts/dockerd` for running rootless Docker via TCP is also provided

## FEATURES
### GLOBAL
- [x] built-in terminal
- [x] settings window for changing connection

### CONTAINERS
- [x] run container
- [x] start/stop/suspend/resume container
- [x] kill container
- [x] create container
- [x] exec container
- [x] browse container
- [x] show logs
- [x] show top
- [x] inspect
- [x] copy from
- [x] copy to
- [ ] attach container
- [ ] prune

### IMAGES
- [x] pull image
- [x] build image
- [x] show history
- [x] search image
- [x] save image
- [x] load image
- [x] inspect
- [ ] prune
- [ ] create container/pull/run from search

### VOLUMES
- [x] inspect

### NETWORKS
- [x] inspect

### IN PROGRESS
- [ ] connect to multiple Docker instances
- [ ] alert notifications for messages
- [ ] swarms

## TODO
