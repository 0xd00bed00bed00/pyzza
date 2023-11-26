from __future__ import unicode_literals
import gi, os, sys, subprocess
from dateutil.parser import parse
from datetime import datetime, date
import timeago, pytz, time
gi.require_version('Gtk', '3.0')
from gi.repository import Vte
from gi.repository import GLib, Notify
import string, random, uuid
from pyee.base import EventEmitter

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
        os.environ['HOME'],
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

def gen_id(retstr=True):
    rnd = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    uid = uuid.uuid5(uuid.NAMESPACE_DNS, rnd)
    if retstr:
        id = str(uid)
        return id
    return uid

ee = EventEmitter()