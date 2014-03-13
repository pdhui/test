import gtk
import gtk.gdk as gdk
from globalVar import *
def getKeyName(keyval):
    '''Get key name.'''
    keyUnicode = gdk.keyval_to_unicode(keyval)
    if keyUnicode == 0:
        return gdk.keyval_name(keyval)
    else:
        return str(unichr(keyUnicode))
    
def getKeyEventModifiers(keyEvent):
    '''Get key event modifiers.'''
    modifiers = []
    
    # Add Ctrl modifier.
    if keyEvent.state & gdk.CONTROL_MASK:
        modifiers.append("C")
        
    # Add Alt modifier.
    if keyEvent.state & gdk.MOD1_MASK:
        modifiers.append("M")
        
    # Don't need add Shift modifier if keyval is upper character.
    if keyEvent.state & gdk.SHIFT_MASK and not gdk.keyval_is_upper(keyEvent.keyval):
        modifiers.append("S")
        
    return modifiers

def getKeyEventName(keyEvent):
    '''Get key event name.'''
    if keyEvent.is_modifier:
        return ""
    else:
        keyModifiers = getKeyEventModifiers(keyEvent)
        keyName = getKeyName(keyEvent.keyval)
        
        if keyModifiers == []:
            return keyName
        else:
            return "-".join(keyModifiers) + "-" + keyName
def colorHexToCairo(color):
    """ 
    Convert a html (hex) RGB value to cairo color. 
     
    @type color: html color string 
    @param color: The color to convert. 
    @return: A color in cairo format. 
    """ 
    if color[0] == '#': 
        color = color[1:] 
    (r, g, b) = (int(color[:2], 16), 
                    int(color[2:4], 16),  
                    int(color[4:], 16)) 
    return colorRGBToCairo((r, g, b)) 

def colorRGBToCairo(color): 
    """ 
    Convert a 8 bit RGB value to cairo color. 
     
    @type color: a triple of integers between 0 and 255 
    @param color: The color to convert. 
    @return: A color in cairo format. 
    """ 
    return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
def getEventCoord(event):
        '''Get event coord.'''
        (rx, ry) = event.get_coords()
        return (int(rx), int(ry))
def getPosition( event,(ex,ey,width,heigth)):
    (x, y) = getEventCoord(event)
    if width < 0:
        ex = ex + width
        width = -width
    if heigth < 0:
        ey = ey + heigth
        heigth = -heigth
    if isInRect((x, y), (ex, ey, width, heigth)):
        return DRAG_INSIDE
def isInRect((cx, cy), (x, y, w, h)):
    '''Whether coordinate in rectangle.'''
    return (x < cx < x + w and y < cy < y + h)
