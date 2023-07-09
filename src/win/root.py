from gi.repository import Gtk
from slugify import slugify
from args import *
from client import Docker
from constants import *
from common import ModelType
from utils import *
import threading, json, numpy as np

class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'main_window'
    selected_tab = None

    MainBox = Gtk.Template.Child()
    nb1: Gtk.Notebook = Gtk.Template.Child()

    hbMain: Gtk.HeaderBar = Gtk.Template.Child()

    bStopContainer: Gtk.Button = Gtk.Template.Child()
    bRestartContainer: Gtk.Button = Gtk.Template.Child()
    bKillContainer: Gtk.Button = Gtk.Template.Child()
    bExecContainer: Gtk.Button = Gtk.Template.Child()
    bAttachContainer: Gtk.Button = Gtk.Template.Child()
    bInspect: Gtk.Button = Gtk.Template.Child()
    bSuspendContainer: Gtk.Button = Gtk.Template.Child()
    bContainerLogs: Gtk.Button = Gtk.Template.Child()
    bResumeContainer: Gtk.Button = Gtk.Template.Child()
    bContainerTop: Gtk.Button = Gtk.Template.Child()
    bRenameContainer: Gtk.Button = Gtk.Template.Child()
    bExportContainer: Gtk.Button = Gtk.Template.Child()
    bDiffContainer: Gtk.Button = Gtk.Template.Child()
    bBrowse: Gtk.Button = Gtk.Template.Child()
    bStartContainer: Gtk.Button = Gtk.Template.Child()
    bRunContainer: Gtk.Button = Gtk.Template.Child()
    bImageHistory: Gtk.Button = Gtk.Template.Child()
    bSaveImage: Gtk.Button = Gtk.Template.Child()
    bImportImage: Gtk.Button = Gtk.Template.Child()
    bPruneContainers: Gtk.Button = Gtk.Template.Child()
    bPruneImages: Gtk.Button = Gtk.Template.Child()
    bBuildImage: Gtk.Button = Gtk.Template.Child()
    bCreateImage: Gtk.Button = Gtk.Template.Child()
    bCreateContainer: Gtk.Button = Gtk.Template.Child()
    bLoadImage: Gtk.Button = Gtk.Template.Child()
    bSearchRunContainer: Gtk.Button = Gtk.Template.Child()
    bPullImage: Gtk.Button = Gtk.Template.Child()

    dashboardTree: Gtk.TreeView = Gtk.Template.Child()
    dashboardStore: Gtk.ListStore = Gtk.Template.Child()

    containersTree: Gtk.TreeView = Gtk.Template.Child()
    containersStore: Gtk.ListStore = Gtk.Template.Child()

    imagesTree: Gtk.TreeView = Gtk.Template.Child()
    imagesStore: Gtk.ListStore = Gtk.Template.Child()

    volumesTree: Gtk.TreeView = Gtk.Template.Child()
    volumesStore: Gtk.ListStore = Gtk.Template.Child()

    networksTree: Gtk.TreeView = Gtk.Template.Child()
    networksStore: Gtk.ListStore = Gtk.Template.Child()

    searches = None
    searchStore: Gtk.ListStore = Gtk.Template.Child()

    lDashboard: Gtk.Label = Gtk.Template.Child()
    lContainers: Gtk.Label = Gtk.Template.Child()
    lImages: Gtk.Label = Gtk.Template.Child()
    lVolumes: Gtk.Label = Gtk.Template.Child()
    lNetworks: Gtk.Label = Gtk.Template.Child()

    term: Vte.Terminal = Gtk.Template.Child()
    txtSearchImage: Gtk.Entry = Gtk.Template.Child()

    selected_id = None
    selected_name = None
    selection = None

    selected_running_container = None
    selected_container = None
    selected_image = None
    selected_volume = None
    selected_network = None

    dashboard_cursor_moved = False
    containers_cursor_moved = False
    images_cursor_moved = False
    volumes_cursor_moved = False
    networks_cursor_moved = False
    search_cursor_moved = False
    fromSearch = False

    running_containers = None
    containers = None
    images = None
    volumes = None
    networks = None