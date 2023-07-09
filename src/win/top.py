from gi.repository import Gtk
from client import Docker

@Gtk.Template.from_file('src/ui/top.glade')
class ContainerTopWindow(Gtk.Window):
    __gtype_name__ = 'wTop'

    wsTop = Gtk.Template.Child()
    hbTop = Gtk.Template.Child()
    id = None
    name = None

    def __init__(self, id=None, name=None):
        super().__init__()
        self.dc = Docker()
        self.id = id
        self.name = name

    def show(self):
        self.hbTop.set_subtitle(self.name)
        top = self.dc.container_top(self.id)
        procs = top['Processes']
        for proc in procs:
            self.wsTop.append(proc)

        super().show()