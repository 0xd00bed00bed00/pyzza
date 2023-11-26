import gi, os, sys
#print(os.getcwd())
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('Notify', '0.7')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, GObject, Vte, Notify, Gio
from windows import MainWindow
from constants import APP_ID
from config import ConfigManager, LogConfig, appLogger, debugLogger, warnLogger, errLogger
from client import Docker
from dotenv import load_dotenv
from os import path
from common import gettmpdir, checkpaths, DEBUG, ENV, getconfigdir, getlogdir
from multiprocessing import Process, cpu_count
import faulthandler, os, logging, logging.config, logging.handlers, subprocess

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
        print('[app]:', type(self.window), isinstance(self.window, Gtk.ApplicationWindow))
        self.window.present()

def main():
    load_dotenv()
    checkpaths()
    LogConfig.writedefaultconfig()
    logging.config.fileConfig(LogConfig.getconfigfile())
    logging.info('Logger initialized')
    appLogger.info('app launched successfully')
    try:
        faulthandler.enable()
        app = Pyzza()
        app.run(sys.argv)
    except KeyboardInterrupt:
        errLogger.error('\nctrl+c detected. Shutting down', exc_info=True)

if __name__ == '__main__':
    main()