import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Vte', '2.91')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GObject, Vte, Notify, Gio, GLib
from args import *
from client import Docker
from utils import *
from windows import *
from common import *
from constants import *
from slugify import slugify
from docker.models import containers, images, volumes, networks, swarm, services, secrets, nodes
import threading, json, numpy as np
from win.run import *
from win.browser import *
from win.exec import *

GObject.type_register(Vte.Terminal)

#UI_FILE = 'pyzza.glade'

class Pyzza(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        Notify.is_initted() or Notify.init('pyzza')
        self.dc = Docker()
        #self.builder = Gtk.Builder()
        #self.builder.add_from_file(UI_FILE)
        #self.builder.connect_signals(self)
        #self.window = self.builder.get_object('main_window')
        #wgterm = Gtk.WindowGroup.new()
        #self.wgterm = wgterm

        self.window = None

        """ self.term = None
        self.selected_running_container = None
        self.selected_container = None
        self.selected_image = None
        self.selected_volume = None
        self.selected_network = None
        self.selected_id = None
        self.selected_name = None
        self.selected_tab = None

        self.containers = None
        self.running_containers = None
        self.images = None
        self.volumes = None
        self.networks = None
        self.searches = None

        self.dashboardStore = None
        self.containersStore = None
        self.imagesStore = None
        self.volumesStore = None
        self.networksStore = None
        self.searchStore = None

        self.selection = None
        self.dashboard_cursor_moved = False
        self.containers_cursor_moved = False
        self.images_cursor_moved = False
        self.volumes_cursor_moved = False
        self.networks_cursor_moved = False
        self.search_cursor_moved = False

        self.saveImageDialog = None
        self.loadImageDialog = None

        self.exportContainer = None
        self.exportContainerBuilder = None

        self.copyFromContainer = None
        self.copyFromContainerBuilder = None

        self.copyToContainer = None
        self.copyToContainerBuilder = None

        self.wCreateContainer = None
        self.wCreateContainerBuilder = None

        self.wBuildImage = None
        self.wBuildImageBuilder = None

        self.wRunOpts = None
        self.wRunOptsBuilder = None

        self.wExecOpts = None
        self.wExecOptsBuilder = None

        self.fromSearch = False """

        #self.check_engine()
        #the = threading.Thread(target=self.listen_to_events, daemon=True, name='events')
        #the.start()

        #main_window = MainWindow()
        #self.window = MainWindow(application=self)

    def do_activate(self):
        self.window = self.window or MainWindow(application=self)
        self.window.present()

    #region exec commands in terminal
    """ def exec(self, title=None, subtitle=None, argv=None, envv=None, callback=None, *cbargs):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wTerm'])
        go = builder.get_object
        wterm = go('wTerm')
        wvterm = go('wvTerm')
        hbterm = go('hbTerm')
        hbterm.set_title(title)
        hbterm.set_subtitle(subtitle)
        spawn_pty(wvterm, argv, envv, callback, *cbargs)
        wterm.show() """
    #endregion

    #region row creation helpers
    def dashboard_create_row(self, id=None, immut=False):
        """ if id is None: return
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
        pass

    def containers_create_row(self, id=None, immut=False):
        """ if id is None: return
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
        pass

    def images_create_row(self, id=None, immut=False):
        #return images_create_row(self.dc, id)
        """ try:
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
        pass

    def volumes_create_row(self, id=None, immut=False):
        #return volumes_create_row(self.dc, id)
        """ try:
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
        pass

    def networks_create_row(self, id=None, immut=False):
        #return networks_create_row(self.dc, id)
        """ try:
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
        pass
    #endregion

    #region class methods
    def ok_cb(self, notification, action, *user_data):
        print('ok_cb:', notification, action, user_data)

    def check_engine(self):
        ping = self.dc.daemon.ping()
        info = self.dc.daemon.info()
        version = self.dc.daemon.version()
        print('check:', ping)

    def notify(self, summary=None, body=None, icon=None, actions=None):
        """ notif = Gio.Notification()
        notif.set_title(summary)
        notif.set_body(body)

        self.send_notification('pyzza', notif) """

        notif = Notify.Notification.new(summary, body, icon)
        notif.set_timeout(Notify.EXPIRES_DEFAULT)
        notif.set_urgency(Notify.Urgency.NORMAL)
        if actions is not None:
            for a in actions:
                id, label, cb, data = a
                notif.add_action(id, label, cb, *data)
        notif.show()

    def ready(self, term, pid, error, *user_data):
        print('ready:', term, pid, error, user_data)

    def start(self):
        nb1 = self.builder.get_object("nb1")
        # nb1.connect('switch-page', self.nb1_switch_page_cb)
        self.selected_tab = 0
        nb1.set_current_page(self.selected_tab)
        self.show_dashboard()
        self.window.show()
        self.show_dashboard_actions(False)
        self.show_container_actions(False)
        self.show_image_actions(False)

        hb = self.go('hbMain')
        title = 'pyzza'
        if check_priv():
            title = f'pyzza [sudo]'
        hb.set_title(title)
        hb.set_subtitle('version 0.1')

        Gtk.main()

    def connect(self, event, handler):
        self.window.connect(event, handler)

    def vis(self, vis=True, *widgets):
        if widgets is None or len(widgets)==0:
            return
        for w in widgets:
            w.hide()
            if vis:
                w.show()
            w.set_visible(vis)

    def go(self, id):
        return self.builder.get_object(id)
    #endregion

    #region docker event listeners
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
        self.dashboard_cursor_moved = False
        self.containers_cursor_moved = False
        try:
            if event['Action'] == 'start':
                try:
                    id = event['id']
                    rcrow = self.dashboard_create_row(id)
                    name = event['Actor']['Attributes']['name']
                    if self.containers is None: return
                    arr = self.containers
                    rowcol = np.where(arr==id)
                    [row], [col] = rowcol
                    assert self.containers[row][col] == id
                    tpath = Gtk.TreePath.new_from_indices([row, col])
                    if self.containersStore is None: return
                    if tpath is None: return
                    iter = self.containersStore.get_iter(tpath)
                    nc = self.containersStore.get_n_columns()
                    crow = list(range(nc))
                    crow = self.containersStore.get(iter, *crow)
                    assert self.containersStore is not None
                    self.containers = np.delete(arr, row, 0)
                    self.containersStore.remove(iter)
                    if self.running_containers is not None:
                        self.running_containers = np.append(self.running_containers, [rcrow], axis=0)
                        self.dashboardStore.append(rcrow)
                except Exception as e:
                    print('start-error:', e)
                
            elif event['Action'] == 'die':
                try:
                    id = event['id']
                    ccrow = self.containers_create_row(id)
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
                        crow = self.containers_create_row(id)
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

    #region item selection handlers
    def dashboardTree_row_activated_cb(self, a, b, c):
        self.dashboard_select(a)

    def dashboardTree_move_cursor_cb(self, a, b, c):
        self.dashboard_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES
            #print('hit!')

    def dashboardTree_cursor_changed_cb(self, a):
        if self.running_containers is not None and self.dashboard_cursor_moved:
            self.dashboard_select(a)

    def dashboardStore_row_deleted_cb(self, a, b):
        if self.running_containers is None: return
        d1, d2 = np.shape(self.running_containers)
        dash = self.go('lDashboard')
        dash.set_text(f'running ({d1})')

    def dashboardStore_row_inserted_cb(self, a, b, c):
        if self.running_containers is None: return
        d1, d2 = np.shape(self.running_containers)
        dash = self.go('lDashboard')
        dash.set_text(f'running ({d1})')

    def dashboard_select(self, a):
        sel = a.get_selection()
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        #print(type(model), type(iter), type(rpath))
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

    def containersTree_row_activated_cb(self, a, b, c):
        self.container_select(a)

    def containersTree_move_cursor_cb(self, a, b, c):
        self.containers_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    def containersTree_cursor_changed_cb(self, a):
        if self.containers is not None and self.containers_cursor_moved:
            self.container_select(a)

    def containersStore_row_deleted_cb(self, a, b):
        if self.containers is None: return
        d1, d2 = np.shape(self.containers) #len(self.containers)
        cont = self.go('lContainers')
        cont.set_text(f'containers ({d1})')

    def containersStore_row_inserted_cb(self, a, b, c):
        if self.containers is None: return
        d1, d2 = np.shape(self.containers) #len(self.containers)
        cont = self.go('lContainers')
        cont.set_text(f'containers ({d1})')

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

    def imagesTree_row_activated_cb(self, a, b, c):
        self.image_select(a)

    def imagesTree_move_cursor_cb(self, a, b, c):
        self.images_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    def imagesTree_cursor_changed_cb(self, a):
        if self.images is not None and self.images_cursor_moved: self.image_select(a)

    def imagesStore_row_deleted_cb(self, a, b):
        if self.images is None: return
        d1, d2 = np.shape(self.images) #len(self.images)
        img = self.go('lImages')
        img.set_text(f'images ({d1})')

    def imagesStore_row_inserted_cb(self, a, b, c):
        if self.images is None: return
        d1, d2 = np.shape(self.images) #len(self.images)
        img = self.go('lImages')
        img.set_text(f'images ({d1})')
    
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

    def volumesTree_cursor_changed_cb(self, a):
        if self.volumes is not None and self.volumes_cursor_moved:
            self.volume_select(a)

    def volumesTree_row_activated_cb(self, a, b, c):
        self.volume_select(a)

    def volumesTree_move_cursor_cb(self, a, b, c):
        self.volumes_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    def volumesStore_row_deleted_cb(self, a, b):
        if self.volumes is None: return
        d1, d2 = np.shape(self.volumes) #len(self.volumes)
        vol = self.go('lVolumes')
        vol.set_text(f'volumes ({d1})')

    def volumesStore_row_inserted_cb(self, a, b, c):
        if self.volumes is None: return
        d1, d2 = np.shape(self.volumes) #len(self.volumes)
        vol = self.go('lVolumes')
        vol.set_text(f'volumes ({d1})')

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

    def networksTree_row_activated_cb(self, a, b, c):
        print('networksTree_row_activated_cb')
        self.network_select(a)

    def networksTree_move_cursor_cb(self, a, b, c):
        self.networks_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES
    
    def networksTree_cursor_changed_cb(self, a):
        if self.networks is not None and self.networks_cursor_moved:
            self.network_select(a)

    def networksStore_row_deleted_cb(self, a, b):
        if self.networks is None: return
        d1, d2 = np.shape(self.networks) #len(self.networks)
        net = self.go('lNetworks')
        net.set_text(f'running ({d1})')

    def networksStore_row_inserted_cb(self, a, b, c):
        if self.networks is None: return
        d1, d2 = np.shape(self.networks) #len(self.networks)
        net = self.go('lNetworks')
        net.set_text(f'running ({d1})')

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

    def searchTree_row_activated_cb(self, a, b, c):
        print('searchTree_row_activated_cb')
        self.search_select(a)

    def searchTree_move_cursor_cb(self, a, b, c):
        print('searchTree_move_cursor_cb')
        self.search_cursor_moved = b == Gtk.MovementStep.DISPLAY_LINES

    def searchTree_cursor_changed_cb(self, a):
        print('searchTree_cursor_changed_cb')
        if self.searches is not None and self.search_cursor_moved:
            self.search_select(a)

    def searchStore_row_deleted_cb(self, a):
        pass

    def searchStore_row_inserted_cb(self, a, b, c):
        if self.searches is None: return
        d1, d2 = np.shape(self.search)
        search = self.go('lSearch')
        search.set_text(f'search ({d1})')

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

    def select(self, a, items, model, selected=None, acts=None, vis=False):
        sel = a.get_selection()
        model, iter = sel.get_selected()
        _, rpath = sel.get_selected_rows()
        if len(rpath)==0: return
        row = rpath[0]
        index = row.get_indices()[0]
        item = items[index]
        id = item[0]
        name = item[1]
        self.selected_id = id
        self.selected_name = name
        if iter is not None:
            #id = model.get_value(iter, 0)
            inspected = self.dc.inspect(id, model)
            selected = (item, inspected)
        if acts is not None: acts(vis)

    def bRefreshData_clicked_cb(self, args):
        tbskipcache = self.go('tbSkipCache')
        skip = tbskipcache.get_active()
        st = self.selected_tab
        if st == 0:
            self.show_dashboard(skip=skip)
            self.show_dashboard_actions(False)
        elif st == 1:
            self.show_containers(skip=skip)
            self.show_container_actions(False)
        elif st == 2:
            self.show_images(skip=skip)
            self.show_image_actions(False)
        elif st == 3:
            self.show_volumes(skip=skip)
            self.show_volume_actions(False)
        elif st == 4:
            self.show_networks(skip=skip)
            self.show_network_actions(False)

    def insert_item(self):
        pass

    def remove_item(self):
        pass
    #endregion

    #region show pages
    def show_dashboard(self, skip=False):
        """ dashboardStore = self.builder.get_object("dashboardStore")
        dashboardStore.clear()
        self.dashboardStore = dashboardStore
        
        if not skip and self.running_containers is not None:
            print('old data')
            for c in self.running_containers.tolist():
                dashboardStore.append(c)
            return

        print('new data')
        runc = list()
        for c in self.dc.list_containers():
            runc.append(c)
            dashboardStore.append(c)
        self.running_containers = np.array(runc)
        self.dashboardStore = dashboardStore

        ld = len(self.running_containers)
        ldashboard = self.go('lDashboard')
        ldashboard.set_text("running ({})".format(ld))

        self.show_dashboard_actions() """
        pass

    def show_containers(self, skip=False):
        """ containersStore = self.builder.get_object("containersStore")
        containersStore.clear()
        self.containersStore = containersStore

        if not skip and self.containers is not None:
            for c in self.containers.tolist():
                containersStore.append(c)
            return

        ccon = list()
        for c, cont, cc in self.dc.list_containers_all():
            ccon.append(c)
            containersStore.append(c)
        self.containers = np.array(ccon)
        self.containersStore = containersStore
        lc = len(self.containers)

        lcontainers = self.go('lContainers')
        lcontainers.set_text("containers ({})".format(lc))
        self.show_container_actions() """
        pass

    def show_images(self, skip=False):
        """ imagesStore = self.builder.get_object("imagesStore")
        imagesStore.clear()
        self.imagesStore = imagesStore

        if not skip and self.images is not None:
            for i in self.images.tolist():
                imagesStore.append(i)
            return

        imgs = list()
        for i in self.dc.list_images():
            imgs.append(i)
            imagesStore.append(i)
        self.images = np.array(imgs)
        self.imagesStore = imagesStore

        li = len(self.images)
        limages = self.go('lImages')
        limages.set_text("images ({})".format(li))
        self.show_image_actions() """
        pass

    def show_volumes(self, skip=False):
        """ volumesStore = self.go('volumesStore')
        volumesStore.clear()
        self.volumesStore = volumesStore

        if not skip and self.volumes is not None:
            for v in self.volumes.tolist():
                volumesStore.append(v)
            return
        
        vols = list()
        for v in self.dc.list_volumes():
            vols.append(v)
            volumesStore.append(v)
        self.volumes = np.array(vols)

        lv = len(self.volumes)
        lvols = self.go('lVolumes')
        lvols.set_text("volumes ({})".format(lv))
        self.show_volume_actions() """
        pass

    def show_networks(self, skip=False):
        """ networksStore = self.go('networksStore')
        networksStore.clear()
        self.networksStore = networksStore

        if not skip and self.networks is not None:
            for n in self.networks.tolist():
                networksStore.append(n)
            return
        
        nets = list()
        for n in self.dc.list_networks():
            nets.append(n)
            networksStore.append(n)
        self.networks = np.array(nets)
        
        ln = len(self.networks)
        lnet = self.go('lNetworks')
        lnet.set_text("networks ({})".format(ln))
        self.show_network_actions() """
        pass

    def show_term(self):
        """ term = self.builder.get_object('term')
        if self.term is None and term is not None:
            term.grab_focus()
            self.term = term
            spawn_pty(term, ['/bin/zsh'], [], None) """
        #self.exec('/bin/zsh', argv=['/bin/zsh'])
        pass

    #endregion

    #region show actions
    def show_container_actions(self, vis=True):
        bstart = self.go('bStartContainer')
        binspect = self.go('bInspect')
        blogs = self.go('bContainerLogs')
        brename = self.go('bRenameContainer')
        bexport = self.go('bExportContainer')

        if vis:
            self.show_dashboard_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
        self.vis(vis, bstart, binspect, blogs, brename, bexport)

    def show_dashboard_actions(self, vis=True, status=None):
        bstop = self.go('bStopContainer')
        brestart = self.go('bRestartContainer')
        bkill = self.go('bKillContainer')
        bexec = self.go('bExecContainer')
        battach = self.go('bAttachContainer')
        binspect = self.go('bInspect')
        bsuspend = self.go('bSuspendContainer')
        blogs = self.go('bContainerLogs')
        bresume = self.go('bResumeContainer')
        btop = self.go('bContainerTop')
        brename = self.go('bRenameContainer')
        bexport = self.go('bExportContainer')
        bdiff = self.go('bDiffContainer')
        bbrowse = self.go('bBrowse')

        if vis:
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
            self.show_search_actions(False)
        self.vis(vis, bstop, brestart, bkill, bexec, battach, binspect, bsuspend, blogs, bresume, btop, brename, bexport, bdiff, bbrowse)

        if status == 'running':
            self.vis(False, bresume)
            #bresume.hide()
            #bresume.set_visible(False)
        elif status == 'paused':
            """ bsuspend.hide()
            bstop.hide()
            bkill.hide()
            bexec.hide()
            battach.hide()
            brestart.hide()
            bsuspend.set_visible(False)
            bstop.set_visible(False)
            bkill.set_visible(False)
            bexec.set_visible(False)
            battach.set_visible(False)
            brestart.set_visible(False) """
            self.vis(False, bsuspend, bkill, bexec, battach, brestart, bstop)

    def show_image_actions(self, vis=True):
        brun = self.go('bRunContainer')
        binspect = self.go('bInspect')
        bhistory = self.go('bImageHistory')
        bsave = self.go('bSaveImage')

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
        binspect = self.go('bInspect')

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
        binspect = self.go('bInspect')
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
        bimportimg = self.go('bImportImage')
        bprunecon = self.go('bPruneContainers')
        bpruneimg = self.go('bPruneImages')
        bbuildimg = self.go('bBuildImage')
        bcreateimg = self.go('bCreateImage')
        bcreatecon = self.go('bCreateContainer')
        bload = self.go('bLoadImage')

        """ if vis:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
            self.show_search_actions(False) """
        self.vis(True, bimportimg, bprunecon, bpruneimg, bbuildimg, bcreateimg, bcreatecon, bload)

    def show_search_actions(self, vis=True):
        brun = self.go('bSearchRunContainer')
        bpull = self.go('bPullImage')

        if vis:
            self.show_dashboard_actions(False)
            self.show_container_actions(False)
            self.show_image_actions(False)
            self.show_volume_actions(False)
            self.show_network_actions(False)
        self.vis(vis, brun, bpull)

    #endregion

    #region action callbacks

    def nb1_switch_page_cb(self, a, b, index):
        self.selected_tab = index
        if index == 0:
            self.show_dashboard()
            self.show_dashboard_actions(False)
        elif index == 1:
            #print(f'dashboard-is-not-none: {self.dashboardStore is not None}')
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

    def bExecOptsStart_clicked_cb(self, args):
        c, cc = self.selected_running_container
        (id, cmd) = c[0], c[2]
        txtname = self.wExecOptsBuilder.get_object('txtContainer')
        name = txtname.get_text()
        txtcommand = self.wExecOptsBuilder.get_object('txtCommand')
        cmd = txtcommand.get_text()
        txtenv = self.wExecOptsBuilder.get_object('txtEnv')
        env = txtenv.get_text()
        txtwdir = self.wExecOptsBuilder.get_object('txtWorkingDir')
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wTerm'])
        wterm = builder.get_object('wTerm')
        vterm = builder.get_object('wvTerm')
        hbar = builder.get_object('hbTerm')
        #print(type(wterm), type(vterm), type(hbar))
        hbar.set_title(name)
        hbar.set_subtitle(cmd)
        #print(c, name, str(cmd))
        lflags = []
        chInt = self.wExecOptsBuilder.get_object('chInteractive')
        chTty = self.wExecOptsBuilder.get_object('chTty')
        chDetach = self.wExecOptsBuilder.get_object('chDetach')
        chPriv = self.wExecOptsBuilder.get_object('chPrivileged')
        interactive = chInt.get_active()
        tty = chTty.get_active()
        detach = chDetach.get_active()
        priv = chPriv.get_active()
        if interactive:
            lflags.append("-i")
        if tty:
            lflags.append("-t")
        if priv:
            lflags.append("--privileged")
        if detach:
            lflags.append("-d")
        flags = " ".join(lflags)
        flags = flags.strip(" ")
        if len(lflags)==0: flags = None
        self.dc.exec_container(vterm, name=name or id, flags=lflags, cmd=cmd)

        self.wExecOpts.destroy()
        wterm.show()
    
    def bExecOptsCancel_clicked_cb(self, args):
        self.wExecOpts.destroy()

    def bExecContainer_clicked_cb(self, args):
        if self.wExecOptsBuilder is not None:
            self.wExecOptsBuilder.show()
            return
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wExecOpts', 'wgExecOpts'])
        wExecOpts = builder.get_object('wExecOpts')
        self.wExecOpts = wExecOpts
        c, cc = self.selected_running_container
        (name, cmd) = c[1], c[2]
        hb = builder.get_object('hbExecOpts')
        hb.set_subtitle(name)
        bExecOptsCancel = builder.get_object('bExecOptsCancel')
        bExecOptsCancel.connect('clicked', self.bExecOptsCancel_clicked_cb)
        bExecOptsStart = builder.get_object('bExecOptsStart')
        bExecOptsStart.connect('clicked', self.bExecOptsStart_clicked_cb)
        txtcontainer = builder.get_object('txtContainer')
        txtcontainer.set_text(name)
        txtcommand = builder.get_object('txtCommand')
        txtcommand.set_text(cmd)
        txtcontainer.set_editable(False)
        chInt = builder.get_object('chInteractive')
        chTty = builder.get_object('chTty')
        chPrivileged = builder.get_object('chPrivileged')
        chDetach = builder.get_object('chDetach')
        chInt.set_active(False)
        chTty.set_active(False)
        chPrivileged.set_active(False)
        chDetach.set_active(False)
        self.wExecOptsBuilder = builder
        wExecOpts.show()
    
    def bStopContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        #self.dc.stop_container(container[0])
        id = container[0]
        #print(len(id), id)
        th = threading.Thread(target=self.dc.stop_container, args=[id], daemon=True)
        th.start()
        #th.join()

    def bStartContainer_clicked_cb(self, args):
        self.show_container_actions(False)
        container, c = self.selected_container
        id = container[0]
        th = threading.Thread(target=self.dc.start_container, args=[id], daemon=True)
        th.start()
        #th.join()

    def bRestartContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        id = container[0]
        th = threading.Thread(target=self.dc.restart_container, args=[id], daemon=True)
        th.start()
        #th.join()

    def bSuspendContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        id = container[0]
        th = threading.Thread(target=self.dc.suspend_container, args=[id], daemon=True)
        th.start()
        #th.join()

    def bResumeContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        container, c = self.selected_running_container
        id = container[0]
        th = threading.Thread(target=self.dc.resume_container, args=[id], daemon=True)
        th.start()
        #th.join()

    def bInspect_clicked_cb(self, args):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wInspect', 'tbuData'])
        winspect = builder.get_object('wInspect')
        tvdata = builder.get_object('tvData')
        tbudata = builder.get_object('tbuData')
        hbinspect = builder.get_object('hbInspect')
        hbinspect.set_subtitle(self.selected_name)

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
            tbudata.set_text(json.dumps(d, sort_keys=True, indent=4))
            winspect.show()

    def bContainerLogs_clicked_cb(self, args):
        id = self.selected_id
        name = self.selected_name
        self.exec(name, argv=['docker', 'logs', '-t', '-f', '--details', '--tail', 'all', id])

    def bKillContainer_clicked_cb(self, args):
        self.show_dashboard_actions(False)
        self.dc.kill_container(self.selected_id)

    def bRunContainerCancel_clicked_cb(self, args):
        self.wRunOpts.destroy()

    def bRunContainerSubmit_clicked_cb(self, args):
        go = self.wRunOptsBuilder.get_object
        txtimage = go('txtiImageName')
        image = txtimage.get_text()

        if self.fromSearch:
            self.exec(image, argv=[
                'docker',
                'pull',
                image,
            ])

        txtcontainer = go('txtiContainerName')
        container = slugify(txtcontainer.get_text())
        txtcmd = go('txtiCommand')
        txtwdir = go('txtiWorkingDir')
        cmd = txtcmd.get_text()
        wdir = txtwdir.get_text()
        chtty = go('chRunContainerTty')
        chstream = go('chRunContainerStream')
        chstdout = go('chRunContainerStdout')
        chstderr = go('chRunContainerStderr')
        chstdin = go('chRunContainerStdin')
        chdetach = go('chRunContainerDetach')
        chpriv = go('chRunContainerPrivileged')
        chnetdis = go('chRunContainerNetDisabled')
        txtuser = go('txtRunContainerUser')
        txthost = go('txtRunContainerHostname')
        tty = chtty.get_active()
        stream = chstream.get_active()
        stdout = chstdout.get_active()
        stderr = chstderr.get_active()
        stdin = chstdin.get_active()
        detach = chdetach.get_active()
        priv = chpriv.get_active()
        netdis = chnetdis.get_active()
        user = txtuser.get_text()
        host = txthost.get_text()
        kwargs = RunContanerKwargs(image=image, name=container, command=cmd, working_dir=wdir, tty=tty, stream=stream, stdout=stdout, stderr=stderr, stdin_open=stdin, detach=detach, privileged=priv, network_disabled=netdis, user=user, hostname=host)
        th = threading.Thread(target=self.dc.run_container, args=[kwargs], daemon=True)
        th.start()
        if self.fromSearch == False: self.wRunOpts.destroy()

    def bRunContainer_clicked_cb(self, args):
        opts = RunContainerOptsWindow()
        opts.show()
        """ builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wRunContainerOpts'])
        go = builder.get_object
        wRunOpts = go('wRunContainerOpts')
        self.wRunOpts = wRunOpts
        self.wRunOptsBuilder = builder
        hb = go('hbRunContainerOpts')
        bsubmit = go('bRunContainerSubmit')
        bsubmit.connect('clicked', self.bRunContainerSubmit_clicked_cb)
        bcancel = go('bRunContainerCancel')
        bcancel.connect('clicked', self.bRunContainerCancel_clicked_cb)
        name = self.selected_name
        if name == '<none>':
            name = self.selected_id
        hb.set_subtitle(name)
        txtimage = go('txtiImageName')
        txtimage.set_text(name)
        if self.selected_name != '<none>':
            txtcontainer = go('txtiContainerName')
            txtcontainer.set_text(name)
        wRunOpts.show() """

    def bBrowse_clicked_cb(self, args):
        browser = BrowserWindow(self.selected_running_container, self.dc)
        browser.show()
        """ builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wFileExplorer', 'tsFileExplorer'])
        go = builder.get_object
        wfx = go('wFileExplorer')
        hb = go('hbFileExplorer')
        tview = go('tvFileExplorer')
        tview.connect('cursor-changed', self.tvFileExplorer_cursor_changed_cb)
        tview.connect('move-cursor', self.tvFileExplorer_move_cursor_cb)
        tview.connect('row-activated', self.tvFileExplorer_row_activated_cb)
        tview.connect('row-expanded', self.tvFileExplorer_row_expanded_cb)
        store = go('tsFileExplorer')
        store.clear()
        self.browsers.append([f'{self.selected_id}:{self.selected_name}', store, builder, wfx])
        hb.set_subtitle(self.selected_name)
        priv = check_priv()
        for name in self.dc.ls(self.selected_id):
            if name in ['.', '..']:
                continue
            row = store.append(None, [name, '', ''])
        wfx.show() """

    def tvFileExplorer_row_expanded_cb(self, a, b, c):
        print('row-expanded')

    def tvFileExplorer_row_activated_cb(self, args):
        print('row-activated')

    def tvFileExplorer_move_cursor_cb(self, a, b, c):
        print('move-cursor')

    def tvFileExplorer_cursor_changed_cb(self, args):
        print('cursor-changed')
        sel = args.get_selection()
        [model, iter] = sel.get_selected()
        names = model.get(iter, 0)
        tree = list(names)
        file_path = '/'.join(tree)
        kwargs=ExecRunKwargs(cmd=f'ls -a {file_path}')
        for file in self.dc.ls(kwargs=kwargs):
            print(file)
        #print(name)

    def bAttachContainer_clicked_cb(self, args):
        pass

    def tbPullImage_clicked_cb(self, args):
        self.bPullImage_clicked_cb(args)

    def bPullImage_clicked_cb(self, args):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wPullImage'])
        wpull = builder.get_object('wPullImage')
        self.wPullImage = wpull
        self.wPullImageBuilder = builder
        bpull = builder.get_object('bPull')
        bpull.connect('clicked', self.bPull_clicked_cb)
        bcancel = builder.get_object('bCancelPull')
        bcancel.connect('clicked', self.bCancelPull_clicked_cb)
        wpull.show()

    def bPull_clicked_cb(self, args):
        txtrepo = self.wPullImageBuilder.get_object('txtImageRepo')
        repo = txtrepo.get_text()
        #th = threading.Thread(target=self.dc.pull_image, args=[repo], daemon=True)
        #th.start()
        self.exec(repo, argv=[
            'docker',
            'pull',
            repo,
        ])
        self.wPullImage.destroy()

    def bCancelPull_clicked_cb(self, args):
        self.wPullImage.destroy()

    def tbBuildImage_clicked_cb(self, args):
        self.bBuildImage_clicked_cb(args)

    def bBuildImage_clicked_cb(self, args):
        if self.wBuildImage is not None:
            self.wBuildImage.show()
            return
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wBuildImage'])
        wbuild = builder.get_object('wBuildImage')
        fcbpath = builder.get_object('fcbPath')
        fcbpath.connect('file-set', self.fcbPath_file_set_cb)
        fcbpath.connect('current-folder-changed', self.fcbPath_current_folder_changed_cb)
        fcbpath.connect('file-activated', self.fcbPath_file_activated_cb)
        fcbpath.connect('selection-changed', self.fcbPath_selection_changed_cb)
        fcbpath.connect('update-preview', self.fcbPath_update_preview_cb)
        bbuild = builder.get_object('bBuild')
        bbuild.connect('clicked', self.bBuild_clicked_cb)
        bcancel = builder.get_object('bCancelBuild')
        bcancel.connect('clicked', self.bCancelBuild_clicked_cb)
        self.wBuildImage = wbuild
        self.wBuildImageBuilder = builder
        wbuild.show()

    def bBuild_clicked_cb(self, args):
        go = self.wBuildImageBuilder.get_object
        fcbpath = go('fcbPath')
        uri = str(fcbpath.get_uri())
        uri = uri.replace('file://', '')
        txttag = go('txtTag')
        tag = txttag.get_text()
        chquiet = go('chQuiet')
        chrm = go('chRm')
        chnocache = go('chNoCache')
        chpull = go('chPull')
        chsquash = go('chSquash')
        quiet = chquiet.get_active()
        rm = chrm.get_active()
        nocache = chnocache.get_active()
        pull = chpull.get_active()
        squash = chsquash.get_active()
        #kwargs = BuildImageKwargs(path=uri, tag=[tag], quiet=quiet, nocache=nocache, rm=rm, pull=pull, squash=squash, dockerfile='Dockerfile')
        argv = ['docker', 'build']
        if quiet:
            argv.append('-q')
        if rm:
            argv.append('--rm')
        if nocache:
            argv.append('--no-cache')
        if pull:
            argv.append('--pull')
        if squash:
            argv.append('--compress')
        if tag is not None and len(tag)>0: argv=argv+['-t', tag]
        argv.append(uri)
        self.exec('build image', argv=argv)
        self.wBuildImage.destroy()

    def fcbPath_file_set_cb(self, args):
        print('fcbPath_file_set_cb#args:', args)

    def fcbPath_current_folder_changed_cb(self, args):
        print('fcbPath_current_folder_changed_cb#args:', args)

    def fcbPath_selection_changed_cb(self, args):
        print('fcbPath_selection_changed_cb#args:', args)

    def fcbPath_update_preview_cb(self, args):
        print('fcbPath_update_preview_cb#args:', args)

    def fcbPath_file_activated_cb(self, args):
        print('fcbPath_file_activated_cb#args:', args)

    def bCancelBuild_clicked_cb(self, args):
        self.wBuildImage.destroy()

    def tbImportImage_clicked_cb(self, args):
        self.bImportImage_clicked_cb(args)

    def bImportImage_clicked_cb(self, args):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wImportImage'])
        wimport = builder.get_object('wImportImage')
        wimport.show()

    def bContainerTop_clicked_cb(self, args):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wTop', 'wsTop'])
        go = builder.get_object
        wtop = go('wTop')
        wstop = go('wsTop')
        hb = go('hbTop')
        hb.set_subtitle(self.selected_name)
        (container, c) = self.selected_running_container
        top = self.dc.container_top(self.selected_id)
        procs = top['Processes']
        for p in procs:
            wstop.append(p)
        wtop.show()

    def tbCreateContainer_clicked_cb(self, args):
        self.bCreateContainer_clicked_cb(args)

    def bCreateContainer_clicked_cb(self, args):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wCreateContainer'])
        go = builder.get_object
        wccon = go('wCreateContainer')
        self.wCreateContainer = wccon
        self.wCreateContainerBuilder = builder
        hb = go('hbCreateContainer')
        imgname = go('txtcImageName')
        if self.selected_tab == 2:
            hb.set_subtitle(self.selected_name)
            imgname.set_text(self.selected_name)
            imgname.set_editable(False)
        bcreate = go('bCreateContainerSubmit')
        bcancel = go('bCreateContainerCancel')
        bcreate.connect('clicked', self.bCreateContainerSubmit_clicked_cb)
        bcancel.connect('clicked', self.bCreateContainerCancel_clicked_cb)
        wccon.show()

    def bCreateContainerSubmit_clicked_cb(self, args):
        go = self.wCreateContainerBuilder.get_object
        txtimgname = go('txtcImageName')
        txtconname = go('txtcContainerName')
        txtcommand = go('txtcCommand')
        txtwdir = go('txtcWorkingDir')
        imgname = txtimgname.get_text()
        conname = txtconname.get_text()
        command = txtcommand.get_text()
        wdir = txtwdir.get_text()
        kwargs = CreateContanerKwargs(image=imgname, name=conname, command=command, working_dir=wdir)
        th = threading.Thread(target=self.dc.create_container, args=[kwargs], daemon=True)
        th.start()
        self.wCreateContainer.destroy()

    def bCreateContainerCancel_clicked_cb(self, args):
        self.wCreateContainer.destroy()

    def bRenameContainer_clicked_cb(self, args):
        print("coming soon")

    def bExportContainer_clicked_cb(self, args):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['fcdExportContainer'])
        self.exportContainerBuilder = builder
        go = builder.get_object
        hb = go('hbExportContainer')
        hb.set_subtitle(self.selected_name)
        fcd = go('fcdExportContainer')
        fcd.connect('current-folder-changed', self.fcdExportContainer_current_folder_changed_cb)
        fcd.connect('file-activated', self.fcdExportContainer_file_activated_cb)
        fcd.connect('selection-changed', self.fcdExportContainer_selection_changed_cb)
        fcd.connect('update-preview', self.fcdExportContainer_update_preview_cb)
        fcd.set_current_name(self.selected_name)
        print(fcd.get_current_name())
        export = go('fcbExport')
        cancel = go('fcbCancelExport')
        export.connect('clicked', self.fcbExport_clicked_cb)
        cancel.connect('clicked', self.fcbCancelExport_clicked_cb)
        fcd.set_action(Gtk.FileChooserAction.SAVE)
        self.exportContainer = fcd
        fcd.show()

    def fcbExport_clicked_cb(self, args):
        id = self.selected_id
        fcd = self.exportContainer
        filename = fcd.get_current_name() or self.selected_name
        #print(fcd.get_current_folder(), filename)
        self.exportContainer.destroy()
        self.exportContainer = None
        th = threading.Thread(target=self.dc.export_container, args=[id, filename], daemon=True)
        th.start()

    def fcbCancelExport_clicked_cb(self, args):
        self.exportContainer.destroy()
        self.exportContainer = None

    def fcdExportContainer_current_folder_changed_cb(self, args):
        print('fcdExportContainer_current_folder_changed_cb')

    def fcdExportContainer_file_activated_cb(self, args):
        print('fcdExportContainer_file_activated_cb')

    def fcdExportContainer_selection_changed_cb(self, args):
        print('fcdExportContainer_selection_changed_cb')

    def fcdExportContainer_update_preview_cb(self, args):
        print('fcdExportContainer_update_preview_cb')

    def bImageHistory_clicked_cb(self, args):
        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wHistory', 'wsHistory'])
        go = builder.get_object
        whistory = go('wHistory')
        wshistory = go('wsHistory')
        hb = go('hbHistory')
        hb.set_subtitle(self.selected_name)
        history = self.dc.image_history(self.selected_id)
        print(history)
        for h in history:
            dt = datetime.fromtimestamp(h['Created'])
            print(dt.astimezone())
            wshistory.append([
                h['Id'][:12],
                get_time_ago(dt.strftime("%Y-%m-%d %H:%M:%S"), ms=False),
                h['CreatedBy'],
                pretty_size(h['Size']),
                h['Comment'],
            ])
        whistory.show()

    def bSearch_clicked_cb(self, args):
        txtsearch = self.go('txtSearchImage')
        term = txtsearch.get_text()
        res = self.dc.search_image(term)
        searchStore = self.go('searchStore')
        searchStore.clear()
        imgs = list()
        for r in res:
            row = [
                r['name'],
                r['description'],
                r['star_count'],
                r['is_official'],
                r['is_automated'],
            ]
            searchStore.append(row)
            imgs.append(row)
        self.searches = np.array(imgs)
        self.searchStore = searchStore

    def bPruneContainers_clicked_cb(self, args):
        print("coming soon")

    def bPruneImages_clicked_cb(self, args):
        print("coming soon")

    def bDiffContainer_clicked_cb(self, args):
        id = self.selected_id
        diff = self.dc.diff_container(id)
        ldiff = 0
        if diff is not None:
            ldiff = len(diff)
        print(ldiff)
    
    def bSaveImage_clicked_cb(self, args):
        if self.saveImageDialog is not None:
            self.saveImageDialog.show()
            return
        
        dlg = self.go('fcdSaveImage')
        self.saveImageDialog = dlg

        hb = self.go('hbSaveImage')
        hb.set_subtitle(self.selected_name)

        txtfilename = self.go('fctSaveFilename')
        txtfilename.set_text(self.selected_name)
        dlg.show()

    def bSearchRunContainer_clicked_cb(self, args):
        self.fromSearch = True

        builder = Gtk.Builder()
        builder.add_objects_from_file(UI_FILE, ['wRunContainerOpts'])
        wRunOpts = builder.get_object('wRunContainerOpts')
        self.wRunOpts = wRunOpts
        self.wRunOptsBuilder = builder
        hb = builder.get_object('hbRunContainerOpts')
        bsubmit = builder.get_object('bRunContainerSubmit')
        bsubmit.connect('clicked', self.bRunContainerSubmit_clicked_cb)
        bcancel = builder.get_object('bRunContainerCancel')
        bcancel.connect('clicked', self.bRunContainerCancel_clicked_cb)
        name = self.selected_name
        if name == '<none>':
            name = self.selected_id
        hb.set_subtitle(name)
        txtimage = builder.get_object('txtiImageName')
        txtimage.set_text(name)
        txtcontainer = builder.get_object('txtiContainerName')
        txtcontainer.set_text(name)
        wRunOpts.show()

    def fcdSaveImage_current_folder_changed_cb(self, args):
        print('[fcdSaveImage_current_folder_changed_cb]:', args)

    def fcdSaveImage_file_activated_cb(self, args):
        print('[fcdSaveImage_file_activated_cb]:', args)

    def fcdSaveImage_selection_changed_cb(self, args):
        print('[fcdSaveImage_selection_changed_cb]:', args)

    def fcdSaveImage_update_preview_cb(self, args):
        print('[fcdSaveImage_update_preview_cb]:', args)

    def fcbSave_clicked_cb(self, args):
        print('[fcbSave_clicked_cb]:', args)

    def fcbCancelSave_clicked_cb(self, args):
        pass

    def bLoadImage_clicked_cb(self, args):
        pass

    def fcdLoadImage_current_folder_changed_cb(self, args):
        pass

    def fcdLoadImage_file_activated_cb(self, args):
        pass

    def fcdLoadImage_selection_changed_cb(self, args):
        pass

    def fcdLoadImage_update_preview_cb(self, args):
        pass

    def fcbOpen_clicked_cb(self, args):
        pass

    def fcbCancelOpen_clicked_cb(self, args):
        pass

    #endregion

def main():
    try:
        # get_priv()
        app = Pyzza()
        #app.connect('destroy', Gtk.main_quit)
        app.run(sys.argv)
        #app.start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()