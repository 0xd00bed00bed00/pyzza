from gi.repository import Gtk
import configparser, string, random, uuid, re

@Gtk.Template.from_file('src/ui/manage.glade')
class ManageConnectionsWindow(Gtk.Window):
    __gtype_name__ = 'wManageConnections'

    config = configparser.ConfigParser()

    activeConnection = None
    defaultConnection = None
    selectedConnection = None
    selectedConnectionLabel = None
    connections = dict()

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

    def __init__(self):
        super().__init__()
        cfg = self.config
        cfg.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        try:
            cfg.read('config.ini')
            #self.defaultConnection = cfg['DEFAULT']
            default = cfg['DEFAULT']
            id = self.gen_id()
            self.defaultId = id
            tp = default['type']
            #print('[tp]:', tp, tp.isnumeric())
            if tp.isnumeric() or tp == '-1':
                tp = int(tp)
            else:
                model = self.cbType.get_model()
                for row in range(len(model)):
                    if model[row][0] == tp:
                        tp = row
                        break
            self.connections['DEFAULT'] = {
                'dat': {
                    'name': default['name'] or 'default',
                    'type': tp,
                    'path': default['path'] or '',
                },
                'old': default['name'],
                'cfg': default,
                'lbl': self.lDefaultConnection,
                'id': id,
            }
            conns = cfg.sections()
            #print(conns)
            for conn in conns:
                #id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                tp = cfg[conn]['type']
                print('[cfg]:', tp, tp.isnumeric())
                if tp.isnumeric():
                    tp = int(tp)
                else:
                    #tp = -1
                    cb = self.cbType
                    model = cb.get_model()
                    print('[model]:', model[0][0])
                    for row in range(len(model)):
                        print('[row]:', row, model[row][0], tp, model[row][0] == tp)
                        if model[row][0] == tp:
                            tp = row
                            print('[match]:', tp)
                            break
                row = self.create_row(name=conn, old_name=conn, conntype=tp, path=cfg[conn]['path'])
                assert row is not None
                self.lbConnections.insert(row, -1)
                #self.lbConnections.select_row(row)
            #self.defaultConnection = default
            print('[load]:', self.connections)
            self.defaultConnection = self.connections['DEFAULT']
            self.lbConnections.select_row(self.lrDefaultConnection)
            self.bDelete.set_sensitive(False)
            self.bDelete.set_visible(False)
            self.bSetAsDefault.set_sensitive(False)
            self.bSetAsDefault.set_visible(False)
            self.txtName.set_text(default['name'])
            self.cbType.set_active(int(default['type']))
            self.txtPath.set_text(default['path'])
            #self.chSetAsDefault.set_active(True)
            #self.chSetAsDefault.set_sensitive(False)
            self.lDefaultConnection.set_name(id)
            #self.selectedConnectionLabel = self.lDefaultConnection
        except Exception as e:
            print('error:', e)

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        name = self.txtName.get_text()
        conntype = self.cbType.get_active()
        path = self.txtName.get_text()
        cfg = self.config
        cb = self.cbType
        model = cb.get_model()
        #print('[keys]:', self.connections.keys())
        for (key, value) in self.connections.items():
            #print(key, value)
            old = value['old']
            #print('[old]:', old is not None, old in cfg.sections(), old in self.connections.keys(), old)
            if old is not None:
                cfg.remove_section(old)
            if key == 'DEFAULT':
                #print('[value]:', value['dat'])
                tp = model[value['dat']['type']][0] or -1
                #value['dat']['type'] = tp
                cfg['DEFAULT']['type'] = tp
                continue
            d = value['dat']
            #print(d, d['name'])
            tp = model[d['type']][0] or -1
            cfg[d['name']] = {
                'type': tp,
                'path': d['path'] or '',
            }
        print('[save]:', self.connections)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    @Gtk.Template.Callback()
    def bTest_clicked_cb(self, args):
        name = self.txtName.get_text()
        conntype = self.cbType.get_active()
        path = self.txtName.get_text()
        #default = self.chSetAsDefault.get_active()

    @Gtk.Template.Callback()
    def bNew_clicked_cb(self, args):
        assert self.lbConnections is not None
        row = self.create_row(name=self.DEFAULT_NEW_CONNECTION_NAME, conntype=-1, path='')
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
        name = conn['dat']['name']
        if name in self.config.sections():
            self.config.remove_section(name)
        self.connections.pop(id)
        print(id in self.connections.keys())
        lb = self.lbConnections
        row = lb.get_selected_row()
        row.destroy()
        lb.select_row(self.lrDefaultConnection)

    @Gtk.Template.Callback()
    def bSetAsDefault_clicked_cb(self, args):
        lbl = self.selectedConnectionLabel
        id = lbl.get_name()
        assert id is not None
        default = self.defaultConnection
        conn = self.selectedConnection
        cfg = self.config
        dat = conn['dat']
        name = dat['name']
        #print('[sections]:', cfg.sections(), self.connections.keys())
        assert name in cfg.sections()
        assert id in self.connections.keys()
        self.connections[default['id']] = default
        self.connections['DEFAULT'] = {
            'dat': conn['dat'],
            'old': conn['dat']['name'],
            'lbl': lbl,
        }
        #print(name in cfg.sections())
        cfg['DEFAULT'] = dat
        cfg[default['dat']['name']] = default['dat']
        cfg.remove_section(name)
        self.connections.pop(id)
        #print('[DEFAULT]:', cfg['DEFAULT'])

    @Gtk.Template.Callback()
    def lbConnections_activate_cursor_row_cb(self, a, b):
        print('[lbConnections_activate_cursor_row_cb]:', a, b)

    @Gtk.Template.Callback()
    def lbConnections_move_cursor_cb(self, a, b, c):
        print('[lbConnections_move_cursor_cb]:', a, b, c)

    @Gtk.Template.Callback()
    def lbConnections_row_activated_cb(self, a, b):
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
            self.txtName.set_text(conn['dat']['name'])
            self.cbType.set_active(conn['dat']['type'])
            self.txtPath.set_text(conn['dat']['path'])
            return
        #if idx == 0:
        self.selectedConnection = default = self.defaultConnection
        #print('[selected]:', self.selectedConnection)
        self.txtName.set_text(default['dat']['name'])
        self.cbType.set_active(default['dat']['type'])
        self.txtPath.set_text(default['dat']['path'])
        #self.chSetAsDefault.set_active(True)
        #self.chSetAsDefault.set_sensitive(False)
        self.bDelete.set_sensitive(False)
        self.bDelete.set_visible(False)
        self.bSetAsDefault.set_sensitive(False)
        self.bSetAsDefault.set_visible(False)
        print('[conns]:', self.connections)

    @Gtk.Template.Callback()
    def lbConnections_row_selected_cb(self, a, b):
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
            self.selectedConnection = self.connections['DEFAULT']
            self.bSetAsDefault.set_sensitive(False)
            self.bSetAsDefault.set_visible(False)
            self.bDelete.set_sensitive(False)
            self.bDelete.set_visible(False)
        #    self.chSetAsDefault.set_active(True)
        #    self.chSetAsDefault.set_sensitive(False)

    @Gtk.Template.Callback()
    def lbConnections_selected_rows_changed_cb(self, a):
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
            self.selectedConnection = self.connections['DEFAULT']
            self.bSetAsDefault.set_sensitive(False)
            self.bSetAsDefault.set_visible(False)
            self.bDelete.set_sensitive(False)
            self.bDelete.set_visible(False)
        #    self.chSetAsDefault.set_active(True)
        #    self.chSetAsDefault.set_sensitive(False)

    @Gtk.Template.Callback()
    def lrDefaultConnection_activate_cb(self, args):
        print('[lrDefaultConnection_activate_cb]:', args)

    @Gtk.Template.Callback()
    def txtName_changed_cb(self, args):
        self.selectedConnectionLabel.set_text(args.get_text())
        id = self.selectedConnectionLabel.get_name()
        if id in self.connections.keys():
            self.connections[id]['dat']['name'] = args.get_text()

    @Gtk.Template.Callback()
    def cbType_changed_cb(self, args):
        id = self.selectedConnectionLabel.get_name()
        cb = self.cbType
        t = cb.get_active()
        if id in self.connections.keys() or id == 'DEFAULT':
            #model = cb.get_model()
            #value = model[t][0]
            #print('[value]:', value)
            self.connections[id]['dat']['type'] = t

    @Gtk.Template.Callback()
    def txtPath_changed_cb(self, args):
        id = self.selectedConnectionLabel.get_name()
        if self.selectedConnection['id'] != self.defaultConnection['id']:
            self.connections[id]['dat']['path'] = args.get_text()
            return
        self.connections['DEFAULT']['dat']['path'] = args.get_text()

    def show(self):
        super().show()
        print('[conns]:', self.connections)

    def create_row(self, name=None, old_name=None, set_fields=False, conntype=None, path=None, default=False):
        print('[conntype]:', conntype)
        id = self.gen_id()

        row = Gtk.ListBoxRow()
        row.set_name(id)
        row.set_activatable(True)
        row.set_selectable(True)
        row.set_visible(True)
        txt = Gtk.Label(name)
        txt.set_visible(True)
        txt.set_name(id)
        row.add(txt)

        if set_fields:
            self.txtName.set_text(name)
            self.cbType.set_active(conntype)
            self.txtPath.set_text(path)

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

        return row
    
    def gen_id(self):
        rnd = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, rnd)
        id = str(uid)
        return id

class Connection:
    name = None
    conntype = None
    path = None

    def __init__(self):
        pass