from gi.repository import Gtk
from client import Docker

@Gtk.Template.from_file('src/ui/copy_from_container.glade')
class CopyFromContainerWindow(Gtk.Window):
    __gtype_name__ = 'wCopyFromContainer'

    hbCopyFromContainer: Gtk.HeaderBar = Gtk.Template.Child()
    fcwCopyFrom: Gtk.FileChooserWidget = Gtk.Template.Child()
    #txtSaveFilename = Gtk.Template.Child()
    bCancel: Gtk.Button = Gtk.Template.Child()
    bSave: Gtk.Button = Gtk.Template.Child()
    selected_file = None
    selected_file_name = None
    selected_file_uri = None
    current_folder = None
    current_folder_name = None
    current_folder_uri = None

    def __init__(self):
        super().__init__()
        self.dc = Docker()
        if self.fcwCopyFrom is not None:
            self.fcwCopyFrom.set_action(Gtk.FileChooserAction.SAVE)

    @Gtk.Template.Callback()
    def fcwCopyFrom_down_folder_cb(self, args):
        print('[fcwCopyFrom_down_folder_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyFrom_up_folder_cb(self, args):
        print('[fcwCopyFrom_up_folder_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyFrom_current_folder_changed_cb(self, args):
        print('[fcwCopyFrom_current_folder_changed_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyFrom_file_activated_cb(self, args, a, b):
        print('[fcwCopyFrom_file_activated_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyFrom_selection_changed_cb(self, args):
        file = self.fcwCopyFrom.get_file()
        if file is not None:
            filename = file.get_basename()
            self.selected_file = file
            self.selected_file_name = filename
            self.selected_file_uri = self.fcwCopyFrom.get_uri()
        folder = self.fcwCopyFrom.get_current_folder_file()
        if folder is not None:
            folder_name = folder.get_basename()
            folder_uri = self.fcwCopyFrom.get_current_folder_uri()
            self.current_folder = folder
            self.current_folder_name = folder_name
            self.current_folder_uri = folder_uri

    def show(self):
        super().show()
        if self.fcwCopyFrom is not None:
            self.fcwCopyFrom.set_action(Gtk.FileChooserAction.SAVE)

    @Gtk.Template.Callback()
    def fcwCopyFrom_update_preview_cb(self, args):
        print(self.fcwCopyFrom.list_shortcut_folders())
        """ file = self.fcwCopyFrom.get_file()
        if file is not None:
            filename = file.get_basename()
            #print('[fcwCopyFrom_update_preview_cb]:', file, filename)
            self.selected_file = file
            self.selected_file_name = filename
            self.selected_file_uri = self.fcwCopyFrom.get_uri()
        uri = self.fcwCopyFrom.get_uri()
        if uri is not None:
            self.selected_file_uri = uri
        folder = self.fcwCopyFrom.get_current_folder_file()
        if folder is not None:
            folder_name = folder.get_basename()
            folder_uri = self.fcwCopyFrom.get_current_folder_uri()
            #print('[fcwCopyFrom_update_preview_cb]:', folder, folder_name)
            self.current_folder = folder
            self.current_folder_name = folder_name
            self.current_folder_uri = folder_uri """

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        print(self.selected_file_name, self.current_folder_name, self.fcwCopyFrom.get_current_name())
        #self.destroy()

@Gtk.Template.from_file('src/ui/copy_to_container.glade')
class CopyToContainerWindow(Gtk.Window):
    __gtype_name__ = 'wCopyToContainer'

    hbCopyToContainer: Gtk.HeaderBar = Gtk.Template.Child()
    fcwCopyTo: Gtk.FileChooserWidget = Gtk.Template.Child()
    ffCopyTo: Gtk.FileFilter = Gtk.Template.Child()
    #txtCopyFilename = Gtk.Template.Child()
    bCancel: Gtk.Button = Gtk.Template.Child()
    bSave: Gtk.Button = Gtk.Template.Child()
    selected_file = None
    selected_file_name = None
    selected_file_uri = None
    current_folder = None
    current_folder_name = None
    current_folder_uri = None

    def __init__(self):
        super().__init__()
        if self.fcwCopyTo is not None:
            self.fcwCopyTo.set_action(Gtk.FileChooserAction.OPEN)

    @Gtk.Template.Callback()
    def fcwCopyTo_down_folder_cb(self, args):
        print('[fcwCopyTo_down_folder_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyTo_up_folder_cb(self, args):
        print('[fcwCopyTo_up_folder_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyTo_confirm_overwrite_cb(self, args):
        print('[fcwCopyTo_confirm_overwrite_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyTo_current_folder_changed_cb(self, args):
        print('[fcwCopyTo_current_folder_changed_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyTo_file_activated_cb(self, args):
        print('[fcwCopyTo_file_activated_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyTo_selection_changed_cb(self, args):
        print('[fcwCopyTo_selection_changed_cb]:', args)

    @Gtk.Template.Callback()
    def fcwCopyTo_update_preview_cb(self, args):
        print('[fcwCopyTo_update_preview_cb]:', args)

    @Gtk.Template.Callback()
    def bCancel_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bSave_clicked_cb(self, args):
        print(self.selected_file_name, self.current_folder_name, self.fcwCopyTo.get_current_name())

    def show(self):
        super().show()
        if self.fcwCopyTo is not None:
            self.fcwCopyTo.set_action(Gtk.FileChooserAction.OPEN)
