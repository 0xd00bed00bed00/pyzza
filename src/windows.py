from gi.repository import Gtk
from args import *
from client import Docker
from common import ModelType
from utils import *
from models.helpers import *
from common import APP_VERSION, APP_NAME
from win.browser import BrowserWindow
from win.history import ImageHistoryWindow
from win.save import ImageSaveWindow
from win.export import ContainerExportWindow
from win.load import ImageLoadWindow
from win.top import ContainerTopWindow
from win.inspect import InspectWindow
from win.run import RunContainerOptsWindow
from win.create import ContainerCreateWindow
from win.exec import ExecContainerOptsWindow
from win.pull import ImagePullWindow
from win.build import ImageBuildWindow
from win.term import exec
from win.manage import ManageConnectionsWindow
import threading, json, numpy as np
from config import ConfigManager

@Gtk.Template.from_file('src/ui/pyzza.glade')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'main_window'
    selected_tab = None

    MainBox = Gtk.Template.Child()
    nb1: Gtk.Notebook = Gtk.Template.Child()

    hbMain: Gtk.HeaderBar = Gtk.Template.Child()

    bStopContainer: Gtk.Button = Gtk.Template.Child()
    bRestartContainer: Gtk.Button = Gtk.Template.Child()
    bKillContainer: Gtk.Button = Gtk.Template.Child()
    bExecContainer: Gtk.Button = Gtk.Template.Child()
    bAttachContainer: Gtk.Button = Gtk.Template.Child()
    bInspect: Gtk.Button = Gtk.Template.Child()
    bSuspendContainer: Gtk.Button = Gtk.Template.Child()
    bContainerLogs: Gtk.Button = Gtk.Template.Child()
    bResumeContainer: Gtk.Button = Gtk.Template.Child()
    bContainerTop: Gtk.Button = Gtk.Template.Child()
    bRenameContainer: Gtk.Button = Gtk.Template.Child()
    bExportContainer: Gtk.Button = Gtk.Template.Child()
    bDiffContainer: Gtk.Button = Gtk.Template.Child()
    bBrowse: Gtk.Button = Gtk.Template.Child()
    bStartContainer: Gtk.Button = Gtk.Template.Child()
    bRunContainer: Gtk.Button = Gtk.Template.Child()
    bImageHistory: Gtk.Button = Gtk.Template.Child()
    bSaveImage: Gtk.Button = Gtk.Template.Child()
    bImportImage: Gtk.Button = Gtk.Template.Child()
    bPruneContainers: Gtk.Button = Gtk.Template.Child()
    bPruneImages: Gtk.Button = Gtk.Template.Child()
    bBuildImage: Gtk.Button = Gtk.Template.Child()
    bCreateImage: Gtk.Button = Gtk.Template.Child()
    bCreateContainer: Gtk.Button = Gtk.Template.Child()
    bLoadImage: Gtk.Button = Gtk.Template.Child()
    bSearchRunContainer: Gtk.Button = Gtk.Template.Child()
    bPullImage: Gtk.Button = Gtk.Template.Child()

    dashboardTree: Gtk.TreeView = Gtk.Template.Child()
    dashboardStore: Gtk.ListStore = Gtk.Template.Child()

    containersTree: Gtk.TreeView = Gtk.Template.Child()
    containersStore: Gtk.ListStore = Gtk.Template.Child()

    imagesTree: Gtk.TreeView = Gtk.Template.Child()
    imagesStore: Gtk.ListStore = Gtk.Template.Child()

    volumesTree: Gtk.TreeView = Gtk.Template.Child()
    volumesStore: Gtk.ListStore = Gtk.Template.Child()

    networksTree: Gtk.TreeView = Gtk.Template.Child()
    networksStore: Gtk.ListStore = Gtk.Template.Child()

    searches = None
    searchStore: Gtk.ListStore = Gtk.Template.Child()

    lDashboard: Gtk.Label = Gtk.Template.Child()
    lContainers: Gtk.Label = Gtk.Template.Child()
    lImages: Gtk.Label = Gtk.Template.Child()
    lVolumes: Gtk.Label = Gtk.Template.Child()
    lNetworks: Gtk.Label = Gtk.Template.Child()

    term: Vte.Terminal = Gtk.Template.Child()
    txtSearchImage: Gtk.Entry = Gtk.Template.Child()

    selected_id = None
    selected_name = None
    selection = None

    selected_running_container = None
    selected_container = None
    selected_image = None
    selected_volume = None
    selected_network = None

    dashboard_cursor_moved = False
    containers_cursor_moved = False
    images_cursor_moved = False
    volumes_cursor_moved = False
    networks_cursor_moved = False
    search_cursor_moved = False
    fromSearch = False

    running_containers = None
    containers = None
    images = None
    volumes = None
    networks = None

    config = None

    def __init__(self, application, docker_client=None):
        super().__init__(application=application)

        self.config = ConfigManager.defaultconfig
        assert self.config is not None
        self.dc = docker_client
        if docker_client is None:
            self.dc = Docker()
        self.check_engine()
        the = threading.Thread(target=self.listen_to_events, daemon=True, name='events')
        the.start()

    #region docker event handlers
    def listen_to_events(self):
        events = [
            'create',
            #'destroy',
            'oom',
            'pause',
            'rename',
            'restart',
            'start',
            #'stop',
            'unpause',
            'import',
            'pull',
            'die',
            'delete',
        ]
        self.show_dashboard_actions(False)
        self.show_container_actions(False)
        self.show_image_actions(False)
        for event in self.dc.daemon.events(decode=True, filters={'Type':'container'}):
            #print('event:', event)
            event_type = event['Type']
            event_action = event['Action']
            #print('event_type:', event_type)
            event_notify = event_action in events
            if not event_notify:
                continue
            if event_type == 'container':
                self.listen_to_container_events(event)
            elif event_type == 'image':
                self.listen_to_image_events(event)
            elif event_type == 'volume':
                self.listen_to_volume_events(event)
            elif event_type == 'network':
                self.listen_to_network_events(event)
        
    def listen_to_container_events(self, event=None):
        print(self.running_containers is not None)
        if self.running_containers is None:
            self.running_containers = np.empty((0, 11))
        self.dashboard_cursor_moved = False
        self.containers_cursor_moved = False
        try:
            if event['Action'] == 'start':
                try:
                    id = event['id']
                    rcrow = dashboard_create_row(client=self.dc, id=id)
                    name = event['Actor']['Attributes']['name']
                    if self.containers is None: return
                    arr = self.containers
                    rowcol = np.where(arr==id)
                    [row], [col] = rowcol
                    assert self.containers[row][col] == id
                    tpath = Gtk.TreePath.new_from_indices([row, col])
                    if self.containersStore is not None:
                        if tpath is None: return
                        iter = self.containersStore.get_iter(tpath)
                        nc = self.containersStore.get_n_columns()
                        crow = list(range(nc))
                        crow = self.containersStore.get(iter, *crow)
                        self.containers = np.delete(arr, row, 0)
                        self.containersStore.remove(iter)
                    if self.running_containers is not None:
                        nc = 0 #self.running_containers.get_n_columns()
                        print(rcrow, len(rcrow), nc, len(rcrow)==nc, np.shape(self.running_containers))
                        self.running_containers = np.append(self.running_containers, [rcrow], axis=0)
                        self.dashboardStore.append(rcrow)
                except Exception as e:
                    print('start-error:', e)
                
            elif event['Action'] == 'die':
                try:
                    id = event['id']
                    ccrow = containers_create_row(client=self.dc, id=id)
                    name = event['Actor']['Attributes']['name']
                    if self.running_containers is None: return
                    arr = self.running_containers
                    rowcol = np.where(arr==id)
                    [row], [col] = rowcol
                    assert self.running_containers[row][col] == id
                    tpath = Gtk.TreePath.new_from_indices([row, col])
                    if self.dashboardStore is None: return
                    if tpath is None: return
                    rr = np.array(self.dashboardStore)
                    iter = self.dashboardStore.get_iter(tpath)
                    nc = self.dashboardStore.get_n_columns()
                    crow = list(range(nc))
                    crow = self.dashboardStore.get(iter, *crow)
                    if self.dashboardStore is not None:
                        self.running_containers = np.delete(arr, row, 0)
                        self.dashboardStore.remove(iter)
                    if self.containers is not None:
                        self.containers = np.append(self.containers, [ccrow], axis=0)
                        self.containersStore.append(ccrow)
                except Exception as e:
                    print('die-error:', e)

            elif event['Action'] == 'pause' or event['Action'] == 'unpause':
                act = event['Action']
                try:
                    id = event['id']
                    status = ''
                    if act == 'pause': status = 'paused'
                    else: status = 'running'

                    if self.running_containers is None: return
                    arr = self.running_containers
                    [row], [col] = np.where(arr==id)
                    assert self.running_containers[row][col] == id
                    tpath = Gtk.TreePath.new_from_indices([row, col])
                    if self.dashboardStore is None: return
                    if tpath is None: return
                    iter = self.dashboardStore.get_iter(tpath)
                    self.dashboardStore.set_value(iter, 3, status)
                    self.running_containers[row][3] = status
                except Exception as e:
                    print(f'{act}-error: {e}')
            
            elif event['Action'] == 'create':
                try:
                    id = event['id']
                    name = event['Actor']['Attributes']['name']
                    if self.containers is None: return
                    if self.containersStore is None: return
                    if self.containersStore is not None:
                        crow = containers_create_row(client=self.dc, id=id)
                        self.containersStore.append(crow)
                        self.containers = np.append(self.containers, [crow], axis=0)
                except Exception as e:
                    print('create-error:', e)
        except Exception as e:
            print(f'error: {e}')

    def listen_to_image_events(self, event=None):
        self.images_cursor_moved = False
        act = event['Action']
        if act == 'pull' or act == 'tag':
            try:
                id = event['id']
                if self.images is None: return
                if self.imagesStore is None: return
                cimg = self.images_create_row(id)
                self.imagesStore.append(cimg)
                self.images = np.append(self.images, [cimg], axis=0)
            except Exception as e:
                print(f'{act}-error: {e}')
        
    def listen_to_volume_events(self, event=None):
        self.volumes_cursor_moved = False

    def listen_to_network_events(self, event=None):
        self.networks_cursor_moved = False

    def listen_to_daemon_events(self):
        pass
    #endregion

    #region row creation helpers
    """ def dashboard_create_row(self, id=None, immut=False):
        if id is None: return
        try:
            m = self.dc.get_container(id)
            ago = get_time_ago(m.attrs['Created'])
            name = m.name
            cmd = "{} {}".format(m.attrs['Path'], ' '.join(m.attrs['Args'])).strip()
            status = m.attrs['State']['Status']
            img = m.attrs['Config']['Image']
            hostname = m.attrs['Config']['Hostname']
            ipaddr = m.attrs['NetworkSettings']['IPAddress']
            macaddr = m.attrs['NetworkSettings']['MacAddress']
            r = [
                id,
                name,
                cmd,
                status,
                ago,
                img,
                '',
                '',
                hostname,
                ipaddr,
                macaddr,
            ]
            if immut: return tuple(r)
            return r
        except Exception as e:
            print('[dashboard_create_row] error:', e) """
    
    """ def containers_create_row(self, id=None, immut=False):
        if id is None: return
        try:
            m = self.dc.get_container(id)
            ago = get_time_ago(m.attrs['Created'])
            name = m.name
            cmd = "{} {}".format(m.attrs['Path'], ' '.join(m.attrs['Args'])).strip()
            status = m.attrs['State']['Status']
            img = m.attrs['Config']['Image']
            hostname = m.attrs['Config']['Hostname']
            ipaddr = m.attrs['NetworkSettings']['IPAddress']
            macaddr = m.attrs['NetworkSettings']['MacAddress']
            r = [
                m.id,
                name,
                cmd,
                status,
                ago,
                img,
                hostname,
                ipaddr,
                macaddr,
            ]
            if immut: return tuple(r)
            return r
        except:
            print('[containers_create_row] error') """
    
    """ def images_create_row(self, id=None, immut=False):
        try:
            m = self.dc.get_image(id)
            ago = get_time_ago(m.attrs['Created'])
            size = pretty_size(m.attrs['Size'])
            vsize = pretty_size(m.attrs['VirtualSize'])
            r = [
                id,
                len(m.tags)>0 and m.tags[0].split(':')[0] or '<none>',
                ago,
                size,
                vsize,
            ]
            if immut: return tuple(r)
            return r
        except Exception as e:
            print('[images_create_row] error:', e) """

    """ def volumes_create_row(self, id=None, immut=False):
        try:
            v = self.dc.get_volume(id)
            ago = get_time_ago(v.attrs['CreatedAt'], ms=False)
            r = [
                id,
                v.attrs['Name'],
                ago,
                v.attrs['Mountpoint']
            ]
            if immut: return tuple(r)
            return r
        except Exception as e:
            print('[volumes_create_row] error:', e) """
    
    """ def networks_create_row(self, id=None, immut=False):
        try:
            n = self.dc.get_network(id)
            ago = get_time_ago(n.attrs['Created'])
            r = [
                id,
                n.attrs['Name'],
                ago,
                ':80/tcp',
            ]
            if immut: return tuple(r)
            return r
        except Exception as e:
            print('[networks_create_row] error:', e) """
    #endregion

    #region class methods
    def present(self):
        assert self.nb1 is not None

        self.selected_tab = 0
        self.nb1.set_current_page(self.selected_tab)
        self.show_dashboard()
        self.show_dashboard_actions(False)
        self.show_container_actions(False)
        self.show_image_actions(False)
        self.show_volume_actions(False)
        self.show_network_actions(False)
        self.show_search_actions(False)

        title = APP_NAME
        self.hbMain.set_title(title)
        self.hbMain.set_subtitle(APP_VERSION)
        super().present()

    def check_engine(self):
        ping = self.dc.daemon.ping()
        info = self.dc.daemon.info()
        version = self.dc.daemon.version()
        print('check:', ping)

    def vis(self, vis=True, *widgets):
        if widgets is None or len(widgets)==0:
            return
        for w in widgets:
            w.hide()
            if vis:
                w.show()
            w.set_visible(vis)

    #endregion

    #region show pages
    def show_dashboard(self, skip=False):
        store = self.dashboardStore
        store.clear()
        
        if not skip and self.running_containers is not None:
            print('old data')
            for c in self.running_containers.tolist():
                store.append(c)
            return

        runc = list()
        self.running_containers = np.empty((0, 11))
        for c in self.dc.list_containers():
            runc.append(c)
            store.append(c)
        if len(runc) > 0:            
            self.running_containers = np.array(runc)

        ld = len(self.running_containers)
        self.lDashboard.set_text("running ({})".format(ld))

        self.show_dashboard_actions()

    def show_containers(self, skip=False):
        store = self.containersStore
        store.clear()

        if not skip and self.containers is not None:
            for c in self.containers.tolist():
                store.append(c)
            return

        ccon = list()
        for c, cont, cc in self.dc.list_containers_all():
            ccon.append(c)
            store.append(c)
        self.containers = np.array(ccon)
        lc = len(self.containers)

        self.lContainers.set_text("containers ({})".format(lc))
        self.show_container_actions()

    def show_images(self, skip=False):
        store = self.imagesStore
        store.clear()

        if not skip and self.images is not None:
            for i in self.images.tolist():
                store.append(i)
            return

        imgs = list()
        for i in self.dc.list_images():
            imgs.append(i)
            store.append(i)
        self.images = np.array(imgs)

        li = len(self.images)
        self.lImages.set_text("images ({})".format(li))
        self.show_image_actions()

    def show_volumes(self, skip=False):
        store = self.volumesStore
        store.clear()

        if not skip and self.volumes is not None:
            for v in self.volumes.tolist():
                store.append(v)
            return
        
        vols = list()
        for v in self.dc.list_volumes():
            vols.append(v)
            store.append(v)
        self.volumes = np.array(vols)

        lv = len(self.volumes)
        self.lVolumes.set_text("volumes ({})".format(lv))
        self.show_volume_actions()

    def show_networks(self, skip=False):
        store = self.networksStore
        store.clear()

        if not skip and self.networks is not None:
            for n in self.networks.tolist():
                store.append(n)
            return
        
        nets = list()
        for n in self.dc.list_networks():
            nets.append(n)
            store.append(n)
        self.networks = np.array(nets)
        
        ln = len(self.networks)
        self.lNetworks.set_text("networks ({})".format(ln))
        self.show_network_actions()

    def show_term(self):
        if self.term.get_pty() is None:
            shell = os.environ.get('SHELL')
            spawn_pty(self.term, [shell], [], None)

    #endregion

    #region show actions
    def show_container_actions(self, vis=True):
        bstart = self.bStartContainer
        binspect = self.bInspect
        blogs = self.bContainerLogs
        brename = self.bRenameContainer
        bexport = self.bExportContainer

        if vis:
            self.show_dashboard_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
        self.vis(vis, bstart, binspect, blogs, brename, bexport)

    def show_dashboard_actions(self, vis=True, status=None):
        bstop = self.bStopContainer
        brestart = self.bRestartContainer
        bkill = self.bKillContainer
        bexec = self.bExecContainer
        battach = self.bAttachContainer
        binspect = self.bInspect
        bsuspend = self.bSuspendContainer
        blogs = self.bContainerLogs
        bresume = self.bResumeContainer
        btop = self.bContainerTop
        brename = self.bRenameContainer
        bexport = self.bExportContainer
        bdiff = self.bDiffContainer
        bbrowse = self.bBrowse

        if vis:
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
            self.show_search_actions(False)
        self.vis(vis, bstop, brestart, bkill, bexec, battach, binspect, bsuspend, blogs, bresume, btop, brename, bexport, bdiff, bbrowse)

        if status == 'running':
            self.vis(False, bresume)
        elif status == 'paused':
            self.vis(False, bsuspend, bkill, bexec, battach, brestart, bstop)

    def show_image_actions(self, vis=True):
        brun = self.bRunContainer
        binspect = self.bInspect
        bhistory = self.bImageHistory
        bsave = self.bSaveImage

        if vis:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
            self.show_search_actions(False)
        self.vis(vis, brun, binspect, bhistory, bsave)

    def show_daemon_actions(self):
        pass
    def show_volume_actions(self, vis=True):
        binspect = self.bInspect

        binspect.hide()
        if vis:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_network_actions(False)
            self.show_search_actions(False)
            binspect.show()
        binspect.set_visible(vis)

    def show_network_actions(self, vis=True):
        binspect = self.bInspect
        binspect.hide()

        if vis:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_search_actions(False)
            binspect.show()
        binspect.set_visible(vis)
        
    def show_global_actions(self, vis=True):
        bimportimg = self.bImportImage
        bprunecon = self.bPruneContainers
        bpruneimg = self.bPruneImages
        bbuildimg = self.bBuildImage
        bcreateimg = self.bCreateImage
        bcreatecon = self.bCreateContainer
        bload = self.bLoadImage

        """ if vis:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
            self.show_search_actions(False) """
        self.vis(True, bimportimg, bprunecon, bpruneimg, bbuildimg, bcreateimg, bcreatecon, bload)

    def show_search_actions(self, vis=True):
        brun = self.bSearchRunContainer
        bpull = self.bPullImage

        if vis:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
        self.vis(vis, brun, bpull)

    #endregion

    #region selection handlers
    #region dashboard selection handlers
    @Gtk.Template.Callback()
    def dashboardTree_row_activated_cb(self, a, b, c):
        self.dashboard_select(a)

    @Gtk.Template.Callback()
    def dashboardTree_move_cursor_cb(self, a, b, c):
        self.dashboard_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    @Gtk.Template.Callback()
    def dashboardTree_cursor_changed_cb(self, a):
        if self.running_containers is not None and self.dashboard_cursor_moved:
            self.dashboard_select(a)

    @Gtk.Template.Callback()
    def dashboardStore_row_deleted_cb(self, a, b):
        if self.running_containers is None: return
        d1, d2 = np.shape(self.running_containers)
        self.lDashboard.set_text(f'running ({d1})')

    @Gtk.Template.Callback()
    def dashboardStore_row_inserted_cb(self, a, b, c):
        if self.running_containers is None: return
        d1, d2 = np.shape(self.running_containers)
        self.lDashboard.set_text(f'running ({d1})')

    def dashboard_select(self, a):
        sel = a.get_selection()
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        if rpath is None: return
        if len(rpath)==0: return
        row = rpath[0]
        index = row.get_indices()[0]
        container = self.running_containers[index]
        self.selected_id = container[0]
        self.selected_name = container[1]
        if iter is not None:
            name = model.get_value(iter, 1)
            con = self.dc.inspect_container(name)
            self.selected_running_container = (container, con)
            self.selection = (index, iter)
        status = container[3]
        self.show_dashboard_actions(True, status=status)
    #endregion
    
    #region container selection handlers
    @Gtk.Template.Callback()
    def containersTree_row_activated_cb(self, a, b, c):
        self.container_select(a)

    @Gtk.Template.Callback()
    def containersTree_move_cursor_cb(self, a, b, c):
        self.containers_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    @Gtk.Template.Callback()
    def containersTree_cursor_changed_cb(self, a):
        if self.containers is not None and self.containers_cursor_moved:
            self.container_select(a)

    @Gtk.Template.Callback()
    def containersStore_row_deleted_cb(self, a, b):
        if self.containers is None: return
        d1, d2 = np.shape(self.containers) #len(self.containers)
        self.lContainers.set_text(f'containers ({d1})')

    @Gtk.Template.Callback()
    def containersStore_row_inserted_cb(self, a, b, c):
        if self.containers is None: return
        d1, d2 = np.shape(self.containers) #len(self.containers)
        self.lContainers.set_text(f'containers ({d1})')

    def container_select(self, a):
        sel = a.get_selection()
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        if rpath is None: return
        if len(rpath)==0: return
        row = rpath[0]
        index = row.get_indices()[0]
        container = self.containers[index]
        self.selected_id = container[0]
        self.selected_name = container[1]
        if iter is not None:
            id = model.get_value(iter, 0)
            #print('model2: ', id)
            con = self.dc.inspect_container(id)
            self.selected_container = (container, con)
            self.selection = (index, iter)
        self.show_container_actions(True)
    #endregion

    #region image selection handlers
    @Gtk.Template.Callback()
    def imagesTree_row_activated_cb(self, a, b, c):
        self.image_select(a)

    @Gtk.Template.Callback()
    def imagesTree_move_cursor_cb(self, a, b, c):
        self.images_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    @Gtk.Template.Callback()
    def imagesTree_cursor_changed_cb(self, a):
        if self.images is not None and self.images_cursor_moved: self.image_select(a)

    @Gtk.Template.Callback()
    def imagesStore_row_deleted_cb(self, a, b):
        if self.images is None: return
        d1, d2 = np.shape(self.images) #len(self.images)
        self.lImages.set_text(f'images ({d1})')

    @Gtk.Template.Callback()
    def imagesStore_row_inserted_cb(self, a, b, c):
        if self.images is None: return
        d1, d2 = np.shape(self.images) #len(self.images)
        self.lImages.set_text(f'images ({d1})')
    
    def image_select(self, a):
        sel = a.get_selection()
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        if rpath is None: return
        if len(rpath)==0: return
        row = rpath[0]
        index = row.get_indices()[0]
        image = self.images[index]
        self.selected_id = image[0]
        self.selected_name = image[1]
        if iter is not None:
            id = model.get_value(iter, 0)
            img = self.dc.inspect_image(id)
            self.selected_image = (image, img)
            self.selection = (index, iter)
        self.show_image_actions(True)
    #endregion

    #region volume selection handlers
    @Gtk.Template.Callback()
    def volumesTree_cursor_changed_cb(self, a):
        if self.volumes is not None and self.volumes_cursor_moved:
            self.volume_select(a)

    @Gtk.Template.Callback()
    def volumesTree_row_activated_cb(self, a, b, c):
        self.volume_select(a)

    @Gtk.Template.Callback()
    def volumesTree_move_cursor_cb(self, a, b, c):
        self.volumes_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    @Gtk.Template.Callback()
    def volumesStore_row_deleted_cb(self, a, b):
        if self.volumes is None: return
        d1, d2 = np.shape(self.volumes) #len(self.volumes)
        self.lVolumes.set_text(f'volumes ({d1})')

    @Gtk.Template.Callback()
    def volumesStore_row_inserted_cb(self, a, b, c):
        if self.volumes is None: return
        d1, d2 = np.shape(self.volumes) #len(self.volumes)
        self.lVolumes.set_text(f'volumes ({d1})')

    def volume_select(self, a):
        sel = a.get_selection()
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        if rpath is None: return
        if len(rpath)==0: return
        row = rpath[0]
        index = row.get_indices()[0]
        volume = self.volumes[index]
        self.selected_id = volume[0]
        self.selected_name = volume[1]
        if iter is not None:
            id = model.get_value(iter, 0)
            vol = self.dc.inspect_volume(id)
            self.selected_volume = (volume, vol)
            self.selection = (index, iter)
        self.show_volume_actions(True)
    #endregion

    #region network selection handlers
    @Gtk.Template.Callback()
    def networksTree_row_activated_cb(self, a, b, c):
        print('networksTree_row_activated_cb')
        self.network_select(a)

    @Gtk.Template.Callback()
    def networksTree_move_cursor_cb(self, a, b, c):
        self.networks_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES
    
    @Gtk.Template.Callback()
    def networksTree_cursor_changed_cb(self, a):
        if self.networks is not None and self.networks_cursor_moved:
            self.network_select(a)

    @Gtk.Template.Callback()
    def networksStore_row_deleted_cb(self, a, b):
        if self.networks is None: return
        d1, d2 = np.shape(self.networks) #len(self.networks)
        self.lNetworks.set_text(f'networks ({d1})')

    @Gtk.Template.Callback()
    def networksStore_row_inserted_cb(self, a, b, c):
        if self.networks is None: return
        d1, d2 = np.shape(self.networks) #len(self.networks)
        self.lNetworks.set_text(f'networks ({d1})')

    def network_select(self, a):
        sel = a.get_selection()
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        if rpath is None: return
        if len(rpath)==0: return
        row = rpath[0]
        index = row.get_indices()[0]
        network = self.networks[index]
        self.selected_id = network[0]
        self.selected_name = network[1]
        if iter is not None:
            id = model.get_value(iter, 0)
            net = self.dc.inspect_network(id)
            self.selected_network = (network, net)
            self.selection = (index, iter)
        self.show_network_actions(True)
    #endregion

    #region search selection handlers
    @Gtk.Template.Callback()
    def searchTree_row_activated_cb(self, a, b, c):
        print('searchTree_row_activated_cb')
        self.search_select(a)

    @Gtk.Template.Callback()
    def searchTree_move_cursor_cb(self, a, b, c):
        print('searchTree_move_cursor_cb')
        self.search_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    @Gtk.Template.Callback()
    def searchTree_cursor_changed_cb(self, a):
        print('searchTree_cursor_changed_cb')
        if self.searches is not None and self.search_cursor_moved:
            self.search_select(a)

    @Gtk.Template.Callback()
    def searchStore_row_deleted_cb(self, a):
        pass

    @Gtk.Template.Callback()
    def searchStore_row_inserted_cb(self, a, b, c):
        if self.searches is None: return
        d1, d2 = np.shape(self.search)
        self.lSearch.set_text(f'search ({d1})')

    def search_select(self, a):
        sel = a.get_selection()
        print(sel)
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        if rpath is None: return
        if len(rpath)==0: return
        row = rpath[0]
        index = row.get_indices()[0]
        search = self.searches[index]
        self.selected_name = search[0]
        if iter is not None:
            name = model.get_value(iter, 0)
            self.selection = (index, iter)
            print(name)
        self.show_search_actions(True)
    #endregion
    #endregion

    #region action callbacks
    @Gtk.Template.Callback()
    def nb1_switch_page_cb(self, a, b, index):
        self.selected_tab = index
        if index == 0:
            self.show_dashboard()
            self.show_dashboard_actions(False)
        elif index == 1:
            self.show_containers()
            self.show_container_actions(False)
        elif index == 2:
            self.show_images()
            self.show_image_actions(False)
        elif index == 3:
            self.show_volumes()
            self.show_volume_actions(False)
        elif index == 4:
            self.show_networks()
            self.show_network_actions(False)
        elif index == 5:
            self.show_term()
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)
        elif index == 6:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)

    @Gtk.Template.Callback()
    def bExecContainer_clicked_cb(self, args):
        opts = ExecContainerOptsWindow(container=self.selected_running_container)
        opts.show()

    @Gtk.Template.Callback()
    def bStopContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        id = self.selected_id
        th = threading.Thread(target=self.dc.stop_container, args=[id], daemon=True)
        th.start()

    @Gtk.Template.Callback()
    def bStartContainer_clicked_cb(self, args):
        self.show_container_actions(False)
        container, c = self.selected_container
        id = self.selected_id
        name = self.selected_name
        def start(*args):
            try:
                self.dc.start_container(*args)
            except Exception as exc:
                print(type(exc))
                print(vars(exc))
                notify(summary=f'Error on {name or id[:16]}', body=exc.explanation)
        th = threading.Thread(target=start, args=[id], daemon=True)
        th.start()

    @Gtk.Template.Callback()
    def bRestartContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        id = self.selected_id
        th = threading.Thread(target=self.dc.restart_container, args=[id], daemon=True)
        th.start()

    @Gtk.Template.Callback()
    def bSuspendContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        id = self.selected_id
        th = threading.Thread(target=self.dc.suspend_container, args=[id], daemon=True)
        th.start()

    @Gtk.Template.Callback()
    def bResumeContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        id = self.selected_id
        th = threading.Thread(target=self.dc.resume_container, args=[id], daemon=True)
        th.start()

    @Gtk.Template.Callback()
    def bInspect_clicked_cb(self, args):
        model = ''
        if self.selected_tab == 0 or self.selected_tab == 1:
            model = ModelType.CONTAINER
        elif self.selected_tab == 2:
            model = ModelType.IMAGE
        elif self.selected_tab == 3:
            model = ModelType.VOLUME
        elif self.selected_tab == 4:
            model = ModelType.NETWORK
        if self.selected_id is not None:
            d = self.dc.inspect(self.selected_id, model)
        insp = InspectWindow(name=self.selected_name, data=json.dumps(d, sort_keys=True, indent=4))
        insp.show()

    @Gtk.Template.Callback()
    def bContainerLogs_clicked_cb(self, args):
        id = self.selected_id
        name = self.selected_name
        exec(name, argv=['docker', 'logs', '-t', '-f', '--details', '--tail', 'all', id])

    @Gtk.Template.Callback()
    def bKillContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        self.dc.kill_container(self.selected_id)

    @Gtk.Template.Callback()
    def bRunContainer_clicked_cb(self, args):
        (image, img) = self.selected_image
        cmd = ' '.join(img['Config']['Cmd'])
        opts = RunContainerOptsWindow(client=self.dc, image_name=image[1], cmd=cmd, from_search=self.fromSearch)
        opts.show()

    @Gtk.Template.Callback()
    def bBrowse_clicked_cb(self, args):
        browser = BrowserWindow(self.selected_running_container)
        th = threading.Thread(target=browser.show, daemon=True)
        th.start()

    @Gtk.Template.Callback()
    def bAttachContainer_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def tbPullImage_clicked_cb(self, args):
        self.bPullImage_clicked_cb(args)

    @Gtk.Template.Callback()
    def bPullImage_clicked_cb(self, args):
        pull = ImagePullWindow()
        pull.show()

    @Gtk.Template.Callback()
    def tbBuildImage_clicked_cb(self, args):
        self.bBuildImage_clicked_cb(args)

    @Gtk.Template.Callback()
    def bBuildImage_clicked_cb(self, args):
        build = ImageBuildWindow()
        build.show()

    @Gtk.Template.Callback()
    def tbImportImage_clicked_cb(self, args):
        self.bImportImage_clicked_cb(args)

    @Gtk.Template.Callback()
    def bImportImage_clicked_cb(self, args):
        impimg = ImageLoadWindow()
        impimg.show()
    
    @Gtk.Template.Callback()
    def bContainerTop_clicked_cb(self, args):
        top = ContainerTopWindow(id=self.selected_id, name=self.selected_name, client=self.dc)
        top.show()
    
    @Gtk.Template.Callback()
    def tbCreateContainer_clicked_cb(self, args):
        self.bCreateContainer_clicked_cb(args)

    @Gtk.Template.Callback()
    def bCreateContainer_clicked_cb(self, args):
        ccreate = ContainerCreateWindow(image=self.selected_name)
        ccreate.show()

    @Gtk.Template.Callback()
    def bRenameContainer_clicked_cb(self, args):
        print("coming soon")
    
    @Gtk.Template.Callback()
    def bExportContainer_clicked_cb(self, args):
        exp = ContainerExportWindow(self.selected_id)
        exp.show()

    @Gtk.Template.Callback()
    def bImageHistory_clicked_cb(self, args):
        hist = ImageHistoryWindow(id=self.selected_id, name=self.selected_name)
        hist.show()
    
    @Gtk.Template.Callback()
    def bSearch_clicked_cb(self, args):
        term = self.txtSearchImage.get_text()
        res = self.dc.search_image(term)
        self.searchStore.clear()
        imgs = list()
        for r in res:
            row = [
                r['name'],
                r['description'],
                r['star_count'],
                r['is_official'],
                r['is_automated'],
            ]
            self.searchStore.append(row)
            imgs.append(row)
        self.searches = np.array(imgs)

    @Gtk.Template.Callback()
    def bPruneContainers_clicked_cb(self, args):
        pruned = self.dc.prune_containers()
        print(pruned)

    @Gtk.Template.Callback()
    def bPruneImages_clicked_cb(self, args):
        pruned = self.dc.prune_images()
        print(pruned)

    @Gtk.Template.Callback()
    def bDiffContainer_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bSaveImage_clicked_cb(self, args):
        imgexp = ImageSaveWindow(name=self.selected_name)
        imgexp.show()

    @Gtk.Template.Callback()
    def bSearchRunContainer_clicked_cb(self, args):
        print(self.selected_name, self.fromSearch)

    @Gtk.Template.Callback()
    def bLoadImage_clicked_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def bSettings_clicked_cb(self, args):
        manage = ManageConnectionsWindow()
        manage.show()

    #endregion
