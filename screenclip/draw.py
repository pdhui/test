# coding:utf-8
import pangocairo
import cairo
from math import *
from util import *

def drawPixbuf(cr, pixbuf, x=0, y=0):
    '''Draw pixbuf.'''
    if pixbuf != None:
        # print "drawPixbuf"
        cr.set_source_pixbuf(pixbuf, x, y)
        cr.paint()
def drawAlphaRectangle(cr, x, y, width, height):
    ''' draw alpha Rectangle '''
    cr.set_source_rgba(0.18, 0.62, 0.18, 0.6)
    cr.rectangle(x, y, width, height)
    cr.stroke_preserve()
    #cr.stroke()
    cr.set_source_rgba(0, 0.7, 1.0, 0.4)
    cr.fill()
def drawRoundTextRectangle(cr, x, y, width, height, r, Text, alpha=0.8):
    ''' draw Round Text Rectangle''' 
    cr.set_source_rgba(0.14, 0.13, 0.15, alpha)
    cr.move_to(x+r, y)
    cr.line_to(x+width-r,y)
        
    cr.move_to(x+width, y+r)
    cr.line_to(x+width, y+height - r)
        
    cr.move_to(x+width-r,y+height)
    cr.line_to(x+r, y+height)
        
    cr.move_to(x, y+height-r)
    cr.line_to(x, y+r)
    cr.arc(x+r, y+r, r, pi, 3*pi / 2)
    cr.arc(x+width-r,y+r,r, 3*pi / 2, 2*pi)
    cr.arc(x+width-r, y+height-r, r, 2*pi, pi / 2)
    cr.arc(x+r, y+height-r, r, pi / 2, pi)    
    cr.fill()
        
    drawFont(cr, Text, 14.0, "#FFFFFF", x + width / 12.0, y + height / 1.5)    
def drawFont(cr, content, fontSize, fontColor, x, y):
    '''Draw font.'''
    DEFAULT_FONT = "文泉驿微米黑"
    if DEFAULT_FONT in getFontFamilies():
        cr.select_font_face(DEFAULT_FONT,
                            cairo.FONT_SLANT_NORMAL, 
                            cairo.FONT_WEIGHT_NORMAL)
    cr.set_source_rgb(*colorHexToCairo(fontColor))
    cr.set_font_size(fontSize)
    cr.move_to(x, y)
    cr.show_text(content)
def getFontFamilies():
    '''Get all font families in system.'''
    fontmap = pangocairo.cairo_font_map_get_default()
    return map(lambda f: f.get_name(), fontmap.list_families()) 