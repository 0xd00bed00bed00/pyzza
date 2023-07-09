from gi.repository import Gtk
from args import *
from client import Docker
from constants import *
from common import ModelType
from utils import *
from win.term import exec

@Gtk.Template.from_file('src/ui/build_image.glade')
class ImageBuildWindow(Gtk.Window):
    __gtype_name__ = 'wBuildImage'

    fcbPath = Gtk.Template.Child()
    txtTag = Gtk.Template.Child()
    chQuiet = Gtk.Template.Child()
    chRm = Gtk.Template.Child()
    chNoCache = Gtk.Template.Child()
    chPull = Gtk.Template.Child()
    chSquash = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    @Gtk.Template.Callback()
    def fcbPath_file_set_cb(self, args):
        print('fcbPath_file_set_cb#args:', args)

    @Gtk.Template.Callback()
    def fcbPath_current_folder_changed_cb(self, args):
        print('fcbPath_current_folder_changed_cb#args:', args)

    @Gtk.Template.Callback()
    def fcbPath_selection_changed_cb(self, args):
        print('fcbPath_selection_changed_cb#args:', args)

    @Gtk.Template.Callback()
    def fcbPath_update_preview_cb(self, args):
        print('fcbPath_update_preview_cb#args:', args)

    @Gtk.Template.Callback()
    def fcbPath_file_activated_cb(self, args):
        print('fcbPath_file_activated_cb#args:', args)

    @Gtk.Template.Callback()
    def bCancelBuild_clicked_cb(self, args):
        self.destroy()

    @Gtk.Template.Callback()
    def bBuild_clicked_cb(self, args):
        uri = str(self.fcbPath.get_uri())
        uri = uri.replace('file://', '')
        tag = self.txtTag.get_text()
        quiet = self.chQuiet.get_active()
        rm = self.chRm.get_active()
        nocache = self.chNoCache.get_active()
        pull = self.chPull.get_active()
        squash = self.chSquash.get_active()
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
        exec('build image', argv=argv)

        self.destroy()