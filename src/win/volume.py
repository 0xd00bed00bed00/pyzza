from gi.repository import Gtk
from client import Docker
from args import CreateVolumeArgs
from utils import notify
from config import errLogger

@Gtk.Template.from_file('src/ui/add_container_volume.glade')
class AddVolumeWindow(Gtk.Window):
    __gtype_name__ = 'wAddContainerVolume'

    txtHostPath = Gtk.Template.Child()
    txtContainerPath = Gtk.Template.Child()
    chReadonly = Gtk.Template.Child()
    bSubmit = Gtk.Template.Child()
    bCancel = Gtk.Template.Child()

    def __init__(self, image_name=None, cb=None):
        super().__init__()
        self.image = image_name
        self.cb = cb

    @Gtk.Template.Callback()
    def bSubmit_clicked_cb(self, args):
        hostPath = self.txtHostPath.get_text()
        containerPath = self.txtContainerPath.get_text()
        readonly = self.chReadonly.get_active()
        mode = 'rw'
        if readonly:
            mode = 'ro'
        if self.cb is not None:
            self.cb((
                hostPath,
                {
                    'bind': containerPath,
                    'mode': mode,
                },
            ))
        self.destroy()

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

@Gtk.Template.from_file('src/ui/new_volume.glade')
class NewVolumeWindow(Gtk.Window):
    __gtype_name__ = 'wNewVolume'

    txtName = Gtk.Template.Child()
    txtDriver = Gtk.Template.Child()
    txtOptOrLbl = Gtk.Template.Child()
    bAddOption = Gtk.Template.Child()
    bRemoveOption = Gtk.Template.Child()
    bAddLabel = Gtk.Template.Child()
    bRemoveLabel = Gtk.Template.Child()
    bSubmit = Gtk.Template.Child()
    bCancel = Gtk.Template.Child()
    lbOpts = Gtk.Template.Child()
    lbLabels = Gtk.Template.Child()

    options = dict()
    labels = dict()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    @Gtk.Template.Callback()
    def bAddOption_clicked_cb(self, args):
        opt = self.txtOptOrLbl.get_text()
        row = Gtk.ListBoxRow()
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(opt)
        txt.set_visible(True)
        row.add(txt)
        self.lbOpts.insert(row, -1)
        self.txtOptOrLbl.set_text('')

    @Gtk.Template.Callback()
    def bRemoveOption_clicked_cb(self, args):
        row = self.lbOpts.get_selected_row()
        if row is not None:
            row.destroy()

    @Gtk.Template.Callback()
    def bAddLabel_clicked_cb(self, args):
        lbl = self.txtOptOrLbl.get_text()
        if lbl == '':
            return
        row = Gtk.ListBoxRow()
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(lbl)
        txt.set_visible(True)
        row.add(txt)
        self.lbLabels.insert(row, -1)
        self.txtOptOrLbl.set_text('')

    @Gtk.Template.Callback()
    def bRemoveLabel_clicked_cb(self, args):
        row = self.lbLabels.get_selected_row()
        if row is not None:
            row.destroy()

    @Gtk.Template.Callback()
    def bSubmit_clicked_cb(self, args):
        name = self.txtName.get_text()
        driver = self.txtDriver.get_text()
        self.lbOpts.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.lbOpts.select_all()
        self.lbOpts.selected_foreach(
            lambda box, row, *user_data:
                self.parse_opts(box, row)
        )
        self.lbOpts.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.lbLabels.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.lbLabels.select_all()
        self.lbLabels.selected_foreach(
            lambda box,  row, *user_data:
                self.parse_lbl(box, row)
        )
        self.lbLabels.set_selection_mode(Gtk.SelectionMode.SINGLE)
        volargs = CreateVolumeArgs(
            name=name,
            driver=driver,
            driver_opts=self.options,
            labels=self.labels,
        )
        try:
            self.client.create_volume(volargs)
            self.options.clear()
            self.labels.clear()
        except Exception as e:
            notify(summary='Failed to create volume', body=f'{e}')
            errLogger.error(e, exc_info=True)
        self.destroy()

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    def parse_opts(self, box, row):
        children = row.get_children()
        lbl = children[0]
        txt = lbl.get_text()
        k, v = str(txt).split('=')
        self.options[k] = v
        
    def parse_lbl(self, box, row):
        children = row.get_children()
        lbl = children[0]
        txt = lbl.get_text()
        k, v = str(txt).split('=')
        self.options[k] = v

    def show(self):
        super().show()