# coding:utf-8
import gtk
import cairo
import pangocairo
import pango
import gobject
import pygtk
import gtk.gdk as gdk
import sys
from draw import *
from eventhandler import *
from globalVar import *
import pyHook
# import pythoncom
import hotkeyregist

import ctypes
import thread
import win32con
from ctypes import wintypes
from pyhk import pyhk

pygtk.require('2.0')

# window.fullscreen()
window.set_keep_above(True)
window.set_app_paintable(True)
window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
window.add_events(gtk.gdk.POINTER_MOTION_MASK)
window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)

window.connect("expose-event", lambda w, e: getCurrentCoord(w))
window.connect("expose-event", redraw)
window.connect("realize", realize_win)
window.connect("key-press-event", keyPress)
window.connect("motion-notify-event", motionNotify)
window.connect("button-press-event", buttonPress)
window.connect("button-release-event", buttonRelease)
window.connect('check-resize', resizemainwin)
window.connect("destroy", gtk.main_quit)
window.connect("delete-event", delete_event)
window.connect("window-state-event", notifyWindowStateChange)

statusicon.connect('activate', status_clicked )
statusicon.connect('popup-menu', on_right_click)

registerKeyBinding("Escape", lambda : destroy(window))
registerKeyBinding("i", iconify)
registerKeyBinding("f", lambda : window.fullscreen())
registerKeyBinding("u", lambda : window.unfullscreen())
# hm = pyHook.HookManager()
# hm.KeyDown = OnKeyboardEvent
# hm.HookKeyboard()
# pythoncom.PumpMessages()



textWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
textWindow.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
textWindow.set_decorated(False)
textWindow.set_keep_above(True)
textWindow.set_transient_for(window)
textAlign = gtk.Alignment()
textAlign.set(0.5, 0.5, 0, 0)
textAlign.set_padding(10, 10, 10, 10)
textVbox = gtk.VBox()
scrollWindow = gtk.ScrolledWindow()
scrollWindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC) 
textView = gtk.TextView()
textBuffer = textView.get_buffer()
textView.set_wrap_mode(gtk.WRAP_WORD)
textView.set_size_request(300, 60)

scrollWindow.add(textView)
textVbox.pack_start(scrollWindow)
textAlign.add(textVbox)
textWindow.add(textAlign)

textWindow.set_focus(textView)
textWindow.set_position(gtk.WIN_POS_CENTER)

window.show_all()
# textWindow.show_all()
kh = hotkeyregist.keyhandler()
kh.connect("HOTKEY-PRESS", hotkeyAction)
# gtk.main()

while QUITFlag:
    if QUITFlag == False:
        print("has exit")
    a= gtk.events_pending()   
    gtk.main_iteration()
    # print(QUIT)
# hotkeyregist.keyhandler()
# byref = ctypes.byref
# user32 = ctypes.windll.user32
# if not user32.RegisterHotKey (None, 1, win32con.MOD_WIN, win32con.VK_F3):
#     print "Unable to register id", 1               
# while 1:
#     try:
#         msg = wintypes.MSG()
#         if user32.GetMessageA (byref (msg), None, 0, 0) != 0:            
#                 if msg.message == win32con.WM_HOTKEY:
#                     print(msg)
#                     if self.HOTKEYS.has_key(msg.wParam):
#                         sys.exit()
#                         self.__emit = self.HOTKEYS[msg.wParam]
#                     user32.TranslateMessage (byref (msg))
#                     user32.DispatchMessageA (byref (msg))
#     except:
#         pass