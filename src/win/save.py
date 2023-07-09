from gi.repository import Gtk

@Gtk.Template.from_file('src/ui/save_image.glade')
class ImageExportWindow(Gtk.Window):
    __gtype_name__ = 'fcdSaveImage'

    hbSaveImage = Gtk.Template.Child()
    fctSaveFilename = Gtk.Template.Child()

    def __init__(self, name=None):
        super().__init__()
        self.hbSaveImage.set_subtitle(name)
        self.fctSaveFilename.set_text(name)

    @Gtk.Template.Callback()
    def fcbSave_clicked_cb(self, args):
        print('[fcbSave_clicked_cb]:', args)

    @Gtk.Template.Callback()
    def fcbCancelSave_clicked_cb(self, args):
        print('[fcbCancelSave_clicked_cb]:', args)