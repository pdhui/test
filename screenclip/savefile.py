#!/usr/bin/python
from gi.repository import Gdk
import cairo

def main():
    root_win = Gdk.get_default_root_window()
    width = root_win.get_width()
19
    height = root_win.get_height()
20
     
21
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
22
    pb = Gdk.pixbuf_get_from_window(root_win, 0, 0, width, height)
23
     
24
    cr = cairo.Context(ims)
25
    Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
26
    cr.paint()
27
     
28
    ims.write_to_png("screenshot.png")
29
         
30
if __name__ == "__main__":
31
    main()
