# PYZZA
Linux desktop app using Glade, GTK+ and Python for managing Docker images and containers

[![Pyzza](https://github.com/0xd00bed00bed00/pyzza/actions/workflows/ci.yml/badge.svg)]()
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/0xd00bed00bed00/pyzza/ci.yml?logo=github)
![GitHub release (with filter)](https://img.shields.io/github/v/release/0xd00bed00bed00/pyzza?logo=github)
![GitHub release (by tag)](https://img.shields.io/github/downloads/0xd00bed00bed00/pyzza/latest/total?logo=github)


## DEVELOPMENT

clone this repo

```bash
git clone https://github.com/0xd00bed00bed00/pyzza
```

### MANJARO INSTALLATION

```bash
pamac install gtk3 vte3 python-gobject
```

### ARCH LINUX INSTALLATION
```bash
pacman -S gtk3 vte3 python-gobject
```


### UBUNTU INSTALLATION (Untested)
install required packages
```bash
apt-get install libgirepository1.0-dev python3-gi libgtk-3-dev libvte-2.91-0 python3-psycopg2 libpq-dev
```

check python version

```bash
which python3
python3 -V
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
This will generate a single binary under `dist` that includes all dependencies causing its file size to be large.

## DEBUG

```bash
./scripts/debug
```
This will generate an uncompressed debug build under `dist/pyzza-debug`

## USER INTERFACE

To edit UI files in `src/ui` Glade must be installed in your system


## DOCKER

By default the port used is `2376` (rootless). If you want to connect to the Docker Engine daemon process change `DOCKER_HOST` in `src/.env`

A script `scripts/dockerd` for running rootless Docker via TCP is also provided

## FEATURES
### GLOBAL
- [x] built-in terminal
- [x] settings window for changing connection
- [x] alert notifications for messages

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
- [x] prune
- [ ] rename

### IMAGES
- [x] pull image
- [x] build image
- [x] show history
- [x] search image
- [x] save image
- [x] load image
- [x] inspect
- [x] prune
- [ ] create container/pull/run from search

### VOLUMES
- [x] inspect
- [x] create volumes

### NETWORKS
- [x] inspect
- [x] create networks

### IN PROGRESS
- [ ] connect to multiple Docker instances
- [ ] swarms

## TODO
- [ ] more options when running containers (ports, volumes, etc.)
- [ ] more options when creating images