import sys
from ctypes import *
from ctypes.wintypes import *
import threading
import gtk
import cairo
import pangocairo

# Define the Windows DLLs, constants and types that we need.
user32 = windll.user32

WM_HOTKEY = 0x0312
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004

class MSG(Structure):
    _fields_ = [('hwnd', c_int),
    ('message', c_uint),
    ('wParam', c_int),
    ('lParam', c_int),
    ('time', c_int),
    ('pt', POINT)]



class KeyCatch(threading.Thread):

    def run(self):

        print "TESTING TO MAKE SURE THREAD IS RUNNING!"
        # Register a hotkey for Ctrl+Shift+P.
        hotkeyId = 1
        if not user32.RegisterHotKey(None, hotkeyId, MOD_CONTROL |MOD_SHIFT, ord('P')):
            sys.exit("Failed to register hotkey; maybe someone elseregistered it?")
        # Spin a message loop waiting for WM_HOTKEY.
        while 1 :

            msg = MSG()
            while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
                print(msg)
                if msg.message == WM_HOTKEY and msg.wParam ==hotkeyId:
                    print "Yay"
                    windll.user32.PostQuitMessage(0)
                user32.TranslateMessage(byref(msg))
                user32.DispatchMessageA(byref(msg))

def redraw(widget, event):  
    print("redraw")
    
GetKey = KeyCatch()
GetKey.start()
# while 1:
#     pass
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_keep_above(True)
window.connect("expose-event", redraw)

window.show_all()
while 1:
    a= gtk.events_pending()
    print(a)
    gtk.main_iteration()
