from gi.repository import Gtk
from win.term import exec

@Gtk.Template.from_file('src/ui/pull_image.glade')
class ImagePullWindow(Gtk.Window):
    __gtype_name__ = 'wPullImage'

    txtImageRepo = Gtk.Template.Child()

    def __init__(self, repo=None):
        super().__init__()

    @Gtk.Template.Callback()
    def bPull_clicked_cb(self, args):
        repo = self.txtImageRepo.get_text()
        exec(repo, argv=[
            'docker',
            'pull',
            repo,
        ])
        self.destroy()

    @Gtk.Template.Callback()
    def bCancelPull_clicked_cb(self, args):
        self.destroy()