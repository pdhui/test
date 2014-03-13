import threading
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
from globalVar import window
import pyHook
import pythoncom
import hotkeyregist

import ctypes
import thread
import win32con
from ctypes import wintypes
from pyhk import pyhk

class ThreadGtk(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)        

    def run(self):
        window.set_keep_above(True)
        window.set_app_paintable(True)

        window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)

        window.connect("expose-event", lambda w, e: getCurrentCoord(w))
        window.connect("expose-event", redraw)
        # window.connect("realize", realize_win)
        window.connect("key-press-event", keyPress)
        window.connect("motion-notify-event", motionNotify)
        window.connect("button-press-event", buttonPress)
        window.connect("button-release-event", buttonRelease)
        window.connect('check-resize', resizemainwin)
        window.connect("destroy", gtk.main_quit)
        window.connect("delete-event", delete_event)

        statusicon.connect('activate', status_clicked )
        statusicon.connect('popup-menu', on_right_click)
        window.show_all()
        while 1:
            a= gtk.events_pending()
            print(a)
            print(gtk.get_current_event())
            gtk.main_iteration()
class ThreadHook(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        byref = ctypes.byref
        user32 = ctypes.windll.user32
        if not user32.RegisterHotKey (None, 1, win32con.MOD_WIN, win32con.VK_F3):
            print "Unable to register id", 1               
        while 1:
            try:
                msg = wintypes.MSG()
                print(msg)
                if user32.GetMessageA (byref (msg), None, 0, 0) != 0:  
                        print(msg)          
                        if msg.message == win32con.WM_HOTKEY:                            
                            if self.HOTKEYS.has_key(msg.wParam):
                                sys.exit()
                                self.__emit = self.HOTKEYS[msg.wParam]
                            user32.TranslateMessage (byref (msg))
                            user32.DispatchMessageA (byref (msg))
            except:
                pass


t = ThreadGtk()
t.start()
t1 = ThreadHook()
t1.start()