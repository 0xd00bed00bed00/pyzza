import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Vte', '2.91')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GObject, Vte, Notify, Gio
from windows import *

GObject.type_register(Vte.Terminal)

class Pyzza(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        Notify.is_initted() or Notify.init('pyzza')
        self.window = None

    def do_activate(self):
        self.window = self.window or MainWindow(application=self)
        self.window.present()

def main():
    try:
        # get_priv()
        app = Pyzza()
        app.run(sys.argv)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()