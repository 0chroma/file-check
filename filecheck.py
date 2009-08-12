#!/usr/bin/env python

# Copyright (c) 2008, Will Riley
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pygtk
pygtk.require('2.0')
import gtk, hashlib, random, os

class Gui:
    def writeFile(self, widget, data=None):
	dialog = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_CANCEL)
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		fp = open(dialog.get_filename(),"w")
		self.filePath = dialog.get_filename()
		self.checksum = self.writeGarbage(fp)
		fp.close()
		self.checkButton.set_sensitive(True)
		self.statusbar.push(data, "Wrote to file \"%s\"" % self.filePath)
	dialog.destroy()
	
    def writeGarbage(self, fp):
	m = hashlib.md5()
	for i in range(1, 200):
	    char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
	    fp.write(char)
	    m.update(char)
	return m.digest()
    
    def checkFile(self, widget, data=None):
	if not os.path.isfile(self.filePath):
		return self.statusbar.push(data, "File could not be found")
	try:
		fp = open(self.filePath, "rb")
		m = hashlib.md5()
		m.update(fp.read())
		if m.digest() == self.checksum:
			self.statusbar.push(data, "File has not changed")
		else:
			self.statusbar.push(data, "File has changed")
		fp.close()
	except IOError:
		self.statusbar.push(data, "File could not be opened")

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.window.resizable = False
        self.window.set_title("File Integrity Checker")
	self.window.resize(300, 100)

	self.statusbar = gtk.Statusbar()
	context_id = self.statusbar.get_context_id("Statusbar")	
	
        self.window.connect("delete_event", self.delete_event)
        table = gtk.Table(2, 2, True)
        self.window.add(table)

        button = gtk.Button("Write File")
        button.connect("clicked", self.writeFile, context_id)
        table.attach(button, 0, 1, 0, 1)
        button.show()

        button = gtk.Button("Check File")
        button.connect("clicked", self.checkFile, context_id)
        table.attach(button, 1, 2, 0, 1)
	button.set_sensitive(False)
        button.show()
	self.checkButton = button

        table.attach(self.statusbar, 0, 2, 1, 2)
        self.statusbar.show()

        table.show()
        self.window.show()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    Gui()
    main()
