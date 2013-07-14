#!/usr/bin/python

import platform, os, os.path, shutil, syslog, sys

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from LCDMenu import LCDMenu
from subprocess import *
from time import sleep, strftime
from datetime import datetime

root = '/op1-backup/'
op1 = '/media/usb0'

lcd = Adafruit_CharLCDPlate()
btn = (lcd.LEFT, lcd.UP, lcd.DOWN, lcd.RIGHT, lcd.SELECT)
prev = -1
buttonsactive = True
is_op1_available = None
backup_position = ""

def logger(msg):
	syslog.syslog(msg)
	print(msg)

def run_cmd(cmd):
		p = Popen(cmd, shell=True, stdout=PIPE)
		output = p.communicate()[0]
		return output

def menulcd():
	clearprint(LCDMenu.getPosition())

def clearprint(message):
	global lcd
	lcd.clear()
	lcd.message(message)

	
def getip(eth = True):
	if (eth):
		cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
		eth_ipaddr = run_cmd(cmd)
		return eth_ipaddr

	cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
	wlan_ipaddr = run_cmd(cmd)
	return wlan_ipaddr

def showip():
	global buttonsactive
	str = "eth:" + getip() + "\nwifi:" + getip(False)
	clearprint(str)
	sleep(3)
	resetmenu();

def op1_is_avaliable():
	return os.path.exists('/media/usb0/album/')

def get_next_backup():
	global root
	current = 0
	for item in os.listdir(root):
		if os.path.isdir(os.path.join(root, item)):
			try:
				val = int(item)
				if current < val:
					current = val

			except ValueError:
				continue

	return root + str(current + 1)	

def copy_tracks():
	global backup_position
	clearprint("Copying tracks\nto raspberry")
	shutil.copytree('/media/usb0/tape/', backup_position + '/tape');
	lcd.backlight(lcd.GREEN)
	clearprint("Copy complete!")
	sleep(5)
	resetmenu();	

def copy_single(side):
	global backup_position

	if (os.path.isdir(backup_position) == False):
		logger("Create: %s" % backup_position)
		os.mkdir(backup_position)

	if (os.path.isdir(backup_position + "/album") == False):
		logger("Create album: %s/album" % backup_position)
		os.mkdir(backup_position + "/album")

	logger('Copy file /media/usb0/album/side_%s.aif ' % side)	
	shutil.copyfile('/media/usb0/album/side_'+side+'.aif', backup_position + '/album/side_'+side+'.aif')


def copy_album_a():
	logger("Begin copy album A")
	clearprint("Copying album A\nto raspberry")
	copy_single("a")
	lcd.backlight(lcd.GREEN)
	logger("End copy album A")
	clearprint("Copy complete!")
	sleep(5)
	resetmenu();	

def copy_album_b():
	logger("Begin copy album B")
	clearprint("Copying album B\nto raspberry")
	copy_single("b")
	lcd.backlight(lcd.GREEN)
	logger("End copy album B")
	clearprint("Copy complete!")
	sleep(5)
	resetmenu();

def copy_album():
	logger("Start copy albums")
	clearprint("Copying album A\nto raspberry")
	copy_single("a")	
	clearprint("Copying album B\nto raspberry")
	copy_single("b")
	lcd.backlight(lcd.GREEN)
	clearprint("Copy complete!\n")
	logger("End copy albums")
	sleep(5)
	resetmenu();	

def upload_track():
	parent = LCDMenu.lcdMenu.currentItem();
	
	clearprint("Upload tracks\nto OP1")
	shutil.copyfile(parent.args[0] + "/track_1.aif", '/media/usb0/tape/track_1.aif')
	clearprint("Upload tracks\nto OP1 1/4")
	shutil.copyfile(parent.args[0] + "/track_2.aif", '/media/usb0/tape/track_2.aif')
	clearprint("Upload tracks\nto OP1 2/4")
	shutil.copyfile(parent.args[0] + "/track_3.aif", '/media/usb0/tape/track_3.aif')
	clearprint("Upload tracks\nto OP1 3/4")
	shutil.copyfile(parent.args[0] + "/track_4.aif", '/media/usb0/tape/track_4.aif')
	clearprint("Upload tracks\nto OP1 4/4")

	lcd.backlight(lcd.GREEN)
	clearprint("Copy complete!")
	sleep(5)
	resetmenu();	

def upload_tracks():
	parent = LCDMenu.lcdMenu.currentItem();
	parent.children = []
	tape_dirs = []
	for dirs in sorted(os.listdir(root)):
		backup_path = os.path.join(root, dirs)
		if (os.path.exists(backup_path+'/tape')):
			parent.addItem(LCDMenu(dirs, parent, upload_track, [backup_path+'/tape']))

	parent.position = len(parent.children) - 1
	LCDMenu.lcdMenu = parent;
	menulcd()

def backupDrumPresets():
	global op1
	for root, dirs, files in os.walk(op1+'/drum/'):
		#files = [os.path.join(root, f) for f in files]
		print "root"
		print(root)
		#print "dirs"
		#print(dirs)
		#print "\n"
		print(files)
		#for fname in files:
			#print fname

def setLCDMenu(newLCDMenu):
	if LCDMenu.lcdMenu is not newLCDMenu:
		LCDMenu.lcdMenu = newLCDMenu
		menulcd()

def loadChildMenu():
	LCDMenu.lcdMenu = LCDMenu.lcdMenu.currentItem();
	menulcd()	

def freezemenu():
	global buttonsactive
	buttonsactive = False
	lcd.backlight(lcd.RED)

def resetmenu(runmenu = True):
	global buttonsactive
	buttonsactive = True
	lcd.backlight(lcd.TEAL)
	if (runmenu):
		menulcd()

def init():
	global is_op1_available
	lcd.backlight(lcd.TEAL)
	clearprint("OP1 Backup 2000!!!\nVersion Three")
	sleep(2)
	if op1_is_avaliable():
		is_op1_available = True
		setLCDMenu(lcdOnlineMenu)
	else: 
		is_op1_available = False
		setLCDMenu(lcdOfflineMenu)


lcdOnlineMenu = LCDMenu('OP1 Backup 2000!!!')

lcdAlbum = LCDMenu("album", lcdOnlineMenu, loadChildMenu)
lcdAlbum.addItem(LCDMenu("backup album a", lcdAlbum, copy_album_a))
lcdAlbum.addItem(LCDMenu("backup album b", lcdAlbum, copy_album_b))
lcdAlbum.addItem(LCDMenu("backup albums", lcdAlbum, copy_album))
lcdOnlineMenu.addItem(lcdAlbum)

lcdTracks = LCDMenu("tracks", lcdOnlineMenu, loadChildMenu)
lcdTracks.addItem(LCDMenu("backup tracks", lcdTracks, copy_tracks))
lcdTracks.addItem(LCDMenu("upload tracks", lcdTracks, upload_tracks))
lcdOnlineMenu.addItem(lcdTracks)

lcdPresets = LCDMenu("drum presets", lcdOnlineMenu, loadChildMenu)
lcdPresets.addItem(LCDMenu("backup all", lcdPresets, backupDrumPresets))
lcdPresets.addItem(LCDMenu("delete on OP1", lcdPresets))
lcdPresets.addItem(LCDMenu("upload", lcdPresets))
#lcdOnlineMenu.addItem(lcdPresets)

lcdOnlineMenu.addItem(LCDMenu("show ip", lcdOnlineMenu, showip))

lcdOfflineMenu = LCDMenu('W00t! no OP1?')
lcdOfflineMenu.addItem(LCDMenu("show ip", lcdOfflineMenu, showip))

init()

while True:
	if op1_is_avaliable() == False and is_op1_available == True:
		is_op1_available = False
		setLCDMenu(lcdOfflineMenu)
	
	if op1_is_avaliable() and is_op1_available == False:
		is_op1_available = True
		backup_position = get_next_backup()
		setLCDMenu(lcdOnlineMenu)

	if (buttonsactive == False): # if active then menusystem is freezed
		continue

	if (lcd.buttons() == 0): # if no button is pressed reset state
		prev = -1

	for b in btn:
		if lcd.buttonPressed(b):
			if (prev == b):
				break

			if b == lcd.UP:
				LCDMenu.up()
				menulcd()

			if b == lcd.DOWN:
				LCDMenu.runFunc()			

			if b == lcd.RIGHT:
				LCDMenu.next()
				menulcd()

			if b == lcd.LEFT:
				LCDMenu.prev()
				menulcd()

			if b == lcd.SELECT:
				LCDMenu.runFunc()

			prev = b
