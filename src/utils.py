import gi, os, sys, subprocess
""" gi.require_version("Gtk", "3.0")
gi.require_version('Vte', '2.91')
gi.require_version('Notify', '0.7') """
from dateutil.parser import parse
from datetime import datetime, date
import timeago, pytz, time
#gi.require_version('Vte', '2.91')
from gi.repository import Vte
from gi.repository import GLib, Notify

def get_time_ago(d, ms=True):
    pd = parse(d)
    tz = pytz.timezone('UTC')
    fmt = '%Y-%m-%dT%H:%M:%S'
    if ms:
        fmt = fmt+'.%f'
    fmt = fmt+'%z'
    dt = datetime.strptime(pd.astimezone().isoformat(), fmt)
    now = datetime.now()
    ago = timeago.format(dt.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"))
    return ago

def unpack_dict(d, *args, **kwargs):
    if not isinstance(d, dict):
        print('must be a dict!')
        return None
    lst = list()
    for a in args:
        lst.append(d.get(a))
    for k, v in kwargs.items():
        lst.append(d.get(k) or v)

    return tuple(lst)

def spawn_pty(term, argv, envv, callback=None, *cbargs):
    term.spawn_async(
        Vte.PtyFlags.DEFAULT,
        None,
        argv,
        envv,
        GLib.SpawnFlags.DEFAULT,
        None,
        -1,
        -1,
        None,
        callback,
        *cbargs,
    )

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PiB'),
    (1<<40, ' TiB'),
    (1<<30, ' GiB'),
    (1<<20, ' MiB'),
    (1<<10, ' KiB'),
    (1, (' byte', ' bytes')),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)

def get_sub(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)

def notify(summary=None, body=None, icon=None, actions=None):
    notif = Notify.Notification.new(summary, body, icon)
    notif.set_timeout(Notify.EXPIRES_DEFAULT)
    notif.set_urgency(Notify.Urgency.NORMAL)
    if actions is not None:
        for a in actions:
            id, label, cb, data = a
            notif.add_action(id, label, cb, *data)
    notif.show()

def check_priv():
    return 'SUDO_UID' in os.environ

def get_priv():
    if not check_priv():
        subprocess.check_call(['sudo', sys.executable] + sys.argv)

class DashboardRow():
    def __init__(self, id=None, name=None, cmd=None, status=None, ago=None, img=None, hostname=None, ipaddr=None, mac=None):
        self.id=id
        self.name=name
        self.cmd=cmd
        self.status=status
        self.ago=ago
        self.img=img
        self.hostname=hostname
        self.ipaddr=ipaddr
        self.mac=mac

class ContainerRow():
    def __init__(self) -> None:
        d = DashboardRow()
        pass

class ImageRow():
    def __init__(self) -> None:
        pass

class VolumeRow():
    def __init__(self) -> None:
        pass

class NetworkRow():
    def __init__(self) -> None:
        pass

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
