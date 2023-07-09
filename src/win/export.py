from gi.repository import Gtk
from client import Docker
import threading

@Gtk.Template.from_file('src/ui/export_container.glade')
class ContainerSaveWindow(Gtk.Window):
    __gtype_name__ = 'fcdExportContainer'

    id = None
    name = None

    hbExportContainer = Gtk.Template.Child()

    def __init__(self, id):
        super().__init__()
        self.dc = Docker()
        self.id = id

    @Gtk.Template.Callback()
    def fcbExport_clicked_cb(self, args):
        id = self.id
        filename = self.get_current_name() or self.name
        self.destroy()
        th = threading.Thread(target=self.dc.export_container, args=[id, filename], daemon=True)
        th.start()

    @Gtk.Template.Callback()
    def fcbCancelExport_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def fcdExportContainer_current_folder_changed_cb(self, args):
        print('fcdExportContainer_current_folder_changed_cb')

    @Gtk.Template.Callback()
    def fcdExportContainer_file_activated_cb(self, args):
        print('fcdExportContainer_file_activated_cb')

    @Gtk.Template.Callback()
    def fcdExportContainer_selection_changed_cb(self, args):
        print('fcdExportContainer_selection_changed_cb')

    @Gtk.Template.Callback()
    def fcdExportContainer_update_preview_cb(self, args):
        print('fcdExportContainer_update_preview_cb')