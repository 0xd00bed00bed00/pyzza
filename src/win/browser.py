import gi
from gi.repository import Gtk
from client import Docker
from .ccopy import *
import numpy as np

@Gtk.Template.from_file('src/ui/file_explorer.glade')
class BrowserWindow(Gtk.Window):
    __gtype_name__ = 'wFileExplorer'

    container_id = None
    container_name = None
    container = None
    hbFileExplorer: Gtk.HeaderBar = Gtk.Template.Child()
    tvFileExplorer: Gtk.TreeView = Gtk.Template.Child()
    tsFileExplorer: Gtk.TreeStore = Gtk.Template.Child()
    bCopyFromContainer: Gtk.Button = Gtk.Template.Child()
    bCopyToContainer: Gtk.Button = Gtk.Template.Child()
    selected_path = list()

    def __init__(self, container=None):
        super().__init__()
        self.dc = Docker()
        assert container is not None
        #print(container[0][0], container[0][1])
        self.container_id = container[0][0]
        self.container_name = container[0][1]
        self.hbFileExplorer.set_subtitle(self.container_name or self.container_id)
        self.selected_path = list()

    def show(self):
        #self.selected_path.append()
        for line in self.dc.ls(self.container_id, path='/'):
            #print('[line]:', line)
            props = line.split(' ')
            props = self.remove_empty(props)
            #print('[props]:', props)
            #print('[props]:', len(props), props)
            if len(props)==0: continue
            name = props[-1]
            if name in ['.', '..'] or len(props)<9:
                continue
            if len(props)>9:
                name = props[-3]
            #print(name)
            file_type = self.dc.get_file_type(self.container_id, path=f'/{name}')
            #mime_type = self.dc.get_mime_type(self.container_id, path=f'/{name}')
            created = ' '.join(props[5:8])
            owner = ':'.join(props[2:4])
            #print(created, owner)
            row = [name, file_type, props[4], created, owner, props[0]]
            self.tsFileExplorer.append(None, row)
        super().show()

    @Gtk.Template.Callback()
    def tvFileExplorer_move_cursor_cb(self, args):
        pass

    @Gtk.Template.Callback()
    def tvFileExplorer_row_activated_cb(self, args, a, b):
        pass

    @Gtk.Template.Callback()
    def tvFileExplorer_row_expanded_cb(self, args, a, b):
        pass

    @Gtk.Template.Callback()
    def tvFileExplorer_cursor_changed_cb(self, args):
        spath = np.array(self.selected_path)
        sel = args.get_selection()
        [mmodel, paths] = sel.get_selected_rows()
        [model, iter] = sel.get_selected()
        tpath = paths[0]
        #file_uri = f'/'
        nn = model.get_value(iter, 0)
        props = nn.split(' ')
        depth = tpath.get_depth()
        perms = model.get_value(iter, 1)
        #file_path = self.get_file_path(tpath, model)
        #file_uri = '/' + file_path
        #print('[file_uri]: ', file_uri)
        #if perms!='folder':
        #    return
        file_path = '/'
        row = np.where(spath==f'idx={tpath.to_string()}')
        if np.size(row)>0:
            return
        if props is not None and len(props)>=9:
            name = props[-1]
            #if depth <= len(spath):
            #    start = len(spath)-depth
            #    spath = spath[start:len(spath)]
        else:
            spath = list()
            (file_path, spath) = self.get_file_path(tpath, model)
            #print('[get_file_path]:', file_path, spath)
            self.selected_path = spath
        file_uri = '/' + file_path
        #names = model.get(iter, 0)
        #tree = list(names)
        #file_path = '/'.join(tree)
        #print('[file_uri]: ', file_uri)
        file_type = self.dc.get_file_type(self.container_id, path=file_uri)
        if perms!='directory':
            return
        for name in self.dc.ls(self.container_id, path=file_uri):
            if name in ['.', '..']:
                continue
            props = name.split(' ')
            props = np.array(props)
            props = props[(props!='')]
            #print('[props]:', props, len(props))
            #props = self.remove_empty(props)
            if len(props)<9:
                continue
            nn = name
            created = ' '.join(props[-4:-2])
            owner = ':'.join(props[2:4])
            if props is not None and len(props)==9:
                nn = props[-1]
            elif props is not None and len(props)==10:
                nn = props[-1]
                created = ' '.join(props[-4:-2].tolist())
            elif props is not None and len(props)>9:
                nn = props[-3]
            perms = props[0]
            if perms[0]=='d':
                file_type = 'directory'
            elif perms[0]=='-':
                file_type = 'file'
            elif perms[0]=='l':
                file_type = 'symlink'
            elif perms[0] in ['c', 'b']:
                file_type = 'device'
            elif perms[0]=='s':
                file_type = 'socket'
            elif perms[0]=='p':
                file_type = 'named pipe'
            else:
                file_type = 'unknown'
            row = [nn, file_type, props[4], created, owner, props[0]]
            #print('[row]:', row)
            model.append(iter, row)

    def remove_empty(self, arr):
        def no_empty(var):
            return var!=''
        arr = filter(no_empty, arr)
        return list(arr)
    
    @Gtk.Template.Callback()
    def bCopyToContainer_clicked_cb(self, args):
        copyto = CopyToContainerWindow()
        copyto.show()

    @Gtk.Template.Callback()
    def bCopyFromContainer_clicked_cb(self, args):
        copyfrom = CopyFromContainerWindow()
        copyfrom.show()

    def get_file_path(self, tpath: Gtk.TreePath, model):
        idx = np.array(tpath.get_indices())
        segments = list()
        spath = len(self.selected_path) and self.selected_path or np.empty((0,4))
        arr = np.empty((0,4))
        n_id = 1
        for indx in idx:
            tmp = idx[:n_id]
            path = Gtk.TreePath.new_from_indices(tmp)
            explored = np.where(spath==f'idx={path.to_string()}')
            print('[explored]:', f'idx={path.to_string()}', np.size(explored), explored)
            if np.size(explored)>0:
                continue
            iter = model.get_iter(f'{path}')
            name = model.get_value(iter, 0)
            segments.append(name)
            r = [name, '/'+'/'.join(segments), path.to_string(), f'idx={path.to_string()}']
            arr = np.append(arr, [r], axis=0)
            n_id += 1
        spath = np.append(spath, arr, axis=0)
        #self.selected_path = spath.tolist()
        return ('/'.join(segments), spath.tolist())