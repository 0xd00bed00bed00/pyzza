from gi.repository import Gtk
from slugify import slugify
from args import RunContanerKwargs
from win.term import exec
import threading

@Gtk.Template.from_file('src/ui/run_container_opts.glade')
class RunContainerOptsWindow(Gtk.Window):
    __gtype_name__ = 'wRunContainerOpts'

    txtiImageName = Gtk.Template.Child()
    txtiContainerName = Gtk.Template.Child()
    txtiCommand = Gtk.Template.Child()
    txtiWorkingDir = Gtk.Template.Child()
    txtRunContainerUser = Gtk.Template.Child()
    txtRunContainerHostname = Gtk.Template.Child()
    chRunContainerTty = Gtk.Template.Child()
    chRunContainerStream = Gtk.Template.Child()
    chRunContainerStdout = Gtk.Template.Child()
    chRunContainerStderr = Gtk.Template.Child()
    chRunContainerStdin = Gtk.Template.Child()
    chRunContainerDetach = Gtk.Template.Child()
    chRunContainerPrivileged = Gtk.Template.Child()
    chRunContainerNetDisabled = Gtk.Template.Child()

    fromSearch = False
    imageName = None
    containerName = None
    command = None

    def __init__(self, image_name=None, container_name=None, cmd=None, from_search=False, client=None):
        super().__init__()
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
        kwargs = RunContanerKwargs(image=image, name=container, command=cmd, working_dir=wdir, tty=tty, stream=stream, stdout=stdout, stderr=stderr, stdin_open=stdin, detach=detach, privileged=priv, network_disabled=netdis, user=user, hostname=host)
        th = threading.Thread(target=self.dc.run_container, args=[kwargs], daemon=True)
        th.start()
        
        if not self.fromSearch: self.destroy()

    def show(self):
        super().show()
        self.txtiImageName.set_text(self.imageName)
        self.txtiContainerName.set_text(self.containerName)
        self.txtiCommand.set_text(self.command)