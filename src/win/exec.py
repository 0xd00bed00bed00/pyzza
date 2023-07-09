from gi.repository import Gtk
from client import Docker
from windows import TerminalWindow

@Gtk.Template.from_file('src/ui/exec_container_opts.glade')
class ExecContainerOptsWindow(Gtk.Window):
    __gtype_name__ = 'wExecOpts'

    hbExecOpts: Gtk.HeaderBar = Gtk.Template.Child()
    bExecOptsCancel: Gtk.Button = Gtk.Template.Child()
    bExecOptsStart = Gtk.Template.Child()
    txtContainer = Gtk.Template.Child()
    txtCommand = Gtk.Template.Child()
    txtEnv = Gtk.Template.Child()
    txtWorkingDir = Gtk.Template.Child()
    chInteractive = Gtk.Template.Child()
    chTty = Gtk.Template.Child()
    chPrivileged = Gtk.Template.Child()
    chDetach = Gtk.Template.Child()
    container = None

    def __init__(self, container=None):
        super().__init__()
        self.dc = Docker()
        self.container = container
        c, cc = container
        (name, cmd) = c[1], c[2]
        self.hbExecOpts.set_subtitle(name)
        self.txtContainer.set_text(name)
        self.txtContainer.set_editable(False)
        self.txtCommand.set_text(cmd)
    
    @Gtk.Template.Callback()
    def bExecOptsStart_clicked_cb(self, args):
        c, cc = self.container
        (id, cmd) = c[0], c[2]
        name = self.txtContainer.get_text()
        cmd = self.txtCommand.get_text()
        #env = self.txtEnv.get_text()
        #wdir = self.txtWorkingDir.get_text()
        int = self.chInteractive.get_active()
        tty = self.chTty.get_active()
        detach = self.chDetach.get_active()
        priv = self.chPrivileged.get_active()
        lflags = []
        if int:
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

        term = TerminalWindow(name=name or id, flags=lflags, cmd=cmd)
        term.spawn()
        term.show()
        self.destroy()

    @Gtk.Template.Callback()
    def bExecOptsCancel_clicked_cb(self, args):
        self.destroy()