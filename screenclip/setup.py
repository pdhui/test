from distutils.core import setup
import py2exe
import os
import sys
# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

setup(
    name = 'handytool',
    description = 'Some handy tool',
    version = '1.0',
    zipfile = None,
    windows = [
                  {
                      'script': 'gtktest2.py',
                      'icon_resources': [(1, "1.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings, pygtk, gtk, glib, gobject',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes': 'cairo, pangocairo, gio, atk, pango',
                      # "bundle_files": 1,
                  }
              },

    data_files=[
                   # 'handytool.glade',
                   # 'readme.txt',
                   # If using GTK+'s built in SVG support, uncomment these
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll'),
               ]
)