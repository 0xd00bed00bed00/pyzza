import gi, os, sys
print(os.getcwd())
gi.require_version("Gtk", "3.0")
gi.require_version('Vte', '2.91')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GObject, Vte, Notify, Gio
from windows import MainWindow
from constants import APP_ID
from config import ConfigManager
from client import Docker
from dotenv import load_dotenv
from os import path
from common import getconfigpath, gettmpdir, checkpaths
import faulthandler, os
import os

GObject.type_register(Vte.Terminal)

dirname = gettmpdir()
if not path.isdir(dirname):
    os.mkdir(dirname)

class Pyzza(Gtk.Application):
    dc: Docker = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        Notify.is_initted() or Notify.init('pyzza')
        self.window = None
        ConfigManager.init()

    def do_activate(self):
        self.window = self.window or MainWindow(application=self)
        self.window.present()

def main():
    load_dotenv()
    try:
        faulthandler.enable()
        checkpaths()
        app = Pyzza()
        app.run(sys.argv)
    except KeyboardInterrupt:
        print('\nctrl+c detected. Shutting down')

if __name__ == '__main__':
    main()