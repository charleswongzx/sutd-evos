#!/bin/bash
# Script for installing EVOS environment

sudo apt -y install python-dev
sudo apt -y install python-kivy

cd
sudo apt -y install openjdk-6-jdk
sudo apt -y install build-essential
sudo apt -y install libglib2.0-dev


wget hhttps://github.com/lcm-proj/lcm/releases/download/v1.3.1/lcm-1.3.1.zip
tar -xzvf lcm-1.3.1.zip
cd lcm-1.3.1
./configure
make
sudo make install
sudo ldconfig

export LCM_INSTALL_DIR=/usr/local/lib
sudo bash -c 'echo '/usr/local/lib' > /etc/ld.so.conf.d/lcm.conf'
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
sudo bash -c 'echo "/usr/local/lib/python2.7/site-packages" > /usr/local/lib/python2.7/lcm.pth'

