#!/bin/sh

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

MICROIDE_DIR=$SCRIPTPATH/microide
DOWNLOAD_DIR=./downloads

ARM_GCC_TOOLCHAIN_URL=https://developer.arm.com/-/media/Files/downloads/gnu-rm/6-2017q2/gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2?product=GNU%20ARM%20Embedded%20Toolchain,64-bit,,Linux,6-2017-q2-update
ARM_GCC_TOOLCHAIN_MD5=13747255194398ee08b3ba42e40e9465
ARM_GCC_TOOLCHAIN_LICENSE_URL=https://developer.arm.com/GetEula?Id=2d916619-954e-4adb-895d-b1ec657ae305
ARM_GCC_TOOLCHAIN_FILENAME=gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2
ARM_GCC_TOOLCHAIN_VERSION=6-2017-q2
ARM_GCC_TOOLCHAIN_LOCATION=toolchains/gcc-arm-none-eabi/microhal

OPENOCD_URL=https://sourceforge.net/projects/openocd/files/openocd/0.10.0/openocd-0.10.0.tar.gz/download
OPENOCD_MD5=8971d16aee5c2642b33ee55fc6c86239
OPENOCD_FILENAME=openocd-0.10.0.tar.gz
OPENOCD_VERSION=0.10.0
OPENOCD_LOCATION=tools/openocd/0.10.0

ECLIPSE_URL=https://www.eclipse.org/downloads/download.php?file=/oomph/epp/oxygen/R/eclipse-inst-linux64.tar.gz\&r=1
ECLIPSE_SHA512=2bbb38475b3f3b13b9c6c5db5895fe25ce24b4a8df6a24c6822a348a9652dc8df49ca19152495f34156c39022b8c2ed6b5bb1e84db3edc751302d73bdc1d56da
ECLIPSE_FILENAME=eclipse-inst-linux64.tar.gz
ECLIPSE_LOCATION=eclipse

WIN_ARM_GCC_TOOLCHAIN_URL=https://developer.arm.com/-/media/Files/downloads/gnu-rm/6-2017q2/gcc-arm-none-eabi-6-2017-q2-update-win32.zip?product=GNU%20ARM%20Embedded%20Toolchain,ZIP,,Windows,6-2017-q2-update
WIN_ARM_GCC_TOOLCHAIN_MD5=df6c2f763a6114c951e3f1e509af3cbc
WIN_ARM_GCC_TOOLCHAIN_LICENSE_URL=https://developer.arm.com/GetEula?Id=2d916619-954e-4adb-895d-b1ec657ae305
WIN_ARM_GCC_TOOLCHAIN_FILENAME=gcc-arm-none-eabi-6-2017-q2-update-win32.zip
WIN_ARM_GCC_TOOLCHAIN_VERSION=6-2017-q2
WIN_ARM_GCC_TOOLCHAIN_LOCATION=toolchains/gcc-arm-none-eabi/microhal

WIN_OPENOCD_URL=http://www.freddiechopin.info/en/download/category/4-openocd?download=154%3Aopenocd-0.10.0
WIN_OPENOCD_SHA256=f46687cd783a7a86716c78474e8132e32de84b773914f23f2226f81509ffcfca
WIN_OPENOCD_FILENAME=openocd-0.10.0.7z
WIN_OPENOCD_VERSION=0.10.0
WIN_OPENOCD_LOCATION=tools/openocd/0.10.0

WIN_ECLIPSE_URL=https://www.eclipse.org/downloads/download.php?file=/oomph/epp/oxygen/R/eclipse-inst-win64.exe\&r=1
WIN_ECLIPSE_SHA512=c585b52bf9da53812a14c9cbf48fa6beb0af983f52aa45e589c7e9cc4edce2a1819ebc87ccb4cd39104515a6d4e6adc6a4d2681d9744a041e9f0883d995349ea
WIN_ECLIPSE_FILENAME=eclipse-inst-win64.exe
WIN_ECLIPSE_LOCATION=eclipse

WIN_CLANG_TOOLCHAIN_URL=http://releases.llvm.org/4.0.1/LLVM-4.0.1-win64.exe
WIN_CLANG_TOOLCHAIN_FILENAME=LLVM-4.0.1-win64.exe
WIN_CLANG_TOOLCHAIN_VERSION=4.0.1

mkdir -p microide
cd microide

wget --directory-prefix=$DOWNLOAD_DIR https://github.com/microHAL/microIDE/archive/master.zip
echo 'Downloading ARM toolchain ...'
wget -O $DOWNLOAD_DIR/$ARM_GCC_TOOLCHAIN_FILENAME $ARM_GCC_TOOLCHAIN_URL
md5_local=$(md5sum "$DOWNLOAD_DIR/$ARM_GCC_TOOLCHAIN_FILENAME" | awk '{print $1}')
if [ "$md5_local" != "$ARM_GCC_TOOLCHAIN_MD5" ]
then
    echo $ARM_GCC_TOOLCHAIN_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $ARM_GCC_TOOLCHAIN_MD5
    echo Aborting...
    exit 1
fi
echo 'Downloading openOCD...'
wget -O $DOWNLOAD_DIR/$OPENOCD_FILENAME $OPENOCD_URL
md5_local=$(md5sum "$DOWNLOAD_DIR/$OPENOCD_FILENAME" | awk '{print $1}')
if [ "$md5_local" != "$OPENOCD_MD5" ]
then
    echo $OPENOCD_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $OPENOCD_MD5
    echo Aborting...
    exit 1
fi
echo 'Downloading Eclipse...'
wget -O $DOWNLOAD_DIR/$ECLIPSE_FILENAME $ECLIPSE_URL
local_sum=$(sha512sum "$DOWNLOAD_DIR/$ECLIPSE_FILENAME" | awk '{print $1}')
if [ "$local_sum" != "$ECLIPSE_SHA512" ]
then
    echo $ECLIPSE_FILENAME checksum missmatch.
    echo Calculated $local_sum
    echo Expected $ECLIPSE_SHA512
    echo Aborting...
    exit 1
fi

echo 'Downloading Windows files...'
echo 'Downloading ARM toolchain ...'
wget -O $DOWNLOAD_DIR/$WIN_ARM_GCC_TOOLCHAIN_FILENAME $WIN_ARM_GCC_TOOLCHAIN_URL
md5_local=$(md5sum "$DOWNLOAD_DIR/$WIN_ARM_GCC_TOOLCHAIN_FILENAME" | awk '{print $1}')
if [ "$md5_local" != "$WIN_ARM_GCC_TOOLCHAIN_MD5" ]
then
    echo $WIN_ARM_GCC_TOOLCHAIN_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $WIN_ARM_GCC_TOOLCHAIN_MD5
    echo Aborting...
    exit 1
fi
echo 'Downloading openOCD...'
wget -O $DOWNLOAD_DIR/$WIN_OPENOCD_FILENAME $WIN_OPENOCD_URL
local_sum=$(sha256sum "$DOWNLOAD_DIR/$WIN_OPENOCD_FILENAME" | awk '{print $1}')
if [ "$local_sum" != "$WIN_OPENOCD_SHA256" ]
then
    echo $WIN_OPENOCD_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $WIN_OPENOCD_SHA256
    echo Aborting...
    exit 1
fi
echo 'Downloading Eclipse...'
wget -O $DOWNLOAD_DIR/$WIN_ECLIPSE_FILENAME $WIN_ECLIPSE_URL
local_sum=$(sha512sum "$DOWNLOAD_DIR/$WIN_ECLIPSE_FILENAME" | awk '{print $1}')
if [ "$local_sum" != "$WIN_ECLIPSE_SHA512" ]
then
    echo $WIN_ECLIPSE_FILENAME checksum missmatch.
    echo Calculated $local_sum
    echo Expected $WIN_ECLIPSE_SHA512
    echo Aborting...
    exit 1
fi
echo 'Downloading clang...'
wget -O $DOWNLOAD_DIR/$WIN_CLANG_TOOLCHAIN_FILENAME $WIN_CLANG_TOOLCHAIN_URL
#signature_invalid=$(gpg --verify --no-default-keyring --keyring $DOWNLOAD_DIR/$WIN_CLANG_TOOLCHAIN_FILENAME LLVM-4.0.1-win64.exe.sig)
#if [ $signature_invalid ]
#then
#    echo $WIN_CLANG_TOOLCHAIN_FILENAME checksum missmatch.
#    echo Aborting...
#    exit 1
#fi




