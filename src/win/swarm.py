from gi.repository import Gtk, GLib
from client import Docker
from utils import ee
from config import errLogger, debugLogger

@Gtk.Template.from_file('src/ui/swarm.glade')
class ManageSwarmWindow(Gtk.Window):
    __gtype_name__ = 'wSwarm'

    nbSwarm = Gtk.Template.Child()
    configsTree = Gtk.Template.Child()
    nodesTree = Gtk.Template.Child()
    pluginsTree = Gtk.Template.Child()
    secretsTree = Gtk.Template.Child()
    servicesTree = Gtk.Template.Child()

    lsConfigs = Gtk.Template.Child()
    lsNodes = Gtk.Template.Child()
    lsPlugins = Gtk.Template.Child()
    lsSecrets = Gtk.Template.Child()
    lsServices = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client
        ee.emit('test-data', 'hello test-data')

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bNewConfig_clicked_cb(self, args):
        nconf = NewConfigWindow(client=self.client)
        nconf.show()

    @Gtk.Template.Callback()
    def bInstallPlugin_clicked_cb(self, args):
        install = InstallPluginWindow(client=self.client)
        install.show()

    @Gtk.Template.Callback()
    def bNewSecret_clicked_cb(self, args):
        nsecret = NewSecretWindow(client=self.client)
        nsecret.show()

    @Gtk.Template.Callback()
    def bNewService_clicked_cb(self, args):
        nservice = NewServiceWindow(client=self.client)
        nservice.show()

    @Gtk.Template.Callback()
    def bLeaveSwarm_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bJoinSwarm_clicked_cb(self, args):
        join = JoinSwarmWindow(client=self.client)
        join.show()

    @Gtk.Template.Callback()
    def bInitSwarm_clicked_cb(self, args):
        init = InitSwarmWindow(client=self.client)
        init.show()

    @Gtk.Template.Callback()
    def bUnlockSwarm_clicked_cb(self, args):
        unlock = UnlockSwarmWindow(client=self.client)
        unlock.show()

@Gtk.Template.from_file('src/ui/init_swarm.glade')
class InitSwarmWindow(Gtk.Window):
    __gtype_name__ = 'wInitSwarm'

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bInit_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bAddLabel_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bRemLabel_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bAddExternalCA_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bRemExternalCA_clicked_cb(self, args):
        pass

@Gtk.Template.from_file('src/ui/join_swarm.glade')
class JoinSwarmWindow(Gtk.Window):
    __gtype_name__ = 'wJoinSwarm'

    txtRemoteAddrs = Gtk.Template.Child()
    txtJoinToken = Gtk.Template.Child()
    txtListenAddr = Gtk.Template.Child()
    txtAdvertiseAddr = Gtk.Template.Child()
    txtDataPathAddr = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bJoin_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

@Gtk.Template.from_file('src/ui/unlock_swarm.glade')
class UnlockSwarmWindow(Gtk.Window):
    __gtype_name__ = 'wUnlockSwarm'

    txtKey = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bUnlock_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

@Gtk.Template.from_file('src/ui/new_config.glade')
class NewConfigWindow(Gtk.Window):
    __gtype_name__ = 'wNewSwarmConfig'

    txtConfigName = Gtk.Template.Child()
    txtLabel = Gtk.Template.Child()
    fcbConfigData = Gtk.Template.Child()
    lbLabels = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bAddLabel_clicked_cb(self, args):
        lbl = self.txtLabel.get_text()
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
        self.txtLabel.set_text('')

    @Gtk.Template.Callback()
    def bRemoveLabel_clicked_cb(self, args):
        row = self.lbLabels.get_selected_row()
        if row is not None:
            row.destroy()

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

@Gtk.Template.from_file('src/ui/install_plugin.glade')
class InstallPluginWindow(Gtk.Window):
    __gtype_name__ = 'wInstallPlugin'

    txtRemoteName = Gtk.Template.Child()
    txtLocalName = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bInstall_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

@Gtk.Template.from_file('src/ui/new_secret.glade')
class NewSecretWindow(Gtk.Window):
    __gtype_name__ = 'wNewSecret'

    txtName = Gtk.Template.Child()
    txtData = Gtk.Template.Child()
    txtDriver = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

@Gtk.Template.from_file('src/ui/new_service.glade')
class NewServiceWindow(Gtk.Window):
    __gtype_name__ = 'wNewService'

    txtName = Gtk.Template.Child()
    txtImage = Gtk.Template.Child()
    txtCommand = Gtk.Template.Child()
    txtArgs = Gtk.Template.Child()
    txtHostname = Gtk.Template.Child()
    txtEnv = Gtk.Template.Child()
    txtLabel = Gtk.Template.Child()
    txtContainerLabel = Gtk.Template.Child()
    txtNetworks = Gtk.Template.Child()
    txtUser = Gtk.Template.Child()
    txtWorkDir = Gtk.Template.Child()
    txtHost = Gtk.Template.Child()
    txtMount = Gtk.Template.Child()

    chkTty = Gtk.Template.Child()
    chkReadonly = Gtk.Template.Child()
    chkStdin = Gtk.Template.Child()

    lbEnv = Gtk.Template.Child()
    lbLabels = Gtk.Template.Child()
    lbContainerLabels = Gtk.Template.Child()
    lbHosts = Gtk.Template.Child()

    bSave = Gtk.Template.Child()
    bCancel = Gtk.Template.Child()
    bResources = Gtk.Template.Child()
    bAddEnv = Gtk.Template.Child()
    bRemEnv = Gtk.Template.Child()
    bAddLbl = Gtk.Template.Child()
    bRemLbl = Gtk.Template.Child()
    bAddCLbl = Gtk.Template.Child()
    bRemCLbl = Gtk.Template.Child()
    bAddHost = Gtk.Template.Child()
    bRemHost = Gtk.Template.Child()
    bAddMount = Gtk.Template.Child()
    bRemMount = Gtk.Template.Child()
    bAddConfig = Gtk.Template.Child()
    bRemConfig = Gtk.Template.Child()
    bAddSecret = Gtk.Template.Child()
    bRemSecret = Gtk.Template.Child()

    configsTree = Gtk.Template.Child()
    secretsTree = Gtk.Template.Child()

    lsConfigs = Gtk.Template.Child()
    lsSecrets = Gtk.Template.Child()

    def __init__(self, client: Docker=None):
        super().__init__()
        self.client = client

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bAddEnv_clicked_cb(self, args):
        env = self.txtEnv.get_text()
        if env == '':
            return
        row = Gtk.ListBoxRow()
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(env)
        txt.set_visible(True)
        row.add(txt)
        self.lbEnv.insert(row, -1)
        self.txtEnv.set_text('')

    @Gtk.Template.Callback()
    def bRemEnv_clicked_cb(self, args):
        row = self.lbEnv.get_selected_row()
        if row is not None:
            row.destroy()

    @Gtk.Template.Callback()
    def bAddLbl_clicked_cb(self, args):
        lbl = self.txtLabel.get_text()
        if lbl == '':
            return
        row = Gtk.ListBoxRow()
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(lbl)
        txt.set_visible(True)
        row.add(txt)
        self.lbEnv.insert(row, -1)
        self.txtLabel.set_text('')

    @Gtk.Template.Callback()
    def bRemLbl_clicked_cb(self, args):
        row = self.lbLabels.get_selected_row()
        if row is not None:
            row.destroy()

    @Gtk.Template.Callback()
    def bAddCLbl_clicked_cb(self, args):
        clbl = self.txtContainerLabel.get_text()
        if clbl == '':
            return
        row = Gtk.ListBoxRow()
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(clbl)
        txt.set_visible(True)
        row.add(txt)
        self.lbEnv.insert(row, -1)
        self.txtContainerLabel.set_text('')

    @Gtk.Template.Callback()
    def bRemCLbl_clicked_cb(self, args):
        row = self.lbContainerLabels.get_selected_row()
        if row is not None:
            row.destroy()

    @Gtk.Template.Callback()
    def bAddHost_clicked_cb(self, args):
        host = self.txtHost.get_text()
        if host == '':
            return
        row = Gtk.ListBoxRow()
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(host)
        txt.set_visible(True)
        row.add(txt)
        self.lbHosts.insert(row, -1)
        self.txtHost.set_text('')

    @Gtk.Template.Callback()
    def bRemHost_clicked_cb(self, args):
        row = self.lbHosts.get_selected_row()
        if row is not None:
            row.destroy()

    @Gtk.Template.Callback()
    def bAddMount_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bRemMount_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bAddConfig_clicked_cb(self, args):
        config = AddConfigSecretWindow()
        config.show()

    @Gtk.Template.Callback()
    def bRemConfig_clicked_cb(self, args):
        selection = self.configsTree.get_selection()
        if selection.count_selected_rows() > 0:
            model, iter = selection.get_selected()
            model.remove(iter)

    @Gtk.Template.Callback()
    def bAddSecret_clicked_cb(self, args):
        secret = AddConfigSecretWindow(issecret=True)
        secret.show()

    @Gtk.Template.Callback()
    def bRemSecret_clicked_cb(self, args):
        selection = self.secretsTree.get_selection()
        if selection.count_selected_rows() > 0:
            model, iter = selection.get_selected()
            model.remove(iter)

    @Gtk.Template.Callback()
    def bResources_clicked_cb(self, args):
        res = ResourcesWindow()
        res.show()

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    @ee.on('config-data')
    def config_cb(data):
        pass

    @ee.on('secret-data')
    def secret_cb(data):
        pass

    @ee.on('resource-data')
    def resource_cb(data):
        pass

@Gtk.Template.from_file('src/ui/config_secret.glade')
class AddConfigSecretWindow(Gtk.Window):
    __gtype_name__ = 'wConfigSecret'

    txtId = Gtk.Template.Child()
    txtName = Gtk.Template.Child()
    txtFilename = Gtk.Template.Child()
    txtUid = Gtk.Template.Child()
    txtGid = Gtk.Template.Child()
    sbMode = Gtk.Template.Child()

    def __init__(self, issecret=False):
        super().__init__()
        self.issecret = issecret

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bOk_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

@Gtk.Template.from_file('src/ui/resources.glade')
class ResourcesWindow(Gtk.Window):
    __gtype_name__ = 'wSwarmResources'

    sbCpuLimit = Gtk.Template.Child()
    sbMemLimit = Gtk.Template.Child()
    sbCpuReservation = Gtk.Template.Child()
    sbMemReservation = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    def show(self):
        super().show()

    @Gtk.Template.Callback()
    def bSet_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()