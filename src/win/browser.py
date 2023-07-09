from gi.repository import Gtk
from client import Docker

@Gtk.Template.from_file('src/ui/file_explorer.glade')
class BrowserWindow(Gtk.Window):
    __gtype_name__ = 'wFileExplorer'

    container_id = None
    container_name = None
    container = None
    hbFileExplorer = Gtk.Template.Child()
    tvFileExplorer = Gtk.Template.Child()
    tsFileExplorer = Gtk.Template.Child()

    def __init__(self, container=None):
        super().__init__()
        self.dc = Docker()
        assert container is not None
        print(container[0][0], container[0][1])
        self.container_id = container[0][0]
        self.container_name = container[0][1]
        self.hbFileExplorer.set_subtitle(self.container_name or self.container_id)

    def show(self):
        for name in self.dc.ls(self.container_id, path='/'):
            if name in ['.', '..']:
                continue
            self.tsFileExplorer.append(None, [name, '', ''])
        super().show()

    @Gtk.Template.Callback()
    def tvFileExplorer_row_expanded_cb(self, a, b, c):
        print('row-expanded')

    @Gtk.Template.Callback()
    def tvFileExplorer_row_activated_cb(self, a, b, c):
        print('row-activated')

    @Gtk.Template.Callback()
    def tvFileExplorer_move_cursor_cb(self, a, b, c):
        print('move-cursor')

    @Gtk.Template.Callback()
    def tvFileExplorer_cursor_changed_cb(self, args):
        print('cursor-changed')
        sel = args.get_selection()
        [model, iter] = sel.get_selected()
        names = model.get(iter, 0)
        tree = list(names)
        file_path = '/'.join(tree)
        stat = self.dc.stat(self.container_id, path=file_path)
        for name in self.dc.ls(self.container_id, path=file_path):
            if name in ['.', '..']:
                continue
            print(name)
            model.append(iter, [name, '', ''])