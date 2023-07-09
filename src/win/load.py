from gi.repository import Gtk

@Gtk.Template.from_file('src/ui/load_image.glade')
class ImageLoadWindow(Gtk.FileChooserDialog):
    __gtype_name__ = 'fcdLoadImage'

    def __init__(self):
        super().__init__()