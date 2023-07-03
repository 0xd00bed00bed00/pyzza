from dateutil.parser import parse
from datetime import datetime, date
import timeago, pytz, time
import gi
gi.require_version('Vte', '2.91')
from gi.repository import Vte, GLib

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