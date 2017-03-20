#!/bin/sh

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

MICROIDE_DIR=$SCRIPTPATH/microide
DOWNLOAD_DIR=./downloads

ARM_GCC_TOOLCHAIN_URL=https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2
ARM_GCC_TOOLCHAIN_LICENSE_URL=https://launchpadlibrarian.net/251686212/license.txt
ARM_GCC_TOOLCHAIN_FILENAME=gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2
ARM_GCC_TOOLCHAIN_VERSION=5.3.0
ARM_GCC_TOOLCHAIN_SIZE=442470400
ARM_GCC_TOOLCHAIN_LOCATION=toolchains/gcc-arm-none-eabi/microhal

OPENOCD_URL=https://sourceforge.net/projects/openocd/files/openocd/0.10.0-rc1/openocd-0.10.0-rc1.tar.gz/download
OPENOCD_FILENAME=openocd-0.10.0-rc1.tar.gz
OPENOCD_VERSION=0.10.0
OPENOCD_SIZE=2333886
OPENOCD_LOCATION=tools/openocd/0.10.0


download() {
wget --directory-prefix=$DOWNLOAD_DIR https://github.com/microHAL/microIDE/archive/master.zip
echo 'Downloading ARM toolchain ...'
wget --directory-prefix=$DOWNLOAD_DIR $ARM_GCC_TOOLCHAIN_URL
echo 'Downloading openOCD...'
wget -O $DOWNLOAD_DIR/$OPENOCD_FILENAME $OPENOCD_URL
echo 'Downloading Eclipse...'
wget --directory-prefix=$DOWNLOAD_DIR http://mirrors.nic.cz/eclipse/oomph/products/eclipse-inst-linux64.tar.gz
}


mkdir -p microide
cd microide
#------------------------------------- toolchains -----------------------------
echo 'Downloading files'
download
echo 'Unpacking toolchain patch and eclipse installer setup configuration.'
unzip $DOWNLOAD_DIR/master.zip 
echo 'Installing ARM Toolchain...'
sudo apt-get update
sudo apt-get install lib32z1 lib32ncurses5 lib32bz2-1.0 lib32stdc++6
mkdir -p $ARM_GCC_TOOLCHAIN_LOCATION
tar --extract --bzip2 --file=$DOWNLOAD_DIR/$ARM_GCC_TOOLCHAIN_FILENAME -C $ARM_GCC_TOOLCHAIN_LOCATION
#installing microhal patch to toolchain, this will allow to use standart operating system library with FreeRTOS
echo 'Patching ARM Toolchain.'
cp -r microIDE-master/toolchains/gcc-arm-none-eabi-patch/$ARM_GCC_TOOLCHAIN_VERSION/* $ARM_GCC_TOOLCHAIN_LOCATION/gcc-arm-none-eabi-5_3-2016q1

# ------------------------------------ tools ---------------------------------
echo 'Installing tools'
echo 'Installing openOCD'
sudo apt-get install libusb-1.0-0-dev libtool pkg-config
mkdir -p tools/openocd
echo 'Extracting OpenOCD...'
mkdir -p tmp
tar --extract --file=$DOWNLOAD_DIR/$OPENOCD_FILENAME -C tmp
echo 'Compilling OpenOCD'
cd tmp/openocd-0.10.0-rc1
./configure --enable-stlink --enable-jlink --prefix=$MICROIDE_DIR/tools/openocd/0.10.0
make
make install
sudo cp contrib/60-openocd.rules /etc/udev/rules.d/
sudo usermod -aG plugdev $USER
cd ../../
# ---------------------------------- eclipse ---------------------------------
echo 'Installing Eclipse'
mkdir -p eclipse-installer
tar --extract --file=$DOWNLOAD_DIR/eclipse-inst-linux64.tar.gz 
#redirect eclipse installer product index
cd eclipse-installer
echo '-Doomph.redirection.setups=http://git.eclipse.org/c/oomph/org.eclipse.oomph.git/plain/setups/->setups/' >> eclipse-inst.ini
cd ../
mkdir -p eclipse-installer/setups
cp -r microIDE-master/eclipse-installer/setups/* eclipse-installer/setups
rm -r microIDE-master
rm -r tmp
rm -r $DOWNLOAD_DIR/master.zip 

echo '-----------------------------------------------------------------------------'
echo 'Please install eclipse in following directory:'
echo $MICROIDE_DIR

#starting eclipse installer
./eclipse-installer/eclipse-inst




  
 
