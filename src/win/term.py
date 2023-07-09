from gi.repository import Gtk, Vte
from client import Docker
from utils import spawn_pty

@Gtk.Template.from_file('src/ui/terminal.glade')
class TerminalWindow(Gtk.Window):
    __gtype_name__ = 'wTerm'
    wvTerm = Gtk.Template.Child()
    hbTerm = Gtk.Template.Child()
    name = None
    flags = None
    cmd = None
    def __init__(self, name=None, subtitle=None, flags=None, cmd=None):
        super().__init__()
        self.dc = Docker()
        self.name=name
        self.flags=flags
        self.cmd=cmd
        self.hbTerm.set_title(name)
        self.hbTerm.set_subtitle(subtitle)
    def spawn(self):
        assert self.wvTerm is not None
        self.dc.exec_container(self.wvTerm, name=self.name, flags=self.flags, cmd=self.cmd)

class Terminal(Vte.Terminal):
    def check():
        pass

def exec(title=None, subtitle=None, argv=None, envv=None, callback=None, *cbargs):
    term = TerminalWindow(name=title, subtitle=subtitle)
    spawn_pty(term.wvTerm, argv, envv, callback, *cbargs)
    term.show()