#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Program:      Python digital clock applications
# Author:       Elvis Baketa
# Version:      0.2
#               Python 3
#               PyGObject

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Pango

import time

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Digital clock")
        self.connect("delete-event", Gtk.main_quit)
        self.connect("key-press-event",self.on_key_press_event)
        self.connect("realize", self.on_realize)
        # set base window background color
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#000000"))
        # set default window size
        self.set_default_size(320, 240)
        # set window position
        self.set_position(Gtk.WindowPosition.CENTER)

        # fullscreen toggling variable
        self.fullscreen_toggler = True
        # hide mouse pointer toggling variable
        self.mousePointer_toggler = False

        # wrapper for holding all elements of a window
        wrapper = Gtk.Box()
        wrapper.set_orientation(Gtk.Orientation.VERTICAL)
        # wrapper.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#222222"))
        wrapper.set_margin_top(5)
        wrapper.set_margin_bottom(5)
        wrapper.set_margin_start(5)
        wrapper.set_margin_end(5)
        self.add(wrapper)

        # time label
        self.lblTime = Gtk.Label()
        self.lblTime.set_alignment(0.5, 1)
        self.lblTime.modify_font(Pango.FontDescription('96'));
        # self.lblTime.set_text("")
        wrapper.pack_start(self.lblTime, True, True, 0)

        # date label
        self.lblDate = Gtk.Label()
        self.lblDate.set_alignment(0.5, 0)
        self.lblDate.set_margin_start(5)
        self.lblDate.set_margin_end(5)
        self.lblDate.modify_font(Pango.FontDescription('24'));
        # self.lblDate.set_text("")
        wrapper.pack_start(self.lblDate, True, True, 0)

    def on_realize(self, widget, data=None):
        self.timeUpdateInterval()
        self.updateDisplay()
        self.fulscreenMode()
        self.hideShowMousePointer()

    # function to update display
    def updateDisplay(self):
        self.timeUpdateInterval()
        self.updateTime()
        self.updateDate()

    # function to toggle between fullscreen and windowed mode
    def fulscreenMode(self):
        # show in fullscreen and hide mouse pointer
        if self.fullscreen_toggler == True:
            self.fullscreen()
            self.mousePointer_toggler = True
        # show in windowed mode and show mouse pinter
        elif self.fullscreen_toggler == False:
            self.unfullscreen()
            self.mousePointer_toggler = False
        else:
            pass

    # function to hide or show mouse pointer
    # must be called after the realization of the display
    def hideShowMousePointer(self):
        # hide mouse pointer
        if self.mousePointer_toggler == True:
            display = self.get_display()
            cursor = Gdk.Cursor.new_for_display(display, Gdk.CursorType.BLANK_CURSOR)
            self.get_window().set_cursor(cursor)
        # show mouse pointer
        elif self.mousePointer_toggler == False:
            display = self.get_display()
            cursor = Gdk.Cursor.new_for_display(display, Gdk.CursorType.TOP_LEFT_ARROW)
            self.get_window().set_cursor(cursor)
        else:
            pass

    # function to fetch current time
    def fetchTime(self):
        currentTime=time.localtime()
        return currentTime

    # function to calculate update interal
    def timeUpdateInterval(self):
        currentTime = self.fetchTime()
        timeSecond = time.strftime("%S", currentTime)
        nextUpdateInterval = 60 - int(timeSecond)
        if nextUpdateInterval == 0:
            nextUpdateInterval = 60
        GLib.timeout_add_seconds(nextUpdateInterval, self.updateDisplay)

    # function to updaet time label
    def updateTime(self):
        self.lblTime.set_text(time.strftime("%H:%M", self.fetchTime()))

    # function to update date label
    def updateDate(self):
        self.lblDate.set_text(time.strftime("%A, %d. %b %Y", self.fetchTime()))

    # function to resolve key press events
    def on_key_press_event(self, widget, event):
        if event.keyval == Gdk.KEY_F11:
            self.fullscreen_toggler = not self.fullscreen_toggler
            self.fulscreenMode()
            self.hideShowMousePointer()
        else:
            pass

if __name__ == "__main__":
    win = MyWindow()
    win.show_all()
    Gtk.main()
