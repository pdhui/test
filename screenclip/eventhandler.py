from draw import *
from globalVar import *
from math import *
import sys
keyBindings = {}
def drawMask(cr):
    if rectWidth > 0:
        mx = ex
        mwidth = rectWidth
    else:
        mx = ex + rectWidth
        mwidth = fabs(rectWidth)
    if rectHeight > 0:
        my = ey
        mheight = rectHeight
    else:
        my = ey + rectHeight
        mheight = fabs(rectHeight)
    cr.set_source_rgba(0, 0, 0, 0.5)
    #draw top
    cr.rectangle(0, 0, mainwidth, my)
    #draw bottom
    cr.rectangle(0, my+mheight, mainwidth, mainheight - my - mheight)
    #draw left
    cr.rectangle(0, my, mx, mheight)
    #draw right
    cr.rectangle(mx + mwidth, my, mainwidth - mx - mwidth, mheight)
    cr.fill()
def keyPress(widget, event):
        '''process key press event'''
        keyEventName = getKeyEventName(event)
        print "keypress %s" % keyEventName
        if keyBindings.has_key(keyEventName):
            keyBindings[keyEventName]()
def registerKeyBinding(keyEventName, callback):
        '''Register a keybinding'''
        keyBindings[keyEventName] = callback
def drawWindowRectangle(cr):
        '''Draw frame.'''
        cr.set_line_width(1)
        cr.rectangle(ex+1, ey+1, rectWidth - 2, rectHeight - 2)
        cr.set_source_rgb(*colorHexToCairo("#00AEFF"))
        cr.stroke()       
def redraw(widget, event):
    cr = widget.window.cairo_create()
    drawPixbuf(cr, desktopBackground)
    drawMask(cr)   
    # drawAlphaRectangle(cr,12,12,240,120)
    # print("redraw: currentX=" + str(currentX))
    if (dragFlag and dragPosition == None) or (not dragFlag and not drawfinish):
        drawMagnifier(cr, window, currentX, currentY,
                           '%d x %d' % (rectWidth, rectHeight),
                            '%s' % ("Tip Drag"), "RGB: %s" % str(getCoordRGB(window, currentX, currentY)))
    if dragFlag or drawfinish:
        drawWindowRectangle(cr)
    if rectWidth != 0 and rectHeight != 0:
        if rectWidth > 0:
            tx = ex
        else:
            tx = ex + rectWidth
        if rectHeight > 0:
            ty = ey 
        else:
            ty = ey + rectHeight
        drawRoundTextRectangle(cr, tx  , ty -32 , 85, 30, 7,'%d x %d' % (fabs(rectWidth), fabs(rectHeight)), 0.7)
    # pixbuf = gtk.gdk.pixbuf_new_from_file("E:/workspace/sublime_workspace/python/screenclip/start_cursor.png")
    # display = window.window.get_display()
    # widget.window.set_cursor(gtk.gdk.Cursor(display, pixbuf, 0, 0))
def realize_win(widget):
    # region = gtk.gdk.region_rectangle(gtk.gdk.Rectangle(50,20,52,32))   
    # widget.window.input_shape_combine_region(region, 0, 0)
    # widget.window.set_back_pixmap(None, False)
    # pixbuf = gtk.gdk.pixbuf_new_from_file("E:/workspace/sublime_workspace/python/screenclip/start_cursor.png")
    display = window.window.get_display()
    widget.window.set_cursor(gtk.gdk.Cursor(display, cursorpixbuf, 0, 0))
def getCurrentCoord(widget):
        '''get Current Coord '''
        global currentX, currentY;
        (currentX, currentY) = widget.window.get_pointer()[:2] 
        # print("currentcoord : currentX=" + str(currentX))
def drawMagnifier(cr, widget, x, y, sizeContent, tipContent = "", rgbContent = "RGB:(255,255,255)"):
    ''' draw Magnifier'''
    
    pixbufWidth = 30
    pixbufHeight = 20
    
    if screenHeight - y < 168:
        offsetY = -34
    else:
        offsetY = 8
    if screenWidth - x < 142:
        offsetX = -33
    else:
        offsetX = 3
    
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, pixbufWidth, pixbufHeight)
    pixbuf.get_from_drawable(widget.get_window(), widget.get_window().get_colormap(),
            int(fabs(x - pixbufWidth / 2)), int(fabs(y - pixbufHeight / 2)),
            0, 0,
            pixbufWidth, pixbufHeight)
    
    #set zoom scale and translate
    cr.save()
    cr.translate(0 - 3 * x, 0 - 3 * y)
    cr.scale(4.0, 4.0)
    
    cr.set_source_rgba(0.0, 0.0, 0.0, 0.8)
    cr.rectangle(x + offsetX - 1, y + offsetY - 1, pixbufWidth + 2, pixbufHeight + 14)
    cr.fill()
    
    #draw magnifier
    cr.set_line_width(1)
    cr.set_source_rgb(1, 1, 1)
    #cr.transform(matrix)
    
    cr.rectangle(x + offsetX, y + offsetY, pixbufWidth, pixbufHeight)
    cr.stroke_preserve()
    cr.set_source_pixbuf(pixbuf, x + offsetX, y + offsetY)
    cr.fill()
    
    #draw Hline
    cr.set_line_width(1.2)
    cr.set_source_rgba(0, 0.7, 1.0, 0.5)
    cr.move_to(x + offsetX , y + offsetY + pixbufHeight / 2)
    cr.line_to(x + offsetX + pixbufWidth, y + offsetY + pixbufHeight / 2)
    cr.stroke()
    
    #draw Vline
    cr.move_to(x + offsetX + pixbufWidth / 2, y + offsetY)
    cr.line_to(x + offsetX + pixbufWidth / 2, y + pixbufHeight + offsetY)
    cr.stroke()
    
    drawFont(cr, sizeContent, 3.0, "#FFFFFF", x + offsetX, y + offsetY + pixbufHeight + 4)
    drawFont(cr, rgbContent, 3.0, "#FFFFFF", x + offsetX, y + offsetY + pixbufHeight + 7.5)
    drawFont(cr, tipContent, 3.0, "#FFFFFF", x + offsetX, y + offsetY + pixbufHeight + 11)
    cr.restore() 
def destroy(widget, data=None):
        '''Destroy main window.'''        
        # gtk.main_quit()
        sys.exit()
   
def getCoordRGB(widget, x, y):
    '''get coordinate's pixel. '''
    width, height = widget.get_size()
    colormap = widget.get_window().get_colormap()
    image = gtk.gdk.Image(gtk.gdk.IMAGE_NORMAL, widget.window.get_visual(), width, height)
    image.set_colormap(colormap)
    # print "getCoordRGB %s x %s" % (x ,y)
    gdkcolor =  colormap.query_color(image.get_pixel(x, y))
    return (gdkcolor.red / 256, gdkcolor.green / 256, gdkcolor.blue / 256)
def motionNotify( widget, event):       
    global rectWidth,rectHeight,ex,ey  
    if dragFlag:
      (x, y) = getEventCoord(event)
      if dragPosition == None:
        (rectWidth, rectHeight) = (x - ex, y - ey)
      elif dragPosition == DRAG_INSIDE:
        ex = min(max(x - dragStartOffsetX, 0), screenWidth - fabs(rectWidth))
        ey = min(max(y - dragStartOffsetY, 0), screenHeight - fabs(rectHeight))
    # print "motionNotify x=%d, y=%d" %(x,y)
    window.queue_draw()
def buttonPress( widget, event):
    global ex,ey,dragFlag, rectHeight, rectWidth, dragPosition, dragStartOffsetY, dragStartOffsetX
    if event.button == 1:        
        x, y = getEventCoord(event)
        dragFlag = True
    elif event.button == 3:
        rectHeight = rectWidth = 0
        ex = ey = -1
        window.queue_draw()
        return

    if drawfinish:
        dragPosition = getPosition(event,(ex,ey,rectWidth,rectHeight))
        # print"buttonPress =%s" %dragPosition
        if dragPosition == DRAG_INSIDE:
            dragStartOffsetX = x - ex
            dragStartOffsetY = y - ey
            return
    ex = x
    ey = y
    window.queue_draw()
def buttonRelease(widget, event):
    global dragFlag,drawfinish,dragPosition
    dragFlag = False
    if rectHeight != 0 or rectWidth != 0:
        drawfinish = True
    else:
        drawfinish = False
    if dragPosition != None:
        dragPosition = None

def resizemainwin(window):
    global mainwidth, mainheight
    mainwidth, mainheight = window.get_size()
def iconify():
    window.iconify()
def showwindow():
    window.deiconify()
def delete_event(window,event):
    window.hide_on_delete()
    return True
def notifyWindowStateChange(window,event):
    # print(event.changed_mask)
    # print(event.new_window_state==gtk.gdk.WINDOW_STATE_ABOVE)
    global SHOWORHIDE
    if event.new_window_state == gtk.gdk.WINDOW_STATE_ICONIFIED | gtk.gdk.WINDOW_STATE_ABOVE:
        print "statechange iconified"
        SHOWORHIDE = False
    elif event.new_window_state == gtk.gdk.WINDOW_STATE_ABOVE:
        print "statechange show"
        SHOWORHIDE = True
    elif event.new_window_state == gtk.gdk.WINDOW_STATE_WITHDRAWN | gtk.gdk.WINDOW_STATE_ABOVE:
        print "statechange hide"
        SHOWORHIDE = False
    elif event.new_window_state == gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_ABOVE:
        print "statechange maximized"
    elif event.new_window_state == gtk.gdk.WINDOW_STATE_FULLSCREEN | gtk.gdk.WINDOW_STATE_ABOVE:
        print "statechange fullscreen"
   
def quitProgram(widget):
    global QUITFlag
    QUITFlag = False
    sys.exit()
def status_clicked(status):
    window.show_all()
    statusicon.set_tooltip("thee window is visible")
    if traymenu:
        traymenu.popdown()
def on_right_click(icon, event_button, event_time):
    global trayshow,traymenu   
    if trayshow or traymenu:
        traymenu.popup(None, None, None,
                event_button, event_time, statusicon)
        return
    trayshow = True
    traymenu = gtk.Menu()
    quit = gtk.ImageMenuItem('Quit')
    quit.set_image(gtk.image_new_from_icon_name('E:/workspace/sublime_workspace/python/screenclip/1.ico', gtk.ICON_SIZE_LARGE_TOOLBAR))
    traymenu.append(quit)
    quit.connect('activate', quitProgram)
    traymenu.show_all()

    traymenu.popup(None, None, None,
                event_button, event_time, statusicon)

def unfullscreen():
    window.unfullscreen()
def hotkeyAction(widget,ev):
    # window.show_all()
    global rootWindow,desktopBackground
    print("hotkeyaction = ",ev)
    if ev == 'screenclipSgn':
        rootWindow = gtk.gdk.get_default_root_window()
        width, height = rootWindow.get_size()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
        desktopBackground = pixbuf.get_from_drawable(
        rootWindow, rootWindow.get_colormap(), 0, 0, 0, 0, width, height)
        if not window.is_active():
            window.present()
        window.queue_draw()
    elif ev == 'minimizeSgn':
        print("minimizeSgn =",window.is_active())
        if window.is_active() :
            iconify()
        else:
            # showwindow()
            # window.set_keep_above(True)
            # window.set_accept_focus(True)
            window.present()           
            # window.show_all()
            # window.grab_focus()

        
