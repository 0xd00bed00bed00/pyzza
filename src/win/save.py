from gi.repository import Gtk

@Gtk.Template.from_file('src/ui/save_image.glade')
class ImageSaveWindow(Gtk.FileChooserDialog):
    __gtype_name__ = 'fcdSaveImage'

    hbSaveImage: Gtk.HeaderBar = Gtk.Template.Child()
    #fctSaveFilename = Gtk.Template.Child()

    def __init__(self, name=None):
        super().__init__()
        self.hbSaveImage.set_subtitle(name)
        #self.fctSaveFilename.set_text(name)

    @Gtk.Template.Callback()
    def fcbSave_clicked_cb(self, args):
        print('[fcbSave_clicked_cb]:', args)
        self.destroy()

    @Gtk.Template.Callback()
    def fcbCancelSave_clicked_cb(self, args):
        self.destroy()