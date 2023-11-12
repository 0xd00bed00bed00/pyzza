from gi.repository import Gtk, Gio
import configparser, string, random, uuid, re
from config import ConfigManager, Config
from utils import gen_id, notify
import threading, redis
from client import Docker
from sqlalchemy.orm import Session
from models.data import Connection, engine

@Gtk.Template.from_file('src/ui/manage.glade')
class ManageConnectionsWindow(Gtk.Window):
    __gtype_name__ = 'wManageConnections'

    config = None #configparser.ConfigParser()

    activeConnection = None
    defaultConnection = None
    selectedConnection = None
    selectedConnectionLabel = None
    connections = None

    txtName = Gtk.Template.Child()
    cbType = Gtk.Template.Child()
    txtPath = Gtk.Template.Child()
    bSetAsDefault = Gtk.Template.Child()
    bTest = Gtk.Template.Child()
    bDelete = Gtk.Template.Child()
    connectiontypelist = Gtk.Template.Child()
    lbConnections = Gtk.Template.Child()
    lrDefaultConnection = Gtk.Template.Child()
    lDefaultConnection = Gtk.Template.Child()

    name = None
    conntype = None
    path = None
    default = None
    defaultId = None

    DEFAULT_NEW_CONNECTION_NAME = 'New Connection'

    isupdating = False

    def __init__(self):
        super().__init__()
        self.config = ConfigManager.load(ConfigManager.configpath)
        cfg = self.config.config
        cfg.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        try:
            assert self.config is not None
            assert self.config.config is not None
            default = self.config.default_connection
            assert default is not None
            self.defaultConnection = self.config.default_connection
            self.connections = self.config.connections
            for (id, conn) in self.connections.items():
                if id == 'DEFAULT':
                    continue
                tp = conn.ctype
                row = self.create_row(id=id, name=conn.name, old_name=conn.old, conntype=tp, path=conn.connpath)
                assert row is not None
                self.lbConnections.insert(row, -1)
            
            self.defaultConnection = self.connections['DEFAULT']
            self.lbConnections.select_row(self.lrDefaultConnection)
            self.bDelete.set_sensitive(False)
            self.bDelete.set_visible(False)
            self.bSetAsDefault.set_sensitive(False)
            self.bSetAsDefault.set_visible(False)
            self.txtName.set_text(default.name)
            self.cbType.set_active(Config.get_index(typestr=default.conntype))
            self.txtPath.set_text(default.connpath)
            self.lDefaultConnection.set_name(default.id)
            self.lDefaultConnection.set_text(default.name)
        except Exception as e:
            print('error:', e)

    def update_list(self):
        self.isupdating = True
        for child in self.lbConnections.get_children():
            self.lbConnections.remove(child)
        self.lbConnections.insert(self.lrDefaultConnection, 0)
        for (key, conn) in self.connections.items():
            if key == 'DEFAULT':
                continue
            tp = conn.ctype
            row = self.create_row(id=key, name=conn.name, old_name=conn.old, conntype=tp, path=conn.connpath, set_fields=True)
            assert row is not None
            self.lbConnections.insert(row, -1)
        default = self.defaultConnection
        self.bDelete.set_sensitive(False)
        self.bDelete.set_visible(False)
        self.bSetAsDefault.set_sensitive(False)
        self.bSetAsDefault.set_visible(False)
        self.txtName.set_text(default.name)
        self.cbType.set_active(Config.get_index(typestr=default.conntype))
        self.txtPath.set_text(default.connpath)
        self.lDefaultConnection.set_name(default.id)
        self.lDefaultConnection.set_text(default.name)
        self.lbConnections.select_row(self.lrDefaultConnection)
        self.isupdating = False

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        cfg = self.config.config
        cb = self.cbType
        model = cb.get_model()
        with Session(engine, expire_on_commit=False) as session:
            dc = dict(**self.connections)
            cfg.clear()
            for (key, value) in dc.items():
                session.add(value)
                old = value.old
                if old is not None:
                    cfg.remove_section(old)
                    if value.action == 'delete':
                        value.delete()
                        self.connections.pop(value.id)
                        cfg.remove_section(value.old)
                if key == 'DEFAULT':
                    self.defaultConnection = value
                    rowid = value.ctype
                    it = model.get_iter_from_string(f'{rowid}:0')
                    tp, *rem = model.get(it, *[0])
                    cfg['DEFAULT']['type'] = tp
                    continue
                value.old = value.name
                tp = model[value.ctype] or -1
                cfg[value.name] = {
                    'type': tp,
                    'path': value.connpath or '',
                }
            session.commit()
        self.config.save()
        self.update_list()

    @Gtk.Template.Callback()
    def bTest_clicked_cb(self, args):
        name = self.txtName.get_text()
        model = self.cbType.get_model()
        conntype = model[self.cbType.get_active()][0]
        path = self.txtPath.get_text()
        try:
            dc = Docker(f'{conntype}://{path}')
            dc.daemon.ping()
            print('connection successful!')
            notify(summary='Connecting to server', body='connection successful')
        except Exception as ex:
            print('[test connection]:', ex)
        #default = self.chSetAsDefault.get_active()

    @Gtk.Template.Callback()
    def bNew_clicked_cb(self, args):
        assert self.lbConnections is not None
        id = gen_id()
        newconn = Connection(id=id, name=self.DEFAULT_NEW_CONNECTION_NAME, type=-1, path='')
        newconn.old = None
        self.connections[id] = newconn
        row = self.create_row(id=id, name=self.DEFAULT_NEW_CONNECTION_NAME, conntype=-1, path='', old_name=None)
        self.lbConnections.insert(row, -1)
        self.lbConnections.select_row(row)

        self.txtName.set_text(self.DEFAULT_NEW_CONNECTION_NAME)
        self.cbType.set_active(-1)
        self.txtPath.set_text('')

        self.bDelete.set_sensitive(True)
        self.bSetAsDefault.set_sensitive(False)

        #print('[keys]:', self.connections.keys())

    @Gtk.Template.Callback()
    def bDelete_clicked_cb(self, args):
        lbl = self.selectedConnectionLabel
        id = lbl.get_name()
        conn = self.selectedConnection
        conn.action = 'delete'
        name = conn.name
        if name in self.config.config.sections():
            self.config.config.remove_section(name)
        if conn.old is None:
            self.connections.pop(conn.id)
        #self.connections.pop(conn.id)
        print(id in self.connections.keys(), len(self.connections))
        lb = self.lbConnections
        row = lb.get_selected_row()
        row.destroy()
        default = self.defaultConnection
        self.selectedConnection = default
        lb.select_row(self.lrDefaultConnection)

    @Gtk.Template.Callback()
    def bSetAsDefault_clicked_cb(self, args):
        lbl = self.selectedConnectionLabel
        id = lbl.get_name()
        assert id is not None
        default = self.defaultConnection
        conn = self.selectedConnection
        conn.action = 'setasdefault'
        cfg = self.config.config
        #dat = conn['dat']
        name = conn.name
        #print('[sections]:', cfg.sections(), self.connections.keys())
        #assert name in cfg.sections()
        assert id in self.connections.keys()
        default.isdefault = False
        self.connections[default.id] = default
        conn.isdefault = True
        self.connections['DEFAULT'] = conn
        #print(name in cfg.sections())
        cfg.remove_section(conn.name)
        cfg['DEFAULT'] = {
            'name': conn.name,
            'type': conn.conntype,
            'path': conn.connpath,
        }
        cfg[default.name] = {
            'name': default.name,
            'type': default.conntype,
            'path': default.connpath,
        }
        self.connections.pop(conn.id)
        #self.defaultConnection = conn
        print('[DEFAULT]:', conn)

    @Gtk.Template.Callback()
    def lbConnections_activate_cursor_row_cb(self, a, b):
        print('[lbConnections_activate_cursor_row_cb]:', a, b)

    @Gtk.Template.Callback()
    def lbConnections_move_cursor_cb(self, a, b, c):
        print('[lbConnections_move_cursor_cb]:', a, b, c)

    @Gtk.Template.Callback()
    def lbConnections_row_activated_cb(self, a, b):
        if self.isupdating: return
        #row = self.lbConnections.get_selected_row()
        idx = b.get_index()
        #print('[lbConnections_row_activated_cb]:', idx, a, b)
        chd = b.get_children()
        lbl = chd[0]
        self.selectedConnectionLabel = lbl
        id = lbl.get_name()
        assert id is not None
        #print('[hdr]:', chd, lbl.get_text(), lbl.get_name())
        #self.chSetAsDefault.set_sensitive(True)
        self.bDelete.set_sensitive(True)
        self.bDelete.set_visible(True)
        self.bSetAsDefault.set_sensitive(True)
        self.bSetAsDefault.set_visible(True)
        id = lbl.get_name()
        if idx > 0:
            self.selectedConnection = self.connections[id]
            #print('[selected]:', self.selectedConnection)
            conn = self.connections[id]
            self.txtName.set_text(conn.name)
            self.cbType.set_active(conn.ctype)
            self.txtPath.set_text(conn.connpath)
            return
        #if idx == 0:
        default = self.defaultConnection
        self.selectedConnection = default
        #print('[selected]:', self.selectedConnection)
        self.txtName.set_text(self.defaultConnection.name)
        self.cbType.set_active(self.defaultConnection.ctype)
        self.txtPath.set_text(self.defaultConnection.connpath)
        #self.chSetAsDefault.set_active(True)
        #self.chSetAsDefault.set_sensitive(False)
        self.bDelete.set_sensitive(False)
        self.bDelete.set_visible(False)
        self.bSetAsDefault.set_sensitive(False)
        self.bSetAsDefault.set_visible(False)
        print('[conns]:', self.connections)

    @Gtk.Template.Callback()
    def lbConnections_row_selected_cb(self, a, b):
        if self.isupdating: return
        row = self.lbConnections.get_selected_row()
        if b is None:
            a.select_row(self.lrDefaultConnection)
            return
        idx = b.get_index()
        chd = b.get_children()
        lbl = chd[0]
        self.selectedConnectionLabel = lbl
        id = lbl.get_name()
        assert id is not None
        if idx > 0:
            self.selectedConnection = self.connections[id]
        #print('[lbConnections_row_selected_cb]:', idx, a, b)
        #self.chSetAsDefault.set_sensitive(True)
        self.bDelete.set_sensitive(True)
        self.bDelete.set_visible(True)
        if idx == 0:
            self.selectedConnection = self.defaultConnection
            self.txtName.set_text(self.defaultConnection.name)
            self.cbType.set_active(self.defaultConnection.ctype)
            self.txtPath.set_text(self.defaultConnection.connpath)
            self.bSetAsDefault.set_sensitive(False)
            self.bSetAsDefault.set_visible(False)
            self.bDelete.set_sensitive(False)
            self.bDelete.set_visible(False)
        #    self.chSetAsDefault.set_active(True)
        #    self.chSetAsDefault.set_sensitive(False)

    @Gtk.Template.Callback()
    def lbConnections_selected_rows_changed_cb(self, a):
        if self.isupdating: return
        row = a.get_selected_row()
        if row is None:
            a.select_row(self.lrDefaultConnection)
            return
        idx = row.get_index()
        chd = row.get_children()
        lbl = chd[0]
        self.selectedConnectionLabel = lbl
        id = lbl.get_name()
        assert id is not None
        if idx > 0:
            self.selectedConnection = self.connections[id]
        print('[lbConnections_selected_rows_changed_cb]:', idx, a)
        #self.chSetAsDefault.set_sensitive(True)
        self.bDelete.set_sensitive(True)
        self.bDelete.set_visible(True)
        if idx == 0:
            self.selectedConnection = self.defaultConnection
            self.txtName.set_text(self.defaultConnection.name)
            self.cbType.set_active(self.defaultConnection.ctype)
            self.txtPath.set_text(self.defaultConnection.connpath)
            self.bSetAsDefault.set_sensitive(False)
            self.bSetAsDefault.set_visible(False)
            self.bDelete.set_sensitive(False)
            self.bDelete.set_visible(False)

    @Gtk.Template.Callback()
    def lrDefaultConnection_activate_cb(self, args):
        print('[lrDefaultConnection_activate_cb]:', args)

    @Gtk.Template.Callback()
    def txtName_changed_cb(self, args):
        if self.isupdating: return
        self.selectedConnectionLabel.set_text(args.get_text())
        id = self.selectedConnectionLabel.get_name()
        if id in self.connections.keys():
            self.connections[id].name = args.get_text()
        if id == self.defaultConnection.id:
            self.connections['DEFAULT'].name = args.get_text()

    @Gtk.Template.Callback()
    def cbType_changed_cb(self, args):
        if self.isupdating: return
        id = self.selectedConnectionLabel.get_name()
        cb = self.cbType
        t = cb.get_active()
        if id in self.connections.keys() or id == 'DEFAULT':
            model = cb.get_model()
            value = model[t][0]
            self.connections[id].ctype = t
            self.connections[id].conntype = value

    @Gtk.Template.Callback()
    def txtPath_changed_cb(self, args):
        if self.isupdating: return
        id = self.selectedConnectionLabel.get_name()
        if self.selectedConnection.id != self.defaultConnection.id:
            self.connections[id].connpath = args.get_text()
            return
        self.connections['DEFAULT'].connpath = args.get_text()

    def show(self):
        super().show()

    def destroy(self):
        super().destroy()

    def create_row(self, id=None, name=None, old_name=None, set_fields=False, conntype=None, path=None, default=False):
        _id=id
        if not id:
            _id = gen_id()

        row = Gtk.ListBoxRow()
        row.set_name(_id)
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(name)
        txt.set_visible(True)
        txt.set_name(_id)
        row.add(txt)

        if set_fields:
            self.txtName.set_text(name)
            self.cbType.set_active(conntype)
            self.txtPath.set_text(path)

        '''
        self.connections[id] = {
            'dat': {
                'name': name,
                'type': conntype,
                'path': path,
            },
            'old': old_name,
            'lbl': txt,
            'id': id,
        }
        '''

        return row
    
    '''
    def gen_id(self):
        rnd = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, rnd)
        id = str(uid)
        return id
    '''

class Connection2:
    name = None
    conntype = None
    path = None

    def __init__(self):
        pass