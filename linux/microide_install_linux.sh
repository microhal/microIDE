#!/bin/sh

# This script was tested on ubuntu 18.04 LTS, it may require some changes to run on other versions

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

#links to installation files

VERSION=0.3.5
ARM_GCC_TOOLCHAIN_URL=https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2018q4/gcc-arm-none-eabi-8-2018-q4-major-linux.tar.bz2?revision=d830f9dd-cd4f-406d-8672-cca9210dd220?product=GNU%20Arm%20Embedded%20Toolchain,64-bit,,Linux,8-2018-q4-major
ARM_GCC_TOOLCHAIN_LICENSE_URL=https://developer.arm.com/GetEula?Id=3703e685-a548-462c-bd0e-2e139db7ab35
ARM_GCC_TOOLCHAIN_FILENAME=gcc-arm-none-eabi-8-2018-q4-major-linux.tar.bz2
ARM_GCC_TOOLCHAIN_VERSION=8.0.0
ARM_GCC_TOOLCHAIN_SIZE=107253352
ARM_GCC_TOOLCHAIN_CHECKSUM=f55f90d483ddb3bcf4dae5882c2094cd
ARM_GCC_TOOLCHAIN_LOCATION=toolchains/gcc-arm-none-eabi/microhal

GCC_ARM_LINUX_GNUEABIHF_TOOLCHAIN_URL=https://releases.linaro.org/components/toolchain/binaries/latest-7/arm-linux-gnueabihf/gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabihf.tar.xz
GCC_ARM_LINUX_GNUEABIHF_LICENSE_URL=
GCC_ARM_LINUX_GNUEABIHF_FILENAME=gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabihf.tar.xz
GCC_ARM_LINUX_GNUEABIHF_VERSION=7.3.1
GCC_ARM_LINUX_GNUEABIHF_SIZE=107031352
GCC_ARM_LINUX_GNUEABIHF_CHECKSUM=e414dc2bbd2bbd2f3b10edad0792fdb3
GCC_ARM_LINUX_GNUEABIHF_LOCATION=toolchains/gcc-arm-linux-gnueabihf

XTENSA_ESP32_ELF_TOOLCHAIN_URL=https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
XTENSA_ESP32_ELF_LICENSE_URL=
XTENSA_ESP32_ELF_FILENAME=xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
XTENSA_ESP32_ELF_VERSION=5.2.0
XTENSA_ESP32_ELF_SIZE=44219107
XTENSA_ESP32_ELF_CHECKSUM=3e00f8faa7360ebfc39971d2d2f3522d
XTENSA_ESP32_ELF_LOCATION=toolchains/xtensa-esp32-elf

OPENOCD_URL=https://sourceforge.net/projects/openocd/files/openocd/0.10.0/openocd-0.10.0.tar.gz/download
OPENOCD_FILENAME=openocd-0.10.0.tar.gz
OPENOCD_VERSION=0.10.0
OPENOCD_SIZE=6124274
OPENOCD_CHECKSUM=8971d16aee5c2642b33ee55fc6c86239
OPENOCD_LOCATION=tools/openocd/0.10.0

ECLIPSE_URL=http://www.eclipse.org/downloads/download.php?file=/oomph/products/latest/eclipse-inst-linux64.tar.gz\&r=1
ECLIPSE_FILENAME=eclipse-inst-linux64.tar.gz
ECLIPSE_VERSION=oxygen
ECLIPSE_SIZE=50140599
ECLIPSE_CHECKSUM=54f451ae0e5e2725d6192ac962a7a0c7
ECLIPSE_LOCATION=eclipse
MICROIDE_DIR=$SCRIPTPATH/microide-$VERSION
DOWNLOAD_DIR=./downloads
BRANCH_NAME=devel
APT_GET_PACKAGES_TO_INSTALL=''
APT_GET_REPOSITORYS_TO_ADD=''

download() {
wget --directory-prefix=$DOWNLOAD_DIR https://github.com/microHAL/microIDE/archive/$BRANCH_NAME.zip
echo '--- Downloading gcc-arm-none-eabi toolchain ...'
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
echo '--- Downloading gcc-arm-linux-gnueabihf toolchain ...'
wget -O $DOWNLOAD_DIR/$GCC_ARM_LINUX_GNUEABIHF_FILENAME $GCC_ARM_LINUX_GNUEABIHF_TOOLCHAIN_URL
md5_local=$(md5sum "$DOWNLOAD_DIR/$GCC_ARM_LINUX_GNUEABIHF_FILENAME" | awk '{print $1}')
if [ "$md5_local" != "$GCC_ARM_LINUX_GNUEABIHF_CHECKSUM" ]
then
    echo $GCC_ARM_LINUX_GNUEABIHF_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $GCC_ARM_LINUX_GNUEABIHF_CHECKSUM
    echo Aborting...
    exit 1
fi
echo '--- Downloading xtensa-esp32-elf toolchain ...'
wget -O $DOWNLOAD_DIR/$XTENSA_ESP32_ELF_FILENAME $XTENSA_ESP32_ELF_TOOLCHAIN_URL
md5_local=$(md5sum "$DOWNLOAD_DIR/$XTENSA_ESP32_ELF_FILENAME" | awk '{print $1}')
if [ "$md5_local" != "$XTENSA_ESP32_ELF_CHECKSUM" ]
then
    echo $XTENSA_ESP32_ELF_FILENAME checksum missmatch.
    echo Calculated $md5_local
    echo Expected $XTENSA_ESP32_ELF_CHECKSUM
    echo Aborting...
    exit 1
fi
echo '--- Downloading openOCD...'
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
echo '--- Downloading HIDAPI (OpenOCD component)...'
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
        ./configure CFLAGS='-Wno-implicit-fallthrough' >> $MICROIDE_DIR/log.log
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
        ./configure CFLAGS='-Wno-implicit-fallthrough -Wno-error=format-overflow=' --enable-stlink --enable-ti-icdi --enable-ulink --enable-cmsis-dap --enable-jlink --enable-oocd_trace --prefix=$MICROIDE_DIR/$OPENOCD_LOCATION >> $MICROIDE_DIR/log.log
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
        #mv $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-linux.tar.bz2} $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-linux.tar.bz2}
        #installing microhal patch to toolchain, this will allow to use standart operating system library with FreeRTOS
        echo 'Patching ARM Toolchain.'
        echo 'Patching ARM Toolchain.-----------------------------------------------------------' >> log.log
        cp -r microIDE-$BRANCH_NAME/toolchains/gcc-arm-none-eabi-patch/${ARM_GCC_TOOLCHAIN_FILENAME%-linux.tar.bz2}/* $ARM_GCC_TOOLCHAIN_LOCATION/${ARM_GCC_TOOLCHAIN_FILENAME%-linux.tar.bz2}
    fi    
}

installARM_LINUX_GNUEABIHF_Toolchain() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL"
    else
        echo 'Installing gcc-arm-linux-gnueabihf Toolchain...-------------------------------------------------------' >> log.log
        mkdir -p $GCC_ARM_LINUX_GNUEABIHF_LOCATION
        tar xf $DOWNLOAD_DIR/$GCC_ARM_LINUX_GNUEABIHF_FILENAME -C $GCC_ARM_LINUX_GNUEABIHF_LOCATION
    fi
}

installXTENSA_ESP32_ELF_Toolchain() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL libncurses-dev flex bison gperf python python-serial"
    else
        echo 'Installing xtensa-esp32-elf Toolchain...-------------------------------------------------------' >> log.log
        mkdir -p $XTENSA_ESP32_ELF_LOCATION
        tar xf $DOWNLOAD_DIR/$XTENSA_ESP32_ELF_FILENAME -C $XTENSA_ESP32_ELF_LOCATION
    fi
}

install_esp_idf() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL"
    else
        echo 'Installing ESP-IDF ...-------------------------------------------------------' >> log.log
        git clone -b v3.1.2 --recursive https://github.com/espressif/esp-idf.git
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
        echo "-Doomph.setup.install.root=$MICROIDE_DIR" >> eclipse-inst.ini
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
        rm -r microIDE-$BRANCH_NAME         
    fi
}

installClangFormat() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
    	APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL clang-format-6.0"
    fi
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
        #    APT_GET_REPOSITORYS_TO_ADD="$APT_GET_REPOSITORYS_TO_ADD ppa:ubuntu-toolchain-r/test"
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
            #    APT_GET_REPOSITORYS_TO_ADD="$APT_GET_REPOSITORYS_TO_ADD ppa:ubuntu-toolchain-r/test"
                APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL gcc-7"
            else
                currentver="$(gcc-7 -dumpversion)"
                requiredver="7"
                if ! [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
                    echo "Unable to find gcc with version 7 or abowe, adding to instalation list"
             #       APT_GET_REPOSITORYS_TO_ADD="$APT_GET_REPOSITORYS_TO_ADD ppa:ubuntu-toolchain-r/test"
                    APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL gcc-7"
               fi
            fi
        fi 
    fi
}

installDoxygen() {
    if [ "$1" = "addAptToGetPackagesToInstall" ]; then
        APT_GET_PACKAGES_TO_INSTALL="$APT_GET_PACKAGES_TO_INSTALL doxygen"
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
    installARM_LINUX_GNUEABIHF_Toolchain 'addAptToGetPackagesToInstall'
    installXTENSA_ESP32_ELF_Toolchain 'addAptToGetPackagesToInstall'
    installOpenOCD 'addAptToGetPackagesToInstall'
    installEclipse 'addAptToGetPackagesToInstall'
    installClangFormat 'addAptToGetPackagesToInstall'
    installCppcheck 'addAptToGetPackagesToInstall'
    installDoxygen 'addAptToGetPackagesToInstall'
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
    echo '**************** Installing ARM Toolchain...'
    installARMToolchain

    echo '**************** Installing gcc-arm-linux-gnueabihf Toolchain...'
    installARM_LINUX_GNUEABIHF_Toolchain

    echo '**************** Installing xtensa-esp32-elf Toolchain...'
    installXTENSA_ESP32_ELF_Toolchain
    echo '------ Installing ESP-IDF...'
    install_esp_idf
    # ------------------------------------ tools ---------------------------------
    echo 'Installing tools'
    installOpenOCD
    # ---------------------------------- eclipse ---------------------------------
    echo '**************** Installing Eclipse'
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




  
 
