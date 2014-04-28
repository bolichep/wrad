#!/usr/bin/python -tt

from gi.repository import Gtk
import pygst
#pygst.require("0.10")
import gst
#import pygtk
import sys

#INCR = 1000000000
INCR = 200000000
DELAY = 0
REGDELAY = 0
class  WradWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Audio Delay")

		self.set_size_request(350, 35)
		self.set_position(Gtk.WindowPosition.CENTER)

		self.box = Gtk.Box(spacing=6 , orientation = Gtk.Orientation.HORIZONTAL)
		self.add(self.box)

		self.button0 = Gtk.Button(label="Start") # Boton Start/Stop
		self.button1 = Gtk.Button(label="Inc")
		self.button2 = Gtk.Button(label="Dec")
		self.button3 = Gtk.Button(label="Reset")
		self.button4 = Gtk.Button(label="Save")
		self.button5 = Gtk.Button(label="Restore")

		self.button0.connect("clicked", self.on_buttonSTART_clicked)
		self.button1.connect("clicked", self.on_buttonINC_clicked)
		self.button2.connect("clicked", self.on_buttonDEC_clicked)
		self.button3.connect("clicked", self.on_buttonRST_clicked)
		self.button4.connect("clicked", self.on_buttonSAV_clicked)
		self.button5.connect("clicked", self.on_buttonRES_clicked)


		self.box.pack_start(self.button2, True, True, 0 )
		self.box.pack_start(self.button0, True, True, 0 )
		self.box.pack_start(self.button1, True, True, 0 )

		self.label = Gtk.Label() # Current Delay Label
		self.label.set_text("Delay")
		self.box.pack_start(self.label, True, True, 0 )	
		
		self.box.pack_start(self.button3, True, True, 0 )				

		self.box.pack_start(self.button4, True, True, 0 )
		self.box.pack_start(self.button5, True, True, 0 )

		self.QueueRun()

	def QueueRun(self):
		self.delay_pipeline = gst.Pipeline("mypipeline")
		self.delay_pipeline.set_property("auto-flush-bus", True)
		#ALSA
		self.audiosrc = gst.element_factory_make("alsasrc", "audio")
		self.audiosrc.set_property("device","default")
		self.delay_pipeline.add(self.audiosrc)
		#Queue
		self.audioqueue = gst.element_factory_make("queue","queue1")
		self.audioqueue.set_property("max-size-time",0)
		self.audioqueue.set_property("max-size-buffers",0)
		self.audioqueue.set_property("max-size-bytes",0)
		self.audioqueue.set_property("min-threshold-time",DELAY)
		self.audioqueue.set_property("leaky","no")
		self.delay_pipeline.add(self.audioqueue)
		#Audio Output
		self.sink = gst.element_factory_make("autoaudiosink", "sink")
		self.delay_pipeline.add(self.sink)
		#Link the elements
		self.audiosrc.link(self.audioqueue)
		self.audioqueue.link(self.sink)
		#Begin Playing
		#self.delay_pipeline.set_state(gst.STATE_PLAYING)
		
	def changeDelay(self):
		self.label.set_text(str(float(DELAY/float(1000000000))))			
		self.delay_pipeline.set_state(gst.STATE_NULL)
		self.audioqueue.set_property("min-threshold-time",DELAY)		
		self.delay_pipeline.set_state(gst.STATE_PLAYING)

	# Stop
	def on_buttonSTOP_clicked(self, widget):
		self.button0.set_label("Start")
		self.button0.connect("clicked", self.on_buttonSTART_clicked)
		self.delay_pipeline.set_state(gst.STATE_NULL)
		
	# Start Delay
	def on_buttonSTART_clicked(self, widget):
		global DELAY
		self.changeDelay()			
		self.button0.set_label("Stop")
		self.button0.connect("clicked", self.on_buttonSTOP_clicked)
	
	# Incrementa Delay		
	def on_buttonINC_clicked(self, widget):
		global DELAY
		DELAY = DELAY + INCR
		#print "Inc DELAY", DELAY
		self.changeDelay()	
		self.button0.set_label("Stop")
		self.button0.connect("clicked", self.on_buttonSTOP_clicked)
			
	# Decrementa Delay		
	def on_buttonDEC_clicked(self, widget):
		global DELAY
		DELAY = DELAY - INCR
		if (DELAY < 0):
			DELAY = 0
		#print "Dec DELAY", DELAY
		self.changeDelay()
		self.button0.set_label("Stop")
		self.button0.connect("clicked", self.on_buttonSTOP_clicked)

	# Reset Delay
	def on_buttonRST_clicked(self, widget):
		global DELAY
		DELAY = 0
		#print "Reset ", DELAY
		self.changeDelay()
		self.button0.set_label("Stop")
		self.button0.connect("clicked", self.on_buttonSTOP_clicked)

	# Save current delay
	def on_buttonSAV_clicked(self,widget):
		global DELAY
		global REGDELAY
		REGDELAY = DELAY

	# Restore current delay
	def on_buttonRES_clicked(self,widget):
		global DELAY
		global REGDELAY
		DELAY = REGDELAY
		self.changeDelay()

window = WradWindow()
window.connect("destroy", lambda w: Gtk.main_quit())

buttonx = Gtk.Button(label="Exit");
buttonx.connect("clicked", Gtk.main_quit)
window.box.pack_end(buttonx,True,True,0)

window.show_all()

Gtk.main()
