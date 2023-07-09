from gi.repository import Gtk

@Gtk.Template.from_file('src/ui/rename_container.glade')
class ContainerRenameWindow(Gtk.Window):
    __gtype_name__ = 'wRename'

    def __init__(self):
        super().__init__()