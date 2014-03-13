#!/usr/bin/env python
 
import ctypes
import thread
import win32con
import gobject
from ctypes import wintypes
from pyhk import pyhk
import gtk
from globalVar import *
class keyhandler(gobject.GObject):
        def __init__(self):
                gobject.GObject.__init__(self)
                self.__emit = False
                self.HOTKEYS = {}
                thread.start_new_thread(self.__catchMsgs, tuple())
                gobject.timeout_add(5,self.checkEmit)
                gobject.signal_new(
                        "HOTKEY-PRESS",
                        self.__class__, gobject.SIGNAL_RUN_LAST,
                                gobject.TYPE_BOOLEAN,
                        (gobject.TYPE_STRING,)
                        )
        def checkEmit(self):
                if self.__emit:
                        self.emit('HOTKEY-PRESS',self.__emit)
                        # print 'Emitiendo senial..'
                        self.__emit = False
                return True
 
        def __catchMsgs(self, *args):    
                def funk1():
                        print "Hotkey pressed: Lcontrol 7"  

                # hot = pyhk()
                # id1 = hot.addHotkey(['Ctrl', 'Alt','7'],funk1)
                # hot.start()         
                byref = ctypes.byref
                user32 = ctypes.windll.user32
                # self.HOTKEYS = {1 : win32con.VK_F3,'modifiers': win32con.MOD_WIN}
                VK_A = 0x41
                VK_X = 0x58
                self.HOTKEYS = {
                                  1 : (VK_X, win32con.MOD_CONTROL|win32con.MOD_SHIFT),
                                  2 : (VK_A, win32con.MOD_CONTROL|win32con.MOD_SHIFT)
                                }
                               

                self.HOTKEYS_ACTIONS = {
                        1: 'minimizeSgn',
                        2: 'screenclipSgn'
                }
                # win32con.VK_F3
                for id,(vk,modifier) in self.HOTKEYS.items ():
                        if not user32.RegisterHotKey (None, id, modifier, vk):
                                print "Unable to register id", 1
                
                while QUITFlag:
                        try:
                                msg = wintypes.MSG()
                                if user32.GetMessageA (byref (msg), None, 0, 0):
                                        if msg.message == win32con.WM_HOTKEY:                                                                                              
                                                if self.HOTKEYS.has_key(msg.wParam):                                                        
                                                        self.__emit = self.HOTKEYS_ACTIONS[msg.wParam]
                                                        # self.checkEmit()
                                        user32.TranslateMessage (byref (msg))
                                        user32.DispatchMessageA (byref (msg))
                        except:
                                pass