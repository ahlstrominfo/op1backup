#!/usr/bin/python

import platform, os, shutil, syslog, sys

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import *
from time import sleep, strftime
from datetime import datetime

root = '/op1-backup/'

BACKUP_ALBUM_A = "backup album a"
BACKUP_ALBUM_B = "backup album b"
BACKUP_ALBUMS = "backup albums"
BACKUP_TRACKS = "backup tracks"
SHOW_IP = "   show ip    "
RECOVER_TRACKS = "recover tracks"

menu = [	
	# "B albums",
	# "B everything",
	BACKUP_ALBUM_A,
	BACKUP_ALBUM_B,
	BACKUP_ALBUMS,
	BACKUP_TRACKS,
#	RECOVER_TRACKS,
	# "B All Synths",
	# "B All Synths",
	SHOW_IP
];



menupos = 0;
lcd = Adafruit_CharLCDPlate()
btn = (lcd.LEFT, lcd.UP, lcd.DOWN, lcd.RIGHT, lcd.SELECT)
prev = -1
buttonsactive = True
is_op1_available = False
backup_position = ""


def run_cmd(cmd):
		p = Popen(cmd, shell=True, stdout=PIPE)
		output = p.communicate()[0]
		return output

def menulcd():
	global menupos

	lenmenu = len(menu) - 1
	if (menupos > lenmenu):
		menupos = 0;
	if (menupos < 0):
		menupos = lenmenu

	clearprint('OP1 Backup 2000\n<%s>' % ( menu[menupos] ))

def clearprint(message):
	global lcd
	lcd.clear()
	lcd.message(message)

def run_select():
	global menupos, menu

	current_menu = menu[menupos]

	if (current_menu == SHOW_IP):
		freezemenu()
		showip()

	if (current_menu == BACKUP_ALBUM_A):
		freezemenu()
		copy_album_a()

	if (current_menu == BACKUP_ALBUM_B):
		freezemenu()
		copy_album_b()

	if (current_menu == BACKUP_ALBUMS):
		freezemenu();
		copy_album()
	
	if (current_menu == BACKUP_TRACKS):
		freezemenu();
		copy_tracks()

	if (current_menu == RECOVER_TRACKS):
		recover_tracks()

	
def getip():
	cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
	ipaddr = run_cmd(cmd)
	return ipaddr	

def showip():
	global buttonsactive

	clearprint('IP %s' % ( getip() ) )
	sleep(3)
	resetmenu(False);

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
		os.mkdir(backup_position)

	if (os.path.isdir(backup_position + "/album") == False):
		os.mkdir(backup_position + "/album")

	shutil.copyfile('/media/usb0/album/side_'+side+'.aif', backup_position + '/album/side_'+side+'.aif')


def copy_album_a():
	clearprint("Copying album A\nto raspberry")
	copy_single("a")
	lcd.backlight(lcd.GREEN)
	clearprint("Copy complete!")
	sleep(5)
	resetmenu();	

def copy_album_b():
	clearprint("Copying album B\nto raspberry")
	copy_single("b")
	lcd.backlight(lcd.GREEN)
	clearprint("Copy complete!")
	sleep(5)
	resetmenu();

def copy_album():
	clearprint("Copying album A\nto raspberry")
	copy_single("a")	
	clearprint("Copying album B\nto raspberry")
	copy_single("b")
	lcd.backlight(lcd.GREEN)
	clearprint("Copy complete!\n")
	sleep(5)
	resetmenu();	

def recover_tracks():
	tape_dirs = []
	for dirs in os.listdir(root):
		backup_path = os.path.join(root, dirs)
		if (os.path.exists(backup_path+'/tape')):
			tape_dirs.append(dirs);
	
	print(tape_dirs)


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
	lcd.backlight(lcd.TEAL)
	clearprint("OP1 Backup 2000!!!")
	sleep(2)
	menulcd()

init()

while True:

	if op1_is_avaliable() == False:
		clearprint("Waiting for OP1\n" + getip())
		is_op1_available = False
		sleep(2)
		continue
	
	if (op1_is_avaliable() and is_op1_available == False):
		is_op1_available = True
		backup_position = get_next_backup()
		print backup_position
		menulcd()

	if (buttonsactive == False): # if active then menusystem is freezed
		continue

	if (lcd.buttons() == 0): # if no button is pressed reset state
		prev = -1

	for b in btn:
		if lcd.buttonPressed(b):
			if (prev == b):
				break

			if b == lcd.RIGHT:
				menupos += 1
				menulcd()

			if b == lcd.LEFT:
				menupos -= 1
				menulcd()

			if b == lcd.SELECT:
				run_select()

			prev = b
