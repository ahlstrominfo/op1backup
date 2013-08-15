# apt-get -y remove --purge xserver-common
# apt-get -y remove --purge x11-common
# apt-get -y remove --purge gnome-icon-theme
# apt-get -y remove --purge gnome-themes-standard
# apt-get -y remove --purge penguinspuzzle
# apt-get -y remove --purge desktop-base
# apt-get -y remove --purge desktop-file-utils
# apt-get -y remove --purge hicolor-icon-theme
# apt-get -y remove --purge raspberrypi-artwork
# apt-get -y remove --purge omxplayer
# apt-get -y autoremove
# apt-get -y update
rm -rf /home/pi/python_games
apt-get -y install python-smbus i2c-tools usbmount sox apache2 php5

cp conf/raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf

mkdir /op1
chmod a+w /op1
chmod a+x /op1
cp *.py /op1
cp radio.json /op1

mkdir /op1-backup
chmod a+w /op1-backup
chmod a+r /op1-backup

cp op1d.sh /etc/init.d/op1lcd
chmod a+x /etc/init.d/op1lcd
update-rc.d op1lcd defaults

cp conf/apache.conf /etc/apache2/sites-available/default
/etc/init.d/apache2 stop
/etc/init.d/apache2 start


cp conf/modules.conf /etc/modules

reboot
