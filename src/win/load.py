from gi.repository import Gtk

@Gtk.Template.from_file('src/ui/load_image.glade')
class ImageLoadWindow(Gtk.FileChooserDialog):
    __gtype_name__ = 'fcdLoadImage'

    def __init__(self):
        super().__init__()

    #@Gtk.Template.Callback()
    def fcbCancelOpen(self, args):
        pass

    #@Gtk.Template.Callback()
    def fcbOpen(self, args):
        pass