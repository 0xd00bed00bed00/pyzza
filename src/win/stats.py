from gi.repository import Gtk, GLib
from client import Docker
from config import errLogger, appLogger, debugLogger
from utils import notify
from utils import pretty_size
import threading

@Gtk.Template.from_file('src/ui/stats.glade')
class ContainerStatsWindow(Gtk.Window):
    __gtype_name__ = 'wContainerStats'

    hbStats: Gtk.HeaderBar = Gtk.Template.Child()
    lblCpus = Gtk.Template.Child()
    lblCpuPercent = Gtk.Template.Child()
    lblMemUsage = Gtk.Template.Child()
    lblMemPercent = Gtk.Template.Child()
    lblPids = Gtk.Template.Child()
    lblNetIO = Gtk.Template.Child()
    lblBlockIO = Gtk.Template.Child()

    def __init__(self, client: Docker=None, container_name=None):
        super().__init__()
        self.client = client
        self.container_name = container_name
        self.hbStats.set_subtitle(container_name)

    def show(self):
        super().show()
        thd = threading.Thread(target=self.update_stats, daemon=True)
        thd.start()

    def update_stats(self):
        for stats in self.client.container_stats(self.container_name):
            online_cpus = stats['cpu_stats']['online_cpus']
            current_pids = stats['pids_stats']['current']
            cpu_total_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            system_cpu_usage = stats['cpu_stats']['system_cpu_usage']
            mem_usage = stats['memory_stats']['usage']
            mem_limit = stats['memory_stats']['limit']
            eth0 = stats['networks']['eth0']
            net_rx = eth0['rx_bytes']
            net_tx = eth0['tx_bytes']
            cpu_percent = (cpu_total_usage / system_cpu_usage) * online_cpus * 100
            mem_percent = (mem_usage / mem_limit) * 100
            self.lblCpus.set_text(str(online_cpus))
            self.lblPids.set_text(str(current_pids))
            self.lblCpuPercent.set_text(f'{cpu_percent:.2}%')
            self.lblMemUsage.set_text(f'{pretty_size(mem_usage)} / {pretty_size(mem_limit)}')
            self.lblMemPercent.set_text(f'{mem_percent:.2}%')
            self.lblNetIO.set_text(f'{pretty_size(net_rx)} / {pretty_size(net_tx)}')
            self.lblBlockIO.set_text('0B / 0B') #to be implemented