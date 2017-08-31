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

mkdir -p microide
cd microide

wget --directory-prefix=$DOWNLOAD_DIR https://github.com/microHAL/microIDE/archive/master.zip
echo 'Downloading ARM toolchain ...'
wget --directory-prefix=$DOWNLOAD_DIR $ARM_GCC_TOOLCHAIN_URL
echo 'Downloading openOCD...'
wget -O $DOWNLOAD_DIR/$OPENOCD_FILENAME $OPENOCD_URL
echo 'Downloading Eclipse...'
wget --directory-prefix=$DOWNLOAD_DIR http://mirrors.nic.cz/eclipse/oomph/products/eclipse-inst-linux64.tar.gz


