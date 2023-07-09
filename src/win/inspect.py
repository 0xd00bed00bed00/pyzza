from gi.repository import Gtk

@Gtk.Template.from_file('src/ui/inspect.glade')
class InspectWindow(Gtk.Window):
    __gtype_name__ = 'wInspect'

    tbuData = Gtk.Template.Child()
    hbInspect = Gtk.Template.Child()

    def __init__(self, name=None, data=None):
        super().__init__()
        self.hbInspect.set_subtitle(name)
        self.tbuData.set_text(data)