from gi.repository import Gtk, GLib

@Gtk.Template.from_file('src/ui/operation_progress.glade')
class OperationProgressWindow(Gtk.Window):
    __gtype_name__ = 'wOperationProgress'

    pbOperation = Gtk.Template.Child()
    hbOperationProgress: Gtk.HeaderBar = Gtk.Template.Child()

    isdone = False
    iserror = False

    def __init__(self, show_progress_text=True, subtitle=None):
        super().__init__()
        self.timer = GLib.timeout_add(100, self.progress_timeout)
        self.pbOperation.set_show_text(show_progress_text)
        self.hbOperationProgress.set_subtitle(subtitle)
        self.hbOperationProgress.set_show_close_button(False)

    def progress_timeout(self):
        self.pbOperation.pulse()
        if self.isdone:
            self.pbOperation.set_fraction(1.0)
        #self.pbOperation.set_show_text(True)
        self.hbOperationProgress.set_show_close_button(True)
        return not self.isdone and not self.iserror

    def show(self):
        super().show()