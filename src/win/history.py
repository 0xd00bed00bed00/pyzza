from gi.repository import Gtk
from client import Docker
from utils import *

@Gtk.Template.from_file('src/ui/history.glade')
class ImageHistoryWindow(Gtk.Window):
    __gtype_name__ = 'wHistory'

    wsHistory = Gtk.Template.Child()
    hbHistory = Gtk.Template.Child()

    history = None

    def __init__(self, id, name=None):
        super().__init__()
        self.dc = Docker()
        history = self.dc.image_history(id)
        self.history = history
        self.hbHistory.set_subtitle(name)

    def show(self):
        for h in self.history:
            dt = datetime.fromtimestamp(h['Created'])
            self.wsHistory.append([
                h['Id'][:12],
                get_time_ago(dt.strftime("%Y-%m-%d %H:%M:%S"), ms=False),
                h['CreatedBy'],
                pretty_size(h['Size']),
                h['Comment'],
            ])
        super().show()