from utils import get_time_ago, spawn_pty, pretty_size
from common import *
from args import *
import os, inspect, docker
#inspect.getfile(os)
#inspect.getfile(docker)
#os.path.dirname(inspect.getfile(docker))

import docker
from docker import DockerClient

class Docker:
    def __init__(self):
        global DOCKER_DEFAULT_HOST
        global _dock
        global _apiclient

        _dock = None
        if os.environ.get('DOCKER_HOST') is not None:
            _dock = docker.from_env()
        else:
            _dock = DockerClient(base_url='tcp://0.0.0.0:2375') #docker.from_env()
        _apiclient = _dock.api
        self.daemon = _dock
        self.client = _apiclient
    
    def list_containers(self):
        containers = []
        containers = _dock.containers.list(all=False)
        
        store = []
        for cont in containers:
            try:
                c = cont.attrs
                id = cont.id
                ago = get_time_ago(c['Created'])
                name = cont.name
                cmd = "{} {}".format(c['Path'], ' '.join(c['Args'])).strip()
                status = c['State']['Status']
                img = c['Config']['Image']
                hostname = c['Config']['Hostname']
                ipaddr = c['NetworkSettings']['IPAddress']
                macaddr = c['NetworkSettings']['MacAddress']
                r = [
                    id,
                    name,
                    cmd,
                    status,
                    ago,
                    img,
                    '',
                    '',
                    hostname,
                    ipaddr,
                    macaddr,
                ]
                store.append(r)
                yield r
            except Exception as e:
                print('[list_containers] error:', e)

    def list_containers_all(self):
        containers = []
        containers = _dock.containers.list(all=True)
        
        for cont in containers:
            try:
                c = cont.attrs
                id = cont.id
                ago = get_time_ago(c['Created'])
                name = cont.name
                cmd = "{} {}".format(c['Path'], ' '.join(c['Args'])).strip()
                status = c['State']['Status']
                if status == 'running' or status == 'paused':
                    continue
                img = c['Config']['Image']
                hostname = c['Config']['Hostname']
                ipaddr = c['NetworkSettings']['IPAddress']
                macaddr = c['NetworkSettings']['MacAddress']
                r = [
                    id,
                    name,
                    cmd,
                    status,
                    ago,
                    img,
                    hostname,
                    ipaddr,
                    macaddr,
                ]
                yield (r, cont, c)
            except Exception as e:
                print('[list_containers_all] error:', e)

    def list_images(self):
        images = []
        images = _dock.images.list()

        store = []
        for img in images:
            try:
                i = img.attrs
                id = img.id
                ago = get_time_ago(i['Created'])
                size = pretty_size(i['Size'])
                vsize = pretty_size(i['VirtualSize'])
                r = [
                    id,
                    len(img.tags)>0 and img.tags[0].split(':')[0] or '<none>',
                    ago,
                    size,
                    vsize,
                ]
                store.append(r)
                yield r
            except Exception as e:
                print('[list_images] error:', e)

    def list_volumes(self):
        volumes = _dock.volumes.list()

        store = []
        for vol in volumes:
            try:
                id = vol.id
                v = vol.attrs
                ago = get_time_ago(v['CreatedAt'], ms=False)
                r = [
                    id,
                    v['Name'],
                    ago,
                    vol.attrs['Mountpoint']
                ]
                store.append(r)
                yield r
            except Exception as e:
                print('[list_volumes] error:', e)

    def list_networks(self):
        networks = _dock.networks.list()

        store = []
        for net in networks:
            try:
                id = net.id
                n = net.attrs
                ago = get_time_ago(n['Created'])
                r = [
                    id,
                    n['Name'],
                    ago,
                    ':80/tcp',
                ]
                store.append(r)
                yield r
            except Exception as e:
                print('[list_networks] error:', e)

    def start_container(self, id):
        _apiclient.start(id)

    def run_container(self, kwargs = RunContanerKwargs()):
        return _dock.containers.run(**kwargs.__dict__)

    def stop_container(self, id):
        _apiclient.stop(id, timeout=0)
        
    def restart_container(self, id):
        _apiclient.restart(id)

    def suspend_container(self, id):
        _apiclient.pause(id)

    def resume_container(self, id):
        _apiclient.unpause(id)

    def kill_container(self, id):
        _apiclient.kill(id)
        
    def search_image(self, term):
        #return _dock.images.search(term)
        return _apiclient.search(term=term)

    def pull_image(self, repo):
        _dock.images.pull(repository=repo)
        
    def build_image(self, kwargs = BuildImageKwargs()):
        _dock.images.build(**kwargs.__dict__)

    def import_image(self, filename):
        pass

    def container_top(self, id, psargs=None):
        return _apiclient.top(id, ps_args=psargs)
    
    def exec_run(self, id, kwargs=ExecRunKwargs()):
        cont = _dock.containers.get(id)
        (exit_code, output) = cont.exec_run(**kwargs.__dict__)
        return (exit_code, output)
    
    def ls(self, id, path=None):
        kwargs = ExecRunKwargs(cmd=f'ls -NAlhkL --group-directories-first {path or "."}')
        (exit_code, output) = self.exec_run(id, kwargs=kwargs)
        output = str(output.decode('ascii')).strip()
        names = output.split('\n')
        return names
    
    def stat(self, id, path):
        kwargs = ExecRunKwargs(cmd=f'file {path}')
        (exit_code, output) = self.exec_run(id, kwargs=kwargs)
        output = str(output.decode('ascii')).strip()
        #print(output)
        return output
    
    def get_file_type(self, id, path):
        cmd = self.check_if_exists(
            path,
            true=self.check_if_dir(
                path,
                true='echo directory',
                false=self.check_if_file(
                    path,
                    true='echo file',
                    false=self.check_if_link(
                        path,
                        true='echo symlink',
                        false='exit 1'
                    ),
                ),
            ),
            false='exit 1',
        )
        #print('[cmd]: ', cmd)
        kwargs = ExecRunKwargs(cmd=f'sh -c "{cmd}"')
        (exit_code, output) = self.exec_run(id, kwargs=kwargs)
        output = str(output.decode('ascii')).strip()
        #print(output, exit_code)
        return output
    
    def get_mime_type(self, id, path):
        kwargs = ExecRunKwargs(cmd=f'file -b {path}')
        (exit_code, output) = self.exec_run(id, kwargs=kwargs)
        output = str(output.decode('ascii')).strip()
        print(output, exit_code)
        return output

    def check_if_file(self, path, true='echo "file" && exit 2', false=None):
        return f'[ -f {path} ] && {true} || ({false})'
    def check_if_dir(self, path, true='echo "directory" && exit 1', false=None):
        return f'[ -d {path} ] && {true} || ({false})'
    def check_if_link(self, path, true='echo "symlink" && exit 3', false=None):
        return f'[ -l {path} ] && {true} || ({false})'
    def check_if_exists(self, path, true=None, false=None):
        return f'[ -e {path} ] && ({true}) || ({false})'
    def check_if(self, path):
        return f'[ -e {path} ]'

    def exec_container(self, term, name, flags, cmd, callback=None, *cbargs):
        c = ['docker', 'exec']
        if flags is not None:
            c = c + flags
        c.append(name)
        c.append(cmd)
        spawn_pty(term, c, [], callback, *cbargs)

    def container_logs(self, id):
        pass

    def export_container(self, id, name=None):
        cont = self.get_container(id)
        export = cont.export()
        f = open(name or cont.name, 'wb')
        for b in export:
            f.write(b)
        f.close()
        return export
    
    def diff_container(self, id):
        cont = self.get_container(id)
        return cont.diff()

    def get_archive(self, id, path):
        cont = self.get_container(id)
        return cont.get_archive(path)

    def create_container(self, kwargs = CreateContanerKwargs()):
        return _dock.containers.create(**kwargs.__dict__)
    
    def image_history(self, id):
        return _apiclient.history(id)
    
    def put_archive(self, id, path, data):
        cont = self.get_container(id)
        cont.put_archive(path, data)

    def prune_containers(self):
        return _dock.containers.prune()

    def prune_images(self):
        return _dock.images.prune()

    def inspect(self, id, model=None):
        if model == ModelType.CONTAINER:
            return self.inspect_container(id)
        elif model == ModelType.IMAGE:
            return self.inspect_image(id)
        elif model == ModelType.VOLUME:
            return self.inspect_volume(id)
        elif model == ModelType.NETWORK:
            return self.inspect_network(id)
    
    def inspect_container(self, id):
        return _apiclient.inspect_container(id)

    def inspect_image(self, id):
        return _apiclient.inspect_image(id)

    def inspect_volume(self, id):
        return _apiclient.inspect_volume(id)

    def inspect_network(self, id):
        return _apiclient.inspect_network(id)

    def inspector(self, model):
        if model == ModelType.CONTAINER:
            return _apiclient.inspect_container
        elif model == ModelType.IMAGE:
            return _apiclient.inspect_image
        elif model == ModelType.VOLUME:
            return _apiclient.inspect_volume
        elif model == ModelType.NETWORK:
            return _apiclient.inspect_network
    
    def get(self, id, model):
        if model == ModelType.CONTAINER:
            return self.get_container(id)
        elif model == ModelType.IMAGE:
            return self.get_image(id)
        elif model == ModelType.VOLUME:
            return self.get_volume(id)
        elif model == ModelType.NETWORK:
            return self.get_network(id)

    def get_container(self, id):
        return _dock.containers.get(id)

    def get_image(self, id):
        return _dock.images.get(id)

    def get_volume(self, id):
        return _dock.volumes.get(id)

    def get_network(self, id):
        return _dock.networks.get(id)

    def getter(self, model):
        if model == ModelType.CONTAINER:
            return _dock.containers.get
        elif model == ModelType.IMAGE:
            return _dock.images.get
        elif model == ModelType.VOLUME:
            return _dock.volumes.get
        elif model == ModelType.NETWORK:
            return _dock.networks.get