from gi.repository import Gtk
from args import CreateContanerKwargs
from client import Docker
import threading

@Gtk.Template.from_file('src/ui/create_container.glade')
class ContainerCreateWindow(Gtk.Window):
    __gtype_name__ = 'wCreateContainer'

    hbCreateContainer = Gtk.Template.Child()
    txtcImageName = Gtk.Template.Child()
    txtcContainerName = Gtk.Template.Child()
    txtcCommand = Gtk.Template.Child()
    txtcWorkingDir = Gtk.Template.Child()

    image = None

    def __init__(self, image=None):
        super().__init__()
        self.dc = Docker()
        self.image = image
        if image is not None:
            self.hbCreateContainer.set_subtitle(image)
            self.txtcImageName.set_text(image)
            self.txtcImageName.set_editable(False)

    @Gtk.Template.Callback()
    def bCreateContainerSubmit_clicked_cb(self, args):
        imgname = self.txtcImageName.get_text()
        conname = self.txtcContainerName.get_text()
        command = self.txtcCommand.get_text()
        wdir = self.txtcWorkingDir.get_text()
        kwargs = CreateContanerKwargs(image=imgname, name=conname, command=command, working_dir=wdir)
        th = threading.Thread(target=self.dc.create_container, args=[kwargs], daemon=True)
        th.start()
        self.destroy()

    @Gtk.Template.Callback()
    def bCreateContainerCancel_clicked_cb(self, args):
        self.destroy()