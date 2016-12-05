#!/bin/sh

mkdir microide
cd microide
#------------------------------------- toolchains -----------------------------
echo 'Installing ARM Toolchain...'
echo 'Creating directory for toolchains...'
mkdir -p toolchains
echo 'Creating directory for gcc ARM toolchains...'
mkdir -p toolchains/arm-none-eabi-gcc
echo '--> Installing GCC ARM toolchain from launchpad website <--'
echo 'Creating directory for ARM GCC from launchpad'
mkdir -p toolchains/arm-none-eabi-gcc/microhal
GCC_ARM_LAUNCHPAD_TOOLCHAIN_FILENAME=gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2
#echo $GCC_ARM_LAUNCHPAD_TOOLCHAIN_FILENAME
echo 'Downloading toolchain...'
#wget https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q3-update/+download/gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2
wget https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2
echo 'Extracting toolchain...'
tar --extract --bzip2 --file=$GCC_ARM_LAUNCHPAD_TOOLCHAIN_FILENAME -C toolchains/arm-none-eabi-gcc/microhal
#installing microhal patch to toolchain, this will allow to use standart operating system library with FreeRTOS
wget https://github.com/microHAL/microIDE/archive/master.zip
unzip master.zip microIDE-master/toolchains/*
cp -r microIDE-master/toolchains/gcc-arm-none-eabi-5_3-patch/* toolchains/arm-none-eabi-gcc/microhal/gcc-arm-none-eabi-5_3-2016q1

# ------------------------------------ tools ---------------------------------
echo 'Installing tools'
echo 'Installing openOCD'
echo 'Creating directory for openOCD'
mkdir -p tools/openocd
echo 'Downloading openOCD...'
wget -O openocd-0.9.0.tar.bz2 https://sourceforge.net/projects/openocd/files/openocd/0.9.0/openocd-0.9.0.tar.bz2/download
echo 'Extracting openOCD...'
tar --extract --bzip2 --file=openocd-0.9.0.tar.bz2 -C tools/openocd

# ---------------------------------- eclipse ---------------------------------
echo 'Installing Eclipse'
echo 'Downloading...'
wget http://mirrors.nic.cz/eclipse/oomph/products/eclipse-inst-linux64.tar.gz
tar --extract --file=eclipse-inst-linux64.tar.gz
#redirect eclipse installer product index
cd eclipse-installer
echo '-Doomph.redirection.setups=http://git.eclipse.org/c/oomph/org.eclipse.oomph.git/plain/setups/->setups/' >> eclipse-inst.ini
cd ../
unzip master.zip microIDE-master/eclipse-installer/setups/* 
mkdir -p eclipse-installer/setups
cp -r microIDE-master/eclipse-installer/setups/* eclipse-installer/setups
rm -r microIDE-master


#starting eclipse installer
./eclipse-installer/eclipse-inst




  
 
