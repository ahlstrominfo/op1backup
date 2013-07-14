#!/usr/bin/python

class LCDMenu:
	lcdMenu = None

 	@staticmethod
	def getPosition():
		return LCDMenu.lcdMenu.header.center(16,' ') + "\n<" + LCDMenu.lcdMenu.currentItem().header.center(14,' ')+">"

	@staticmethod
	def next():
		lcd = LCDMenu.lcdMenu
		lcd.position = (lcd.position+1) % len(lcd.children)		
	
	@staticmethod
	def prev():
		lcd = LCDMenu.lcdMenu
		lcd.position = (lcd.position-1) % len(lcd.children)		

	@staticmethod
	def runFunc():
		lcd = LCDMenu.lcdMenu
		lcd.run()

	@staticmethod
	def up():
		lcd = LCDMenu.lcdMenu
		if (lcd.parent is not None):
			LCDMenu.lcdMenu = lcd.parent


	def __init__(self, header, parent = None, func = None, args = []):
		self.position = 0
		self.header = header
		self.parent = parent
		self.children = []
		self.func = func
		self.args = args

	def addItem(self, aLCDMenu):
		self.children.append(aLCDMenu)

	def currentItem(self):
		return self.children[self.position]

	def run(self):
		func = self.children[self.position].func
		if (func is not None):
			func()

	def printTree(self):
		if (self.parent is not None):
			print self.parent.header
			print self.header
			print "-"
		for childMenu in self.children:
			childMenu.printTree()

# def doshit():
# 	print("done")

# print doshit

#def main():

	# lcdMenu = LCDMenu("THIS IS OPBACKUP!");
	# lcdMenu.addItem(LCDMenu("Copy Album A", lcdMenu, doshit))
	# lcdMenu.addItem(LCDMenu("Copy Album B", lcdMenu))
	# lcdMenu.addItem(LCDMenu("Copy Albums", lcdMenu))
	# lcdMenu.addItem(LCDMenu("Copy Tracks", lcdMenu))
	# lcdMenu.addItem(LCDMenu("Show IP", lcdMenu))

	# #lcdMenu.printit()

	# lcdMenu.printPosition()
	# lcdMenu.run()
	# print "-----"
	# lcdMenu.next()
	# lcdMenu.next()
	# lcdMenu.next()
	# lcdMenu.next()
	# lcdMenu.next()
	# #lcdMenu.printPosition()

	# lcdMenu.prev()
	# lcdMenu.prev()
	# lcdMenu.prev()
	#lcdMenu.printPosition()


#if  __name__ =='__main__':
 #   main()		