from gi.repository import Gtk, Vte
from client import Docker

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