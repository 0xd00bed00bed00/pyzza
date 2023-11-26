from gi.repository import Gtk
from client import Docker
from args import CreateNetworkArgs
from utils import notify
from config import errLogger

@Gtk.Template.from_file('src/ui/new_network.glade')
class NewNetworkWindow(Gtk.Window):
    __gtype_name__ = 'wNewNetwork'

    txtName = Gtk.Template.Child()
    txtDriver = Gtk.Template.Child()
    txtScope = Gtk.Template.Child()
    txtOptOrLbl = Gtk.Template.Child()

    chCheckDuplicate = Gtk.Template.Child()
    chEnableIPv6 = Gtk.Template.Child()
    chIngress = Gtk.Template.Child()
    chInternal = Gtk.Template.Child()
    chAttachable = Gtk.Template.Child()

    bAddOpt = Gtk.Template.Child()
    bRemoveOpt = Gtk.Template.Child()
    bAddLabel = Gtk.Template.Child()
    bRemoveLabel = Gtk.Template.Child()
    bSubmit = Gtk.Template.Child()
    bCancel = Gtk.Template.Child()

    lbOptions = Gtk.Template.Child()
    lbLabels = Gtk.Template.Child()

    options = dict()
    labels = dict()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    @Gtk.Template.Callback()
    def bAddOpt_clicked_cb(self, args):
        opt = self.txtOptOrLbl.get_text()
        if opt == '':
            return
        row = Gtk.ListBoxRow()
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(opt)
        txt.set_visible(True)
        row.add(txt)
        self.lbOptions.insert(row, -1)
        self.txtOptOrLbl.set_text('')

    @Gtk.Template.Callback()
    def bRemoveOpt_clicked_cb(self, args):
        row = self.lbLabels.get_selected_row()
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
        scope = self.txtScope.get_text()
        checkdup = self.chCheckDuplicate.get_active()
        enableipv6 = self.chEnableIPv6.get_active()
        attachable = self.chAttachable.get_active()
        internal = self.chInternal.get_active()
        ingress = self.chIngress.get_active()
        self.lbOptions.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.lbOptions.select_all()
        self.lbOptions.selected_foreach(
            lambda box, row, *user_data:
                self.parse_options(box, row)
        )
        self.lbOptions.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.lbLabels.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.lbLabels.select_all()
        self.lbLabels.selected_foreach(
            lambda box, row, *user_data:
                self.parse_labels(box, row)
        )
        self.lbLabels.set_selection_mode(Gtk.SelectionMode.SINGLE)
        netargs = CreateNetworkArgs(
            name=name,
            driver=driver,
            scope=scope,
            check_duplicate=checkdup,
            enable_ipv6=enableipv6,
            attachable=attachable,
            internal=internal,
            ingress=ingress,
            options=self.options,
            labels=self.labels,
        )
        try:
            self.client.create_network(netargs)
            self.options.clear()
            self.labels.clear()
        except Exception as e:
            notify(summary='Failed to create network', body=f'{e}')
            errLogger.error(e, exc_info=True)
        self.destroy()

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    def parse_options(self, box, row):
        children = row.get_children()
        lbl = children[0]
        txt = lbl.get_text()
        k, v = str(txt).split('=')
        self.options[k] = v
        print(k, v)

    def parse_labels(self, box, row):
        children = row.get_children()
        lbl = children[0]
        txt = lbl.get_text()
        k, v = str(txt).split('=')
        self.labels[k] = v
        print(k, v)

    def show(self):
        super().show()