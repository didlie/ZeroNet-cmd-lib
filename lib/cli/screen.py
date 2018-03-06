import sys, platform
import size

from colorama import Fore, Back, Style

import colorama

class Screen(object):
	class Resized(Exception):
		pass

	def __init__(self):
		if platform.system().lower() == "windows":
			# On Linux and Darwin, ANSI escapes just work.

			build = int(platform.win32_ver()[1].split(".")[-1])
			if build < 10525:
				# Before build 10525, ANSI escapes were not handled by Windows
				self.color_support = "simulation"

				# Colorama will simulate some ANSI escapes with WinAPI calls
				colorama.init()
			elif build < 16257:
				# Before build 16257, ANSI escapes were enabled by default
				self.color_support = "full"
			elif build >= 16257:
				# As of build 16257, we need to enable ANSI escapes manually

				from ctypes import windll, c_int, byref
				stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
				mode = c_int(0)
				windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
				mode = c_int(mode.value | 4)
				windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)

		self.terminal_size = self.getTerminalSize()

	def loop(self, handler):
		while True:
			cur = self.getTerminalSize()
			if self.terminal_size != cur:
				raise Screen.Resized
			self.terminal_size = cur

			handler(self)

	def getTerminalSize(self):
		return size.get_terminal_size()

	def write(self, data):
		sys.stdout.write(data)


	def clear(self):
		self.write("\033[2J\033[1;1f")

	def moveCursor(self, x, y):
		self.write("\x1b[%d;%dH" % (y + 1, x + 1))

	def printAt(self, text, x, y):
		self.moveCursor(int(x), int(y))
		self.write(text)

	def colorize(self, text, fg=None, bg=None, bright=False):
		if fg is not None:
			text = getattr(Fore, fg.upper()) + text
		if bg is not None:
			text = getattr(Back, bg.upper()) + text
		if bright:
			text = Style.BRIGHT + text

		text += Style.RESET_ALL
		return text

	def fill(self, x1, y1, x2, y2, char=" ", style=lambda s: s):
		s = char * (int(x2) - int(x1))
		for y in range(int(y1), int(y2)):
			self.printAt(style(s), x=int(x1), y=y)