#!/bin/sh

# This script was tested on ubuntu 16.04 LTS, it may require some changes to run on other versions

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

#links to installation files

VERSION=0.3.3
ARM_GCC_TOOLCHAIN_URL=https://developer.arm.com/-/media/Files/downloads/gnu-rm/7-2017q4/gcc-arm-none-eabi-7-2017-q4-major-linux.tar.bz2?revision=375265d4-e9b5-41c8-bf23-56cbe927e156?product=GNU%20Arm%20Embedded%20Toolchain,64-bit,,Linux,7-2017-q4-major
ARM_GCC_TOOLCHAIN_LICENSE_URL=https://developer.arm.com/GetEula?Id=b8689563-35c9-4da7-b0cf-9c21f422343c
ARM_GCC_TOOLCHAIN_FILENAME=gcc-arm-none-eabi-7-2017-q4-major-linux.tar.bz2
ARM_GCC_TOOLCHAIN_VERSION=7.2.0
ARM_GCC_TOOLCHAIN_SIZE=99857645
ARM_GCC_TOOLCHAIN_CHECKSUM=d3b00ae09e847747ef11316a8b04989a
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
ECLIPSE_SIZE=48063925
ECLIPSE_CHECKSUM=c8105a0d04c8aa105e282b955cb89c98
ECLIPSE_LOCATION=eclipse
MICROIDE_DIR=$SCRIPTPATH/microide-$VERSION
DOWNLOAD_DIR=./downloads
BRANCH_NAME=devel
APT_GET_PACKAGES_TO_INSTALL=''
APT_GET_REPOSITORYS_TO_ADD=''

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
echo 'Downloading HIDAPI (OpenOCD component)...'
wget -O $DOWNLOAD_DIR/hidapi.zip https://github.com/signal11/hidapi/archive/master.zip
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


installOpenOCD() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL autoconf libudev-dev libusb-1.0-0-dev libtool pkg-config"
    else         
        echo 'Installing HIDAPI ----------------------------------------------------------------' >> $MICROIDE_DIR/log.log  
        mkdir -p tmp
        if ! unzip $DOWNLOAD_DIR/hidapi.zip -d tmp >> $MICROIDE_DIR/log.log; then
            echo 'Unable to install HIDAPI, aborting -----------------------------------------------' >> $MICROIDE_DIR/log.log
            echo 'Unable to unzip repozitory files'
            echo 'Aborting...'
            exit 1
        fi 
        cd tmp/hidapi-master
        ./bootstrap >> $MICROIDE_DIR/log.log
        ./configure >> $MICROIDE_DIR/log.log
        echo 'Compilling HIDAPI ----------------------------------------------------------------' >> $MICROIDE_DIR/log.log
        make -j 4 >> $MICROIDE_DIR/log.log
        echo 'Installing (make install) HIDAPI -------------------------------------------------' >> $MICROIDE_DIR/log.log
        sudo make install 
        sudo ldconfig
        cd ../../
        
        echo 'Installing openOCD'    
        mkdir -p tools/openocd
        echo 'Extracting OpenOCD... ------------------------------------------------------------' >> $MICROIDE_DIR/log.log
        tar --extract --file=$DOWNLOAD_DIR/$OPENOCD_FILENAME -C tmp >> $MICROIDE_DIR/log.log
        echo 'Compilling OpenOCD'
        echo 'Compilling OpenOCD ---------------------------------------------------------------' >> $MICROIDE_DIR/log.log
        cd tmp/${OPENOCD_FILENAME%.tar.gz}
        ./configure --enable-stlink --enable-ti-icdi --enable-ulink --enable-cmsis-dap --enable-jlink --enable-oocd_trace --prefix=$MICROIDE_DIR/$OPENOCD_LOCATION >> $MICROIDE_DIR/log.log
        make -j 4 >> $MICROIDE_DIR/log.log
        echo 'Installing OpenOCD ---------------------------------------------------------------' >> $MICROIDE_DIR/log.log
        make install
        sudo cp contrib/60-openocd.rules /etc/udev/rules.d/
        sudo usermod -aG plugdev $USER
        cd ../../
        rm -r tmp
    fi
}

installARMToolchain() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL lib32z1 lib32ncurses5 libbz2-1.0:i386 lib32stdc++6"
    else 
        echo 'Installing ARM Toolchain...-------------------------------------------------------' >> log.log
        mkdir -p $ARM_GCC_TOOLCHAIN_LOCATION
        tar --extract --bzip2 --file=$DOWNLOAD_DIR/$ARM_GCC_TOOLCHAIN_FILENAME -C $ARM_GCC_TOOLCHAIN_LOCATION
        mv $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-linux.tar.bz2} $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-*-linux.tar.bz2}
        #installing microhal patch to toolchain, this will allow to use standart operating system library with FreeRTOS
        echo 'Patching ARM Toolchain.'
        echo 'Patching ARM Toolchain.-----------------------------------------------------------' >> log.log
        cp -r microIDE-$BRANCH_NAME/toolchains/gcc-arm-none-eabi-patch/${ARM_GCC_TOOLCHAIN_FILENAME%-*-linux.tar.bz2}/* $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-*-linux.tar.bz2}
    fi    
}

installEclipse() {
    MICROIDE_PRODUCTS_SETUP_FILE_CONTENT='<?xml version="1.0" encoding="UTF-8"?>
<setup:ProductCatalog
    xmi:version="2.0"
    xmlns:xmi="http://www.omg.org/XMI"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:setup="http://www.eclipse.org/oomph/setup/1.0"
	xmlns:setup.p2="http://www.eclipse.org/oomph/setup/p2/1.0"
    name="microide"
    label="microide Products">   
  <product
	href="file:'"$MICROIDE_DIR"'/eclipse-installer/microideLocalSetups/microide.product.setup#/"/>  
  <description>Default IDE for microhal project</description>
</setup:ProductCatalog>'

    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL default-jre"
    else 
        echo 'Installing Eclipse ---------------------------------------------------------------' >> log.log
        mkdir -p eclipse-installer
        # extract eclipse installer files:
        tar --extract --file=$DOWNLOAD_DIR/$ECLIPSE_FILENAME
        # redirect eclipse installer product index:
        cd eclipse-installer       
        echo '-Doomph.redirection.myProductsCatalog=index:/redirectable.products.setup->file:'"$MICROIDE_DIR"'/eclipse-installer/microideLocalSetups/microide.products.setup' >> eclipse-inst.ini
        echo '-Doomph.redirection.myProjectsCatalog=index:/redirectable.projects.setup->https://raw.githubusercontent.com/microHAL/microIDE/devel/eclipse-installer/microideSetups/microhal.projects.setup' >> eclipse-inst.ini
        echo '-Doomph.setup.product.catalog.filter=microide' >> eclipse-inst.ini
        # prepare directory for micride product setup files
        mkdir -p microideLocalSetups
        cd microideLocalSetups
        echo "$MICROIDE_PRODUCTS_SETUP_FILE_CONTENT" > microide.products.setup
        cd ../../
        cp -r microIDE-$BRANCH_NAME/eclipse-installer/microideLocalSetups/* eclipse-installer/microideLocalSetups
        mv eclipse-installer/microideLocalSetups/microide.product.setup.linux eclipse-installer/microideLocalSetups/microide.product.setup
        # set path to microide
        echo $MICROIDE_DIR
        sed -i -e 's,value="${installation.location|uri}",value="file:'"$MICROIDE_DIR"'",g' "eclipse-installer/microideLocalSetups/microide.product.setup"
        # remove files that are no longer needed
        rm eclipse-installer/microideLocalSetups/microide.product.setup.windows
        rm -r microIDE-$BRANCH_NAME         
    fi
}

installClangFormat() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL clang-format-5.0"
    fi 
    #sudo apt-get install clang-format
}

installCppcheck() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL cppcheck"
    fi 
}

installGCC() {
    if ! [ -x "$(command -v gcc)" ]; then
        if ! [ -x "$(command -v gcc-7)" ]; then  
            echo "Unable to find gcc, adding to instalation list"
            APT_GET_REPOSITORYS_TO_ADD="$APT_GET_REPOSITORYS_TO_ADD ppa:ubuntu-toolchain-r/test"
            APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL gcc-7"
        fi
    else
        currentver="$(gcc -dumpversion)"
        requiredver="7"
        if [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
            echo "GCC already installed"
        else
            if ! [ -x "$(command -v gcc-7)" ]; then  
                echo "Unable to find gcc, adding to instalation list"
                APT_GET_REPOSITORYS_TO_ADD="$APT_GET_REPOSITORYS_TO_ADD ppa:ubuntu-toolchain-r/test"
                APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL gcc-7"
            else
                currentver="$(gcc-7 -dumpversion)"
                requiredver="7"
                if ! [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
                    echo "Unable to find gcc with version 7 or abowe, adding to instalation list"
                    APT_GET_REPOSITORYS_TO_ADD="$APT_GET_REPOSITORYS_TO_ADD ppa:ubuntu-toolchain-r/test"
                    APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL gcc-7"
               fi
            fi
        fi 
    fi
}

checkArchitecture() {
    if [ "$(uname -i)" != "x86_64" ]; then
        echo "This script can be used only on 64 bit systems. Aborting."
        exit 1
    fi
}

instal() {
    checkArchitecture
    echo 'Installing required packages:'
    installARMToolchain 'addAptToGetPackagesToInstall'
    installOpenOCD 'addAptToGetPackagesToInstall'
    installEclipse 'addAptToGetPackagesToInstall'
    installClangFormat 'addAptToGetPackagesToInstall'
    installCppcheck 'addAptToGetPackagesToInstall'
    installGCC
    echo $APT_GET_PACKAGES_TO_INSTALL
    echo $APT_GET_REPOSITORYS_TO_ADD

    if [ "$APT_GET_REPOSITORYS_TO_ADD" != "" ]; then
        sudo add-apt-repository $APT_GET_REPOSITORYS_TO_ADD
    fi
    sudo apt-get update
    sudo apt-get install $APT_GET_PACKAGES_TO_INSTALL

    #------------------------------------- toolchains -----------------------------
    echo 'Unpacking toolchain patch and eclipse installer setup configuration.'
    echo 'Unpacking toolchain patch and eclipse installer setup configuration.---------------' >> log.log
    if ! unzip $DOWNLOAD_DIR/$BRANCH_NAME.zip >> log.log; then
        echo 'Unable to unzip repozitory files'
        echo 'Aborting...'
        exit 1
    fi 
    echo 'Installing ARM Toolchain...'
    installARMToolchain
    # ------------------------------------ tools ---------------------------------
    echo 'Installing tools'
    installOpenOCD
    # ---------------------------------- eclipse ---------------------------------
    echo 'Installing Eclipse'
    installEclipse
    #install clang-format
    installClangFormat

    #removing not needed files
    rm -r $DOWNLOAD_DIR

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




  
 
