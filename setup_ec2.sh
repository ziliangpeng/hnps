#!/bin/sh


cd ~
sudo apt-get update
sudo apt-get -y install git
sudo apt-get -y install subversion


sudo apt-get -y install build-essential python-dev

svn checkout http://py-leveldb.googlecode.com/svn/trunk/ py-leveldb-read-only
cd py-leveldb-read-only


sudo apt-get -y install autotools-dev
sudo apt-get -y install automake
sudo apt-get -y install libtool
sudo apt-get -y install pkg-config


./compile_leveldb.sh
sudo python setup.py build
sudo python setup.py install
