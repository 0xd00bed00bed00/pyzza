from gi.repository import Gtk
from slugify import slugify
from args import RunContanerKwargs
from win.term import exec
from win.expose import ExposePortsWindow
from win.volume import AddVolumeWindow
from config import debugLogger, appLogger, errLogger
from models.helpers import getrowdata
from utils import notify
import threading, re, ipaddress

@Gtk.Template.from_file('src/ui/run_container_opts.glade')
class RunContainerOptsWindow(Gtk.Window):
    __gtype_name__ = 'wRunContainerOpts'

    txtiImageName = Gtk.Template.Child()
    txtiContainerName = Gtk.Template.Child()
    txtiCommand = Gtk.Template.Child()
    txtiWorkingDir = Gtk.Template.Child()
    txtRunContainerUser = Gtk.Template.Child()
    txtRunContainerHostname = Gtk.Template.Child()
    txtNetwork = Gtk.Template.Child()
    txtMacAddress = Gtk.Template.Child()
    txtDevices = Gtk.Template.Child()
    txtEnvironment = Gtk.Template.Child()
    txtHealthcheck = Gtk.Template.Child()
    txtEntrypoint = Gtk.Template.Child()
    txtStopSignal = Gtk.Template.Child()
    txtPlatform = Gtk.Template.Child()
    chRunContainerTty = Gtk.Template.Child()
    chRunContainerStream = Gtk.Template.Child()
    chRunContainerStdout = Gtk.Template.Child()
    chRunContainerStderr = Gtk.Template.Child()
    chRunContainerStdin = Gtk.Template.Child()
    chRunContainerDetach = Gtk.Template.Child()
    chRunContainerPrivileged = Gtk.Template.Child()
    chRunContainerNetDisabled = Gtk.Template.Child()
    chRemove = Gtk.Template.Child()
    chReadonly = Gtk.Template.Child()
    chPublishAllPorts = Gtk.Template.Child()
    chInit = Gtk.Template.Child()
    chAutoRemove = Gtk.Template.Child()
    chOomKillDisable = Gtk.Template.Child()
    bAddPort = Gtk.Template.Child()
    bRemovePort = Gtk.Template.Child()
    portsTree: Gtk.TreeView = Gtk.Template.Child()
    volumesTree: Gtk.TreeView = Gtk.Template.Child()
    lsPorts: Gtk.ListStore = Gtk.Template.Child()
    lsVolumes: Gtk.ListStore = Gtk.Template.Child()

    fromSearch = False
    imageName = None
    containerName = None
    command = None

    def __init__(self, image_name=None, container_name=None, cmd=None, from_search=False, client=None):
        super().__init__()
        self.ports = dict()
        self.volumes = dict()
        self.dc = client
        self.fromSearch = from_search
        self.imageName = image_name
        self.containerName = container_name or image_name
        if not from_search:
            self.command = cmd

    @Gtk.Template.Callback()
    def bRunContainerCancel_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bRunContainerSubmit_clicked_cb(self, args):
        image = self.txtiImageName.get_text()
        if self.fromSearch:
            exec(image, argv=[
                'docker',
                'pull',
                image,
            ])

        container = slugify(self.txtiContainerName.get_text())
        cmd = self.txtiCommand.get_text()
        wdir = self.txtiWorkingDir.get_text()
        tty = self.chRunContainerTty.get_active()
        stream = self.chRunContainerStream.get_active()
        stdout = self.chRunContainerStdout.get_active()
        stderr = self.chRunContainerStderr.get_active()
        stdin = self.chRunContainerStdin.get_active()
        detach = self.chRunContainerDetach.get_active()
        priv = self.chRunContainerPrivileged.get_active()
        netdis = self.chRunContainerNetDisabled.get_active()
        user = self.txtRunContainerUser.get_text()
        host = self.txtRunContainerHostname.get_text()
        remove = self.chRemove.get_active()
        readonly = self.chReadonly.get_active()
        publishall = self.chPublishAllPorts.get_active()
        init = self.chInit.get_active()
        autoremove = self.chAutoRemove.get_active()
        oomkilldisable = self.chOomKillDisable.get_active()
        network = self.txtNetwork.get_text()
        mac = self.txtMacAddress.get_text()
        devices = self.txtDevices.get_text()
        environment = self.txtEnvironment.get_text()
        healthcheck = self.txtHealthcheck.get_text()
        stopsignal = self.txtStopSignal.get_text()
        platform = self.txtPlatform.get_text()
        entrypoint = self.txtEntrypoint.get_text()
        self.lsPorts.foreach(
            lambda model, path, iter, *data:
                self.addports(model, path, iter, *data)
        )
        self.lsVolumes.foreach(
            lambda model, path, iter, *data:
                self.addvolumes(model, path, iter, *data)
        )

        kwargs = RunContanerKwargs(image=image, name=container, command=cmd, working_dir=wdir, tty=tty, stream=stream, stdout=stdout, stderr=stderr, stdin_open=stdin, detach=detach, privileged=priv, network_disabled=netdis, user=user, hostname=host, remove=remove, read_only=readonly, publish_all_ports=publishall, auto_remove=autoremove, init=init, network=network, platform=platform, mac_address=mac, devices=devices, stop_signal=stopsignal)
        '''
        if mac is not None:
            kwargs.mac_address = mac
        if devices is not None:
            kwargs.devices = devices
        if stopsignal != '':
            kwargs.stop_signal = stopsignal
        '''
        if environment != '':
            kwargs.environment = str(environment).split(',')
        if entrypoint != '':
            kwargs.entrypoint = str(entrypoint).split(';')
        if len(self.ports.items()) > 0:
            kwargs.ports = self.ports
        if len(self.volumes.items()) > 0:
            kwargs.volumes = self.volumes
        debugLogger.debug(kwargs.__dict__)
        th = threading.Thread(target=self.dc.run_container, args=[kwargs], daemon=True)
        th.start()
        
        if not self.fromSearch: self.destroy()

    @Gtk.Template.Callback()
    def bAddPort_clicked_cb(self, args):
        #debugLogger.debug(f'[bAddPort_clicked_cb]: {args}')
        exposew = ExposePortsWindow(client=self.dc, image_name=self.imageName, cb=self.expose_cb)
        exposew.show()

    @Gtk.Template.Callback()
    def bAddVolume_clicked_cb(self, args):
        addvol = AddVolumeWindow(image_name=self.imageName, cb=self.addvolume_cb)
        addvol.show()

    @Gtk.Template.Callback()
    def bRemoveVolume_clicked_cb(self, args):
        selection = self.volumesTree.get_selection()
        if selection.count_selected_rows() > 0:
            model, iter = selection.get_selected()
            model.remove(iter)

    @Gtk.Template.Callback()
    def bRemovePort_clicked_cb(self, args):
        #debugLogger.debug(f'[bRemovePort_clicked_cb]: {args}')
        selection = self.portsTree.get_selection()
        if selection.count_selected_rows() > 0:
            model, iter = selection.get_selected()
            model.remove(iter)

    def expose_cb(self, args):
        print('[args]:', args)
        self.lsPorts.append(args)
        self.lsPorts.foreach(lambda model, path, iter, *data:
            print(model.get(iter, *[i for i in range(model.get_n_columns())]))
        )

    def addvolume_cb(self, args):
        print('[args]:', args)
        self.lsVolumes.append([
            args[0],
            args[1]['bind'],
            args[1]['mode'],
        ])
        aa = {
            args[0]: args[1],
        }
        self.lsVolumes.foreach(lambda model, path, iter, *data:
            print(model.get(iter, *[i for i in range(model.get_n_columns())]))
        )

    def addports(self, model, path, iter, *data):
        row = getrowdata(model, iter)
        ptype, value = str(row[1]).split(':')
        self.ports[row[0]] = value
        if ptype == 'single':
            self.ports[row[0]] = int(value)
        elif ptype == 'random':
            self.ports[row[0]] = None
        elif ptype == 'multiple':
            value = str(value).split(',')
            self.ports[row[0]] = value
        elif ptype == 'interface':
            intf = str(value).split(',')
            try:
                ip = intf[0]
                ipaddress.ip_interface(ip)
                value = (ip, int(intf[1]))
                self.ports[row[0]] = value
            except ValueError as ve:
                notify(summary='Error while parsing ip address', body=f'{ve}')
                errLogger.error(ve, exc_info=True)
            

    def addvolumes(self, model, path, iter, *data):
        row = getrowdata(model, iter)
        self.volumes[row[0]] = {
            'bind': row[1],
            'mode': row[2],
        }

    def show(self):
        super().show()
        self.txtiImageName.set_text(self.imageName)
        self.txtiContainerName.set_text(self.containerName)
        self.txtiCommand.set_text(self.command)