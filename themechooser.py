import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import subprocess
from glob import glob


class MainWindow(Gtk.Window):

    def __init__(self):
        ##Establish css

        css_names = ['#header_label_css{font-weight: 600;margin-left:5px;margin-top:20px;margin-bottom:10px}',
                   '#button_theme_css{margin-left:5px;margin-right:5px;border-color: #111111}']

        for css in css_names:
            style_provider = Gtk.CssProvider()
            val = css
            val = bytes(val, 'utf-8')
            style_provider.load_from_data(val)
            Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        ## Read the themes directory path and remove those not to choose from
        sm_dirs = glob("/usr/share/themes/*/")

        for idx, ele in enumerate(sm_dirs):
            sm_dirs[idx] = ele.replace('/usr/share/themes/', '')

        for idx, ele in enumerate(sm_dirs):
            sm_dirs[idx] = ele.replace('/', '')

        for idx, ele in enumerate(sm_dirs):
            sm_dirs[idx] = ele.replace('_', ' ')

        remove = ["Adwaita-dark", "Adwaita", "Default", "Emacs"]
        sm_dirs = [x for x in sm_dirs if x not in remove]

        app_btn_lbl = ["Light BG/Blue", "Light BG/Green", "Dark BG/Blue", "Dark BG/Green"]
        app_btn_pic = ["/usr/share/customscripts/pythemeselector/lbthumbnail.png",
                       "/usr/share/customscripts/pythemeselector/lgthumbnail.png",
                       "/usr/share/customscripts/pythemeselector/dbthumbnail.png",
                       "/usr/share/customscripts/pythemeselector/dgthumbnail.png", ]

        ##Build the GUI
        Gtk.Window.__init__(self, title="Desktop Theme Chooser")
        self.set_default_size(400, 300)

        main_frame = Gtk.Frame()
        self.grid = Gtk.Grid(column_spacing=1, row_spacing=2)

        main_frame.add(self.grid)
        self.add(main_frame)

        label = Gtk.Label(label="START MENU/TASKBAR")
        label.set_name("header_label_css")
        self.grid.attach(label, 1, 1, 2, 1)

        label = Gtk.Label(label="          ")
        self.grid.attach(label, 3, 1, 2, 1)

        label = Gtk.Label(label="APPLICATIONS")
        label.set_name("header_label_css")
        self.grid.attach(label, 5, 1, 2, 1)

        rowcount = 1
        for item in sm_dirs:
            rowcount += 1
            button = Gtk.Button(label=item)
            button._value = item
            button.set_name("button_theme_css")
            self.grid.attach(button, 1, rowcount, 1, 1)
            button.connect("clicked", self.sm_button_clicked)
            item = item.replace(" ", "_")

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename='/usr/share/themes/' + item + '/cinnamon/thumbnail.png',
                width=25,
                height=25,
                preserve_aspect_ratio=True)

            img = Gtk.Image.new_from_pixbuf(pixbuf)
            img.set_name("button_theme_css")
            self.grid.attach(img, 2, rowcount, 1, 1)

        rowcount = 1
        for item in app_btn_lbl:
            rowcount += 1
            button = Gtk.Button(label=item)
            button._value = item
            button.set_name("button_theme_css")
            self.grid.attach(button, 5, rowcount, 1, 1)
            button.connect("clicked", self.at_button_clicked)

        rowcount = 1
        for item in app_btn_pic:
            rowcount += 1

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=item,
                width=100,
                height=100,
                preserve_aspect_ratio=True)

            img = Gtk.Image.new_from_pixbuf(pixbuf)
            img.set_name("button_theme_css")
            self.grid.attach(img, 6, rowcount, 1, 1)

    def sm_button_clicked(self, button):
        theme = button._value.replace(" ", "_")
        if theme:
            subprocess.Popen(["gsettings", "set", "org.cinnamon.theme", "name", theme])

    def at_button_clicked(self, button):
        theme = button._value.replace(" ", "")
        theme = theme.replace("/", "")

        if theme == "DarkBGGreen":
            subprocess.Popen(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", "Dark"])

        if theme == "DarkBGBlue":
            subprocess.Popen(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", "Adwaita-dark"])

        if theme == "LightBGGreen":
            subprocess.Popen(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", "Opaque"])

        if theme == "LightBGBlue":
            subprocess.Popen(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", "Adwaita"])


window = MainWindow()
window.connect("delete_event", Gtk.main_quit)
window.show_all()
Gtk.main()
