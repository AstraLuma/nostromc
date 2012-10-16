# -*- tab-width: 4; use-tabs: 1; coding: utf-8 -*-
# vim:tabstop=4:noexpandtab:
"""
Restart ourselves if we we detect a file change.
"""
from __future__ import division, absolute_import, with_statement
import sys, os
import pyinotify
__all__ = 'config',

class config(pyinotify.ProcessEvent):
	MASK = pyinotify.IN_CLOSE_WRITE
	def __init__(self, **ops):
		global _INRESTART
		self.ops = ops
		self.wm = pyinotify.WatchManager()
		self.notifier = pyinotify.ThreadedNotifier(self.wm, self)
		self.notifier.setDaemon(True)
		self.notifier.start()
		for path in ops['watches']:
			if not os.path.exists(path): continue
			self.wm.add_watch(path, self.MASK, rec=True)
	
	def filter(self, fn):
		if 'filter' in self.ops:
			return self.ops['filter'](fn)
		else:
			return True
	
	def restart(self):
		print "Reloading..."
		os.closerange(3,20)
		os.execv(sys.argv[0], sys.argv)
	
	def process_IN_CLOSE_WRITE(self, event):
		if self.filter(event.name):
			self.restart()

