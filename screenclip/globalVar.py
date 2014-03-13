import gtk
import gobject

currentX = currentY = 12 
ex = ey = 0
dragFlag = False
drawfinish = False
rectWidth=0
rectHeight=0      
trayshow = False
traymenu = None
QUITFlag = True
SHOWORHIDE = True
DRAG_INSIDE = 1
dragPosition = None
dragStartOffsetX = dragStartOffsetY = 0

cursorpixbuf = gtk.gdk.pixbuf_new_from_file("start_cursor.png")
rootWindow = gtk.gdk.get_default_root_window()
(screenWidth, screenHeight) = rootWindow.get_size()
pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, screenWidth, screenHeight)
desktopBackground = pixbuf.get_from_drawable(
    rootWindow, rootWindow.get_colormap(), 0, 0, 0, 0, screenWidth, screenHeight)

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_can_focus(True)
window.resize(600,400)
mainwidth, mainheight = window.get_size()

# statusicon = gtk.status_icon_new_from_stock(gtk.STOCK_GOTO_TOP)
statusicon = gtk.StatusIcon()
statusicon.set_from_file('E:/workspace/sublime_workspace/python/screenclip/1.ico')
statusicon.set_visible(True)



