from gi.repository import Gtk
from config import debugLogger

@Gtk.Template.from_file('src/ui/expose_port.glade')
class ExposePortsWindow(Gtk.Window):
    __gtype_name__ = 'wExposePortOpts'

    hbExposePorts: Gtk.HeaderBar = Gtk.Template.Child()
    txtContainerPort = Gtk.Template.Child()
    cbProtocol = Gtk.Template.Child()
    cbPortType = Gtk.Template.Child()
    txtHostPort = Gtk.Template.Child()
    bExposeSubmit = Gtk.Template.Child()
    bExposeCancel = Gtk.Template.Child()

    lsPortType = Gtk.Template.Child()
    lsProtocol = Gtk.Template.Child()

    def __init__(self, client=None, image_name=None, cb=None):
        super().__init__()
        self.client = client
        self.image = image_name
        self.containerport = None
        self.protocol = None
        self.type = None
        self.hostport = None
        self.cb = cb
        self.exposedPorts = dict()

    def bAddPort_clicked_cb(self, args):
        proto = self.cbProtocol.get_active()
        model = self.cbProtocol.get_model()
        protocol = model[proto][0]
        self.protocol = protocol
        ptype = self.cbPortType.get_active()
        model = self.cbPortType.get_model()
        ptype = model[ptype][0]
        self.type = ptype
        assert self.protocol is not None
        key = self.containerport
        if proto > 0:
            key = f'{self.containerport}/{protocol}'
            #if key not in self.exposedPorts.keys():
        value = f'{ptype}:{self.hostport}'
        if ptype == 'single':
            value = self.hostport
        elif ptype == 'random':
            value = f'{ptype}'
        self.lsPorts.append([
            key,
            value,
        ])
        self.exposedPorts[key] = f'{ptype}:{self.hostport}'

    def present(self):
        self.hbExposePorts.set_subtitle(self.image)

    def bRemovePort_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def txtContainerPort_changed_cb(self, args):
        self.containerport = args.get_text()

    @Gtk.Template.Callback()
    def txtHostPort_changed_cb(self, args):
        self.hostport = args.get_text()

    @Gtk.Template.Callback()
    def cbProtocol_changed_cb(self, args):
        index = self.cbProtocol.get_active()
        model = self.cbProtocol.get_model()
        proto = model[index][0]
        self.protocol = proto
        debugLogger.debug('[proto]: '+proto)

    @Gtk.Template.Callback()
    def cbPortType_changed_cb(self, args):
        index = self.cbPortType.get_active()
        model = self.cbPortType.get_model()
        ptype = model[index][0]
        self.type = ptype
        debugLogger.debug('[ptype]: '+ptype)

    @Gtk.Template.Callback()
    def bExposeSubmit_clicked_cb(self, args):
        proto = self.cbProtocol.get_active()
        model = self.cbProtocol.get_model()
        protocol = model[proto][0]
        ptype = self.cbPortType.get_active()
        model = self.cbPortType.get_model()
        ptype = model[ptype][0]
        key = self.containerport
        if proto > 0:
            key = f'{self.containerport}/{self.protocol}'
        value = f'{ptype}:{self.hostport}'
        #if ptype == 'random':
        #    value = None
        #if ptype == 'multiple':
        #    value = str(value).split(',')
        if self.cb is not None:
            self.cb([key, value])
        self.destroy()

    @Gtk.Template.Callback()
    def bExposeCancel_clicked_cb(self, args):
        self.destroy()