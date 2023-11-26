from utils import *

def dashboard_create_row(client, id=None, immut=False):
    if id is None: return
    try:
        m = client.get_container(id)
        ago = get_time_ago(m.attrs['Created'])
        name = m.name
        cmd = "{} {}".format(m.attrs['Path'], ' '.join(m.attrs['Args'])).strip()
        status = m.attrs['State']['Status']
        img = m.attrs['Config']['Image']
        hostname = m.attrs['Config']['Hostname']
        ipaddr = m.attrs['NetworkSettings']['IPAddress']
        macaddr = m.attrs['NetworkSettings']['MacAddress']
        ports = []
        bindings = m.attrs['HostConfig']['PortBindings']
        if bindings is not None:
            for key, binding in bindings.items():
                hports = []
                for b in binding:
                    hports.append(b['HostPort'])
                hports = ','.join(hports)
                ports.append(f'{key}:{hports}')
        #for (key, value) in m.attrs['HostConfig']['PortBindings']:
        #    ports.append(f'{key}:{value["HostPort"]}')
        print('[ports]:', ports)
        r = [
            id,
            name,
            cmd,
            status,
            ago,
            img,
            ','.join(ports),
            '',
            hostname,
            ipaddr,
            macaddr,
        ]
        if immut: return tuple(r)
        return r
    except Exception as e:
        print('[dashboard_create_row] error:', e)

def containers_create_row(client, id=None, immut=False):
    if id is None: return
    try:
        m = client.get_container(id)
        ago = get_time_ago(m.attrs['Created'])
        name = m.name
        cmd = "{} {}".format(m.attrs['Path'], ' '.join(m.attrs['Args'])).strip()
        status = m.attrs['State']['Status']
        img = m.attrs['Config']['Image']
        hostname = m.attrs['Config']['Hostname']
        ipaddr = m.attrs['NetworkSettings']['IPAddress']
        macaddr = m.attrs['NetworkSettings']['MacAddress']
        r = [
            m.id,
            name,
            cmd,
            status,
            ago,
            img,
            hostname,
            ipaddr,
            macaddr,
        ]
        if immut: return tuple(r)
        return r
    except:
        print('[containers_create_row] error')

def images_create_row(client, id=None, immut=False):
    try:
        m = client.get_image(id)
        ago = get_time_ago(m.attrs['Created'])
        size = pretty_size(m.attrs['Size'])
        vsize = pretty_size(m.attrs['VirtualSize'])
        r = [
            id,
            len(m.tags)>0 and m.tags[0].split(':')[0] or '<none>',
            ago,
            size,
            vsize,
        ]
        if immut: return tuple(r)
        return r
    except Exception as e:
        print('[images_create_row] error:', e)

def volumes_create_row(client, id=None, immut=False):
    try:
        v = client.get_volume(id)
        ago = get_time_ago(v.attrs['CreatedAt'], ms=False)
        r = [
            id,
            v.attrs['Name'],
            ago,
            v.attrs['Mountpoint']
        ]
        if immut: return tuple(r)
        return r
    except Exception as e:
        print('[volumes_create_row] error:', e)

def networks_create_row(client, id=None, immut=False):
    try:
        n = client.get_network(id)
        ago = get_time_ago(n.attrs['Created'])
        r = [
            id,
            n.attrs['Name'],
            ago,
            ':80/tcp',
        ]
        if immut: return tuple(r)
        return r
    except Exception as e:
        print('[networks_create_row] error:', e)

def getrowdata(model, iter):
    return model.get(iter, *[i for i in range(model.get_n_columns())])