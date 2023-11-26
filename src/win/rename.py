from gi.repository import Gtk
from client import Docker

@Gtk.Template.from_file('src/ui/rename_container.glade')
class ContainerRenameWindow(Gtk.Window):
    __gtype_name__ = 'wRenameContainer'

    hbRenameContainer: Gtk.HeaderBar = Gtk.Template.Child()
    txtNewName = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()