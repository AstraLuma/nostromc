# -*- tab-width: 4; use-tabs: 1; coding: utf-8 -*-
# vim:tabstop=4:noexpandtab:
"""
Some stuff to handle Minecraft config files
"""
from __future__ import division, absolute_import, with_statement
import os, os.path, glob
from pyinput import uinput
import lwjgl_keys
__all__ = 'McConfig', 'find_latest', 'find_configs', 'inr_config'

def find_configs():
	"""find_configs() -> string, ...
	Scans a bunch of the usual locations for minecraft config files, yielding 
	all found config files.
	"""
	_ = os.path.expanduser
	if os.path.exists(_("~/.minecraft/options.txt")):
		yield _("~/.minecraft/options.txt")
	for fn in glob.glob(_("~/.techniclauncher/*/options.txt")):
		yield fn
	for fn in glob.glob(_("~/.spoutcraft/*/options.txt")):
		yield fn

def find_latest():
	"""find_latest() -> string
	Scans a bunch of the usual locations for minecraft config files, returning 
	the newest one.
	"""
	age = 0
	newfn = None
	for fn in find_configs():
		a = os.stat(fn).st_mtime
		if a > age:
			age = a
			newfn = fn
	return newfn

class McConfig(object):
	def __init__(self, fn):
		self.load(fn, wipe=True)
	
	def load(self, fn, wipe=False):
		if wipe:
			self.ops = {}
		for l in open(fn):
			l = l.rstrip()
			if not l: continue
			k, v = l.split(':', 1)
			self.ops[k] = v
	
	def ui(self, *settings):
		"""
		Gets the uinput key given the setting.
		"""
		for setting in settings:
			try:
				s = self.ops[setting]
			except KeyError:
				continue
			s = int(s)
			if s <= 0: return None
			kn = lwjgl_keys.Keys.getname(s)
			return getattr(uinput, kn)
		else:
			return 0

def inr_filter(fn):
	return os.path.basename(fn) == "options.txt"

def inr_config():
	"""inr_config() -> dict
	Tells inrestart what to monitor.
	"""
	_ = os.path.expanduser
	return {
		'filter': inr_filter,
		'watches': [
			_("~/.minecraft/options.txt"),
			_("~/.techniclauncher"),
			_("~/.spoutcraft"),
			],
		}
