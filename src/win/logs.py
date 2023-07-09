from gi.repository import Gtk

@Gtk.Template.from_file('src/ui/logs.glade')
class ContainerLogsWindow(Gtk.Window):
    __gtype_name__ = 'wLogs'

    def __init__(self):
        super().__init__()