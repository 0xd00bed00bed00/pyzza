from gi.repository import Gtk
from client import Docker

@Gtk.Template.from_file('src/ui/diff.glade')
class ContainerDiffWindow(Gtk.Window):
    __gtype_name__ = 'wContainerDiff'

    hbDiff: Gtk.HeaderBar = Gtk.Template.Child()
    diffTree = Gtk.Template.Child()
    lsDiff = Gtk.Template.Child()

    diff_kind = ['C', 'A', 'D']

    def __init__(self, client: Docker=None, container_id=None):
        super().__init__()
        self.client = client
        self.container_id = container_id
        self.hbDiff.set_subtitle(container_id)

    def show(self):
        super().show()
        diffs = self.client.diff_container(self.container_id)
        for diff in diffs:
            self.lsDiff.append([
                diff['Path'],
                self.diff_kind[diff['Kind']],
            ])