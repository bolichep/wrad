#!/usr/bin/python -tt

import gtk
import gst

Incr = 200000000
Delay = 0
RegDelay = 0
#label0 = None

def on_buttonX_clicked(widget):
    return

def abutton(abox="", label="",event="",callback=on_buttonX_clicked):
    buttonX = gtk.Button(label)
    buttonX.connect("clicked", callback)
    abox.pack_start(buttonX, True, True, 0)
    return buttonX
    


def Window():
    global button1
    global button5
    global label0

    window = gtk.Window()
    window.set_default_size(350,35)
    window.set_position(gtk.WIN_POS_CENTER)
    window.connect("destroy", lambda w: gtk.main_quit())


    box = gtk.HBox(spacing=6)
    window.add(box)

    button0 = abutton(abox=box,label="Dec",event="clicked",callback=on_buttonDec_clicked)
    button1 = abutton(abox=box,label="Start",event="clicked",callback=on_buttonStart_clicked)
    button2 = abutton(abox=box,label="Inc",event="clicked",callback=on_buttonInc_clicked)
    label0 = gtk.Label()
    label0.set_text("Delay")
    box.pack_start(label0, True, True, 0)
    button3 = abutton(abox=box,label="Reset",event="clicked",callback=on_buttonReset_clicked)
    button4 = abutton(abox=box,label="Save",event="clicked",callback=on_buttonSave_clicked)
    button5 = abutton(abox=box,label="Restore",event="clicked",callback=on_buttonRestore_clicked)
    button5.set_sensitive(False)

    window.show_all()
    QueueRun()

def QueueRun():
    global delay_pipeline
    global audioqueue

    delay_pipeline = gst.Pipeline("pipeline")
    delay_pipeline.set_property("auto-flush-bus", False)
    #ALSA
    audiosrc = gst.element_factory_make("alsasrc", "audio")
    audiosrc.set_property("device","default")
    delay_pipeline.add(audiosrc)
    #Queue
    audioqueue = gst.element_factory_make("queue","queue1")
    audioqueue.set_property("max-size-time",0)
    audioqueue.set_property("max-size-buffers",0)
    audioqueue.set_property("max-size-bytes",0)
    audioqueue.set_property("min-threshold-time",Delay)
    audioqueue.set_property("leaky","no")
    delay_pipeline.add(audioqueue)
    #Audio Output
    sink = gst.element_factory_make("autoaudiosink", "sink")
    delay_pipeline.add(sink)
    #Link the elements
    audiosrc.link(audioqueue)
    audioqueue.link(sink)
    #Begin Playing
    # delay_pipeline.set_state(gst.STATE_PLAYING)

def changeDelay():
    global label0

    label0.set_text(str(float(Delay/float(1000000000))))			
    delay_pipeline.set_state(gst.STATE_NULL)
    audioqueue.set_property("min-threshold-time",Delay)		
    delay_pipeline.set_state(gst.STATE_PLAYING)


def on_buttonStart_clicked(widget):
    global button1
    changeDelay()			
    button1.set_label("Stop")
    button1.connect("clicked", on_buttonStop_clicked)

def on_buttonStop_clicked(widget):		
    global button1
    button1.set_label("Start")
    button1.connect("clicked", on_buttonStart_clicked)
    delay_pipeline.set_state(gst.STATE_NULL)
    return

def on_buttonDec_clicked(widget):		
    global Delay
    global button1
    Delay = Delay - Incr
    if (Delay < 0):
        Delay = 0
        #print "Dec DELAY", DELAY
        button1.set_label("Stop")
        button1.connect("clicked", on_buttonStop_clicked)
    changeDelay()
    return

def on_buttonInc_clicked(widget):
    global Delay
    global button1
    Delay = Delay + Incr
    #print "Inc DELAY", DELAY
    changeDelay()	
    button1.set_label("Stop")
    button1.connect("clicked", on_buttonStop_clicked)
    return

def on_buttonSave_clicked(widget):
    global RegDelay
    global button5
    
    button5.set_sensitive(True)
    RegDelay = Delay
    changeDelay()
    return

def on_buttonReset_clicked(widget):
    global Delay
    global button1
    Delay = 0
    changeDelay()
    button1.set_label("Stop")
    button1.connect("clicked", on_buttonStop_clicked)
    return

def on_buttonRestore_clicked(widget):
    global Delay
    global RegDelay
    if ( RegDelay != 0):
        Delay = RegDelay
    changeDelay()
    return

    
def main():
    Window()
    gtk.main()

if __name__ == '__main__':
  main()
    
    
