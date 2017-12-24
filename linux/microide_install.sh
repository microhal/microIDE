#!/bin/sh

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

#links to installation files

VERSION=0.3.2
ARM_GCC_TOOLCHAIN_URL=https://developer.arm.com/-/media/Files/downloads/gnu-rm/6-2017q2/gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2?revision=2cc92fb5-3e0e-402d-9197-bdfc8224d8a5?product=GNU%20Arm%20Embedded%20Toolchain,64-bit,,Linux,6-2017-q2-update
ARM_GCC_TOOLCHAIN_LICENSE_URL=https://developer.arm.com/GetEula?Id=2d916619-954e-4adb-895d-b1ec657ae305
ARM_GCC_TOOLCHAIN_FILENAME=gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2
ARM_GCC_TOOLCHAIN_VERSION=6.2.0
ARM_GCC_TOOLCHAIN_SIZE=100554551
ARM_GCC_TOOLCHAIN_CHECKSUM=13747255194398ee08b3ba42e40e9465
ARM_GCC_TOOLCHAIN_LOCATION=toolchains/gcc-arm-none-eabi/microhal

OPENOCD_URL=https://sourceforge.net/projects/openocd/files/openocd/0.10.0/openocd-0.10.0.tar.gz/download
OPENOCD_FILENAME=openocd-0.10.0.tar.gz
OPENOCD_VERSION=0.10.0
OPENOCD_SIZE=6124274
OPENOCD_CHECKSUM=8971d16aee5c2642b33ee55fc6c86239
OPENOCD_LOCATION=tools/openocd/0.10.0

ECLIPSE_URL=http://www.eclipse.org/downloads/download.php?file=/oomph/products/latest/eclipse-inst-linux64.tar.gz\&r=1
ECLIPSE_FILENAME=eclipse-inst-linux64.tar.gz
ECLIPSE_VERSION=oxygen
ECLIPSE_SIZE=48060711
ECLIPSE_CHECKSUM=52bce05a9d774e1ee8723833dbb74354
ECLIPSE_LOCATION=eclipse
MICROIDE_DIR=$SCRIPTPATH/microide-$VERSION
DOWNLOAD_DIR=./downloads
BRANCH_NAME=devel

download() {
wget --directory-prefix=$DOWNLOAD_DIR https://github.com/microHAL/microIDE/archive/$BRANCH_NAME.zip
echo 'Downloading ARM toolchain ...'
wget -O $DOWNLOAD_DIR/$ARM_GCC_TOOLCHAIN_FILENAME $ARM_GCC_TOOLCHAIN_URL
md5_local=$(md5sum "$DOWNLOAD_DIR/$ARM_GCC_TOOLCHAIN_FILENAME" | awk '{print $1}')
if [ "$md5_local" != "$ARM_GCC_TOOLCHAIN_CHECKSUM" ]
then
    echo $ARM_GCC_TOOLCHAIN_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $ARM_GCC_TOOLCHAIN_CHECKSUM
    echo Aborting...
    exit 1
fi
echo 'Downloading openOCD...'
wget -O $DOWNLOAD_DIR/$OPENOCD_FILENAME $OPENOCD_URL
md5_local=$(md5sum "$DOWNLOAD_DIR/$OPENOCD_FILENAME" | awk '{print $1}')
if [ "$md5_local" != "$OPENOCD_CHECKSUM" ]
then
    echo $OPENOCD_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $OPENOCD_CHECKSUM
    echo Aborting...
    exit 1
fi
echo 'Downloading Eclipse...'
wget -O $DOWNLOAD_DIR/$ECLIPSE_FILENAME $ECLIPSE_URL
#md5_local=$(md5sum "$DOWNLOAD_DIR/$ECLIPSE_FILENAME" | awk '{print $1}')
#if [ "$md5_local" != "$ECLIPSE_CHECKSUM" ]
#then
#    echo $ECLIPSE_FILENAME checksum missmatch.
#    echo Calculated $md5_local
#    echo Expected $ECLIPSE_CHECKSUM
#    echo Aborting...
#    exit 1
#fi
}


instal() {
#------------------------------------- toolchains -----------------------------
echo 'Unpacking toolchain patch and eclipse installer setup configuration.'
echo 'Unpacking toolchain patch and eclipse installer setup configuration.---------------' >> log.log
if ! unzip $DOWNLOAD_DIR/$BRANCH_NAME.zip >> log.log; then
    echo 'Unable to unzip repozitory files'
    echo 'Aborting...'
    exit 1
fi 
echo 'Installing ARM Toolchain...'
echo 'Installing ARM Toolchain...-------------------------------------------------------' >> log.log
sudo apt-get update
sudo apt-get install lib32z1 lib32ncurses5 libbz2-1.0:i386 lib32stdc++6
mkdir -p $ARM_GCC_TOOLCHAIN_LOCATION
tar --extract --bzip2 --file=$DOWNLOAD_DIR/$ARM_GCC_TOOLCHAIN_FILENAME -C $ARM_GCC_TOOLCHAIN_LOCATION
mv $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-linux.tar.bz2} $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-*-linux.tar.bz2}
#installing microhal patch to toolchain, this will allow to use standart operating system library with FreeRTOS
echo 'Patching ARM Toolchain.'
echo 'Patching ARM Toolchain.-----------------------------------------------------------' >> log.log
cp -r microIDE-$BRANCH_NAME/toolchains/gcc-arm-none-eabi-patch/${ARM_GCC_TOOLCHAIN_FILENAME%-*-linux.tar.bz2}/* $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-*-linux.tar.bz2}

# ------------------------------------ tools ---------------------------------
echo 'Installing tools'
echo 'Installing openOCD'
sudo apt-get install libusb-1.0-0-dev libtool pkg-config
mkdir -p tools/openocd
echo 'Extracting OpenOCD...'
mkdir -p tmp
tar --extract --file=$DOWNLOAD_DIR/$OPENOCD_FILENAME -C tmp
echo 'Compilling OpenOCD'
echo 'Compilling OpenOCD ---------------------------------------------------------------' >> log.log
cd tmp/${OPENOCD_FILENAME%.tar.gz}
./configure --enable-stlink --enable-jlink --enable-oocd_trace --enable-buspirate --prefix=$MICROIDE_DIR/$OPENOCD_LOCATION >> log.log
make  >> log.log
make install
sudo cp contrib/60-openocd.rules /etc/udev/rules.d/
sudo usermod -aG plugdev $USER
cd ../../
# ---------------------------------- eclipse ---------------------------------
echo 'Installing Eclipse'
echo 'Installing Eclipse ---------------------------------------------------------------' >> log.log
mkdir -p eclipse-installer
sudo apt-get install default-jre
tar --extract --file=$DOWNLOAD_DIR/$ECLIPSE_FILENAME
#redirect eclipse installer product index
cd eclipse-installer
echo '-Doomph.redirection.setups=http://git.eclipse.org/c/oomph/org.eclipse.oomph.git/plain/setups/->setups/' >> eclipse-inst.ini
cd ../
mkdir -p eclipse-installer/setups/
cp -r microIDE-$BRANCH_NAME/eclipse-installer/setups/* eclipse-installer/setups
mv eclipse-installer/setups/microIDE/microide.product.setup.linux eclipse-installer/setups/microIDE/microide.product.setup
rm eclipse-installer/setups/microIDE/microide.product.setup.windows
rm -r microIDE-$BRANCH_NAME
rm -r tmp
rm -r $DOWNLOAD_DIR/$BRANCH_NAME.zip
#install clang-format
sudo apt-get install clang-format


echo '-----------------------------------------------------------------------------'
echo 'Please install eclipse in following directory:'
echo $MICROIDE_DIR

#starting eclipse installer
./eclipse-installer/eclipse-inst
}




# script starting point
mkdir -p microide-$VERSION
cd microide-$VERSION

if [ "$1" = "--checkDownload" ]; then
	echo "Selected download checking mode."
	download
else
	echo "Starting normal install."
	download
	instal
fi




  
 
