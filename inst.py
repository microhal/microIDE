#!/usr/bin/env python

import os
import hashlib
import shutil
import re
import argparse
import subprocess

microideVersion = '0.3.2'

armGccToolchain_old_gcc5 = {
    'filename' : 'gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2',
    'size' : '0',
    'version' : '6.2.0',
    'url' : 'https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2', 
    'checksum' : {'md5' : '5a261cac18c62d8b7e8c70beba2004bd'},
    'licenseUrl' : 'https://launchpadlibrarian.net/251686212/license.txt',
    'installationLocation' : '${microide}/toolchains/gcc-arm-none-eabi/microhal'
}

armGccToolchain_6_2016_q2 = {
    'filename' : 'gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2',
    'size' : '0',
    'version' : '6.2.0',
    'url' : 'https://developer.arm.com/-/media/Files/downloads/gnu-rm/6-2017q2/gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2?revision=2cc92fb5-3e0e-402d-9197-bdfc8224d8a5?product=GNU%20Arm%20Embedded%20Toolchain,64-bit,,Linux,6-2017-q2-update',
    'checksum' : {'md5' : '13747255194398ee08b3ba42e40e9465'},
    'licenseUrl' : 'https://developer.arm.com/GetEula?Id=2d916619-954e-4adb-895d-b1ec657ae305',
    'installationLocation' : '${microide}/toolchains/gcc-arm-none-eabi/microhal'
}

armGccToolchain_7_2017_q4 = {
    'filename' : 'gcc-arm-none-eabi-7-2017-q4-major-linux.tar.bz2',
    'size' : '0',
    'version' : '7.2.0',
    'url' : 'https://developer.arm.com/-/media/Files/downloads/gnu-rm/7-2017q4/gcc-arm-none-eabi-7-2017-q4-major-linux.tar.bz2?revision=375265d4-e9b5-41c8-bf23-56cbe927e156?product=GNU%20Arm%20Embedded%20Toolchain,64-bit,,Linux,7-2017-q4-major',
    'checksum' : {'md5' : 'd3b00ae09e847747ef11316a8b04989a'},
    'licenseUrl' : 'https://developer.arm.com/GetEula?Id=b8689563-35c9-4da7-b0cf-9c21f422343c',
    'installationLocation' : '${microide}/toolchains/gcc-arm-none-eabi/microhal'
}

openOCD = {
    'filename' : 'openocd-0.10.0.tar.gz',
    'size' : '0',
    'version' : '0.10.0',
    'url' : 'https://sourceforge.net/projects/openocd/files/openocd/0.10.0/openocd-0.10.0.tar.gz/download',
    'checksum' : {'md5' : '8971d16aee5c2642b33ee55fc6c86239'},
    'installationLocation' : 'tools/openocd/0.10.0'
}

eclipse = {
    'filename' : 'eclipse-inst-linux64.tar.gz',
    'size' : '0',
    'version' : 'oxygen',
    'url' : 'http://www.eclipse.org/downloads/download.php?file=/oomph/products/latest/eclipse-inst-linux64.tar.gz\&r=1',
    'checksum' : {'' : ''},
    'installationLocation' : 'eclipse'
}

# ------------------------------------- windows version
winArmGccToolchain_7_2017_q4 = {
    'filename' : 'gcc-arm-none-eabi-7-2017-q4-major-win32.exe',
    'size' : '0',
    'version' : '7.2.0',
    'url' : 'https://developer.arm.com/-/media/Files/downloads/gnu-rm/7-2017q4/gcc-arm-none-eabi-7-2017-q4-major-win32.exe?revision=732bae94-c929-403d-9520-0b2bccd81ad7?product=GNU%20Arm%20Embedded%20Toolchain,32-bit,,Windows,7-2017-q4-major', 
    'checksum' : {'md5' : 'bb4def39ff1cb3ff5d2931597d9aea4e'},
    'licenseUrl' : 'https://developer.arm.com/GetEula?Id=b8689563-35c9-4da7-b0cf-9c21f422343c',
    'installationLocation' : '{app}\\toolchains\\gcc-arm-none-eabi\\microhal'
}

winArmGccToolchain_5_3_2016 = {
    'filename' : 'gcc-arm-none-eabi-5_3-2016q1-20160330-win32.exe',
    'size' : '0',
    'version' : '5.3.0',
    'url' : 'https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-win32.exe', 
    'checksum' : {'' : ''},
    'licenseUrl' : 'https://launchpadlibrarian.net/251686212/license.txt',
    'installationLocation' : '{app}\\toolchains\\gcc-arm-none-eabi\\microhal'
}

winClangToolchain = {
    'filename' : 'LLVM-3.8.0-win64.exe',
    'size' : '0',
    'version' : '3.8.0',
    'url' : 'http://llvm.org/releases/3.8.0/LLVM-3.8.0-win64.exe', 
    'checksum' : {'' : ''},
    'licenseUrl' : 'https://launchpadlibrarian.net/251686212/license.txt',
    'installationLocation' : '{app}\\toolchains\\LLVM\\3.8.0'
}


winMinGwToolchain = {
    'filename' : 'x86_64-7.1.0-release-win32-seh-rt_v5-rev2.7z',
    'size' : '0',
    'version' : '',
    'url' : 'https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-win32/seh/x86_64-7.1.0-release-win32-seh-rt_v5-rev2.7z', 
    'checksum' : {'md5' : 'bd537f46793fc11b7b161f071e9ef31e'},
    'licenseUrl' : 'http://sourceforge.net/projects/mingw-w64/',
    'installationLocation' : '{app}\\toolchains\\mingw-w64'
}

winOpenOCD = {
    'filename' : 'openocd-0.10.0.7z',
    'size' : '0',
    'version' : '0.10.0',
    'url' : 'http://www.freddiechopin.info/en/download/category/4-openocd?download=154%3Aopenocd-0.10.0',             
    'checksum' : {'SHA256' : 'f46687cd783a7a86716c78474e8132e32de84b773914f23f2226f81509ffcfca'},
    'installationLocation' : "{app}\\tools\\openocd\\0.10.0"
}

winDoxygen = {
    'filename' : 'doxygen-1.8.13-setup.exe',
    'size' : '0',
    'version' : '1.8.13',
    'url' : 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.13-setup.exe',
    'checksum' : {'' : ''},
    'licenseUrl' : 'http://www.stack.nl/~dimitri/doxygen/index.html',
    'installationLocation' : "{app}\\tools\\doxygen\\1.8.13"
}

winEclipse = {
    'filename' : 'eclipse-inst-win64.exe',
    'size' : '0',
    'version' : 'oxygen',
    'url' : 'http://www.eclipse.org/downloads/download.php?file=/oomph/products/latest/eclipse-inst-win64.exe\&r=1',
    'checksum' : {'' : ''},
    'installationLocation' : 'eclipse'
}

armGccToolchain = armGccToolchain_7_2017_q4
winArmGccToolchain = winArmGccToolchain_7_2017_q4
linuxFiles = [armGccToolchain, openOCD, eclipse]
windowsFiles = [winArmGccToolchain, winClangToolchain, winMinGwToolchain, winOpenOCD, winDoxygen, winEclipse]
allFiles = linuxFiles + windowsFiles

# ------------------------------------ end of file declaration

def download(destynation, filename, url, checksum):
    if destynation:
        destynation = destynation + "/"

    parameters = "wget -O ./" + destynation + filename + ' ' + url
    os.system(parameters  + " >> output.log")
    if checksum.has_key('md5') == True:
        if hashlib.md5(open('./'  + destynation + filename,'rb').read()).hexdigest() != checksum['md5']:
            return [False, 0]
    if checksum.has_key('SHA512') == True:
        if hashlib.sha512(open('./' + destynation + filename,'rb').read()).hexdigest() != checksum['SHA512']:
            return [False, 0]
    if checksum.has_key('SHA256') == True:
        if hashlib.sha256(open('./'  + destynation + filename,'rb').read()).hexdigest() != checksum['SHA256']:
            return [False, 0]

    return [True, os.stat('./'  + destynation + filename).st_size]
    

def generateLinuxProductSetup():
    with open('templates/microide.product.setup.template', 'r') as file:
        content = file.read()
#    toolchainPatch = armGccToolchain['installationLocation'] + '/' + re.sub('-\d{8}-linux.tar.bz2', '', armGccToolchain['filename']) // for gcc 5
    toolchainPatch = armGccToolchain['installationLocation'] + '/' + re.sub('-.{5,6}-linux\.tar\.bz2', '', armGccToolchain['filename'])
    content = content.replace("##microideToolchainPatch##", toolchainPatch)

    content = content.replace("##clangFormatLocation##", "/usr/bin/clang-format")

    content = content.replace("##MinGWToolchainPatch##", "/usr/bin")

    content = content.replace("##DoxygenPatch##", "/usr/bin")

    with open('eclipse-installer/setups/microIDE/microide.product.setup.linux', 'w') as file:
        file.write(content)

def generateWindowsProductSetup():
    with open('templates/microide.product.setup.template', 'r') as file:
        content = file.read()
    toolchainPatch = winArmGccToolchain['installationLocation'].replace('{app}', '${microide}') + '\\' + re.sub('-.{5,6}-win32\.exe', '', winArmGccToolchain['filename'])
    content = content.replace("##microideToolchainPatch##", toolchainPatch.replace('/', '\\'))
    
    clangPath = winClangToolchain['installationLocation']
    clangPath = clangPath.replace('{app}', '${microide|file}') + '/bin/clang-format.exe'
    content = content.replace("##clangFormatLocation##", clangPath.replace('/', '\\' ))

    mingwPath = winMinGwToolchain['installationLocation']
    mingwPath = mingwPath.replace('{app}', '${microide}') 
    content = content.replace("##MinGWToolchainPatch##", mingwPath.replace('/', '\\' ))

    doxygenPath = winDoxygen['installationLocation']
    doxygenPath = doxygenPath.replace('{app}', '${microide|file}') + '/bin'
    content = content.replace("##DoxygenPatch##", doxygenPath)

    with open('eclipse-installer/setups/microIDE/microide.product.setup.windows', 'w') as file:
        file.write(content)


def generateLinuxInstaller():
    with open('templates/microide_install.template', 'r') as file:
        content = file.read()
    text = 'VERSION=' + microideVersion + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_URL=' + armGccToolchain['url'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_LICENSE_URL=' + armGccToolchain['licenseUrl'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_FILENAME=' + armGccToolchain['filename'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_VERSION=' + armGccToolchain['version'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_SIZE=' + str(armGccToolchain['size']) + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_CHECKSUM=' + armGccToolchain['checksum']['md5'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_LOCATION=' + armGccToolchain['installationLocation'].replace('${microide}/', '')
    text = text + '\n\nOPENOCD_URL=' + openOCD['url'] 
    text = text + '\nOPENOCD_FILENAME=' + openOCD['filename']
    text = text + '\nOPENOCD_VERSION=' + openOCD['version']
    text = text + '\nOPENOCD_SIZE=' + str(openOCD['size'])
    text = text + '\nOPENOCD_CHECKSUM=' + openOCD['checksum']['md5']
    text = text + '\nOPENOCD_LOCATION=' + openOCD['installationLocation'] 
    text = text + '\n\nECLIPSE_URL=' + eclipse['url'] + '\nECLIPSE_FILENAME=' + eclipse['filename'] + '\nECLIPSE_VERSION=' + eclipse['version'] + '\nECLIPSE_SIZE=' + str(eclipse['size']) + '\nECLIPSE_CHECKSUM=' + eclipse['checksum']['md5'] + '\nECLIPSE_LOCATION=' + eclipse['installationLocation']

    content = content.replace("#replace this text with instalation files information", text)

    with open('linux/microide_install.sh', 'w') as file:
        file.write(content)    

def recursiveRemoveNotListedFiles(directory, filesToPath):    
    for root, subdirs, files in os.walk(directory, topdown=False):
        for filename in files:
            file_path = os.path.join(root, filename)
    #        print('\t- file %s (full path: %s)' % (filename, file_path))
            if filename not in filesToPath:
                os.remove(file_path)

        for subdir in subdirs:
            #print('\t- subdirectory ' + subdir)
            if os.path.isdir(subdir):
                if not os.listdir(subdir):
                    os.rmdir(subdir)

        if not os.listdir(root):
            os.rmdir(root)

def replaceRecursive(destination, sourcefiledir, sourcefilename):
    replaceCounter = 0
    for root, subdirs, files in os.walk(destination):
        for filename in files:
            file_path = os.path.join(root, filename)    
            if filename == sourcefilename:
                shutil.copy(sourcefiledir + "/" + sourcefilename, file_path)
                replaceCounter = replaceCounter + 1
    print "Replaced " + str(replaceCounter) + " files"


def verifyWindowsDownloads(destdir):
    destdir = destdir + '/windows'
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    files = windowsFiles 
    for file in files:
        status = download(destdir, file['filename'], file['url'], file['checksum'])    
        if status[0] == False:
            print "An error occurred" 
            exit(-1) 

def verifyLinuxDownloads(destdir):
    destdir = destdir + '/linux'
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    files = linuxFiles
    for file in files:
        status = download(destdir, file['filename'], file['url'], file['checksum'])    
        if status[0] == False:
            print "An error occurred"
            exit(-1) 

def getFiles(destdir):
    verifyLinuxDownloads(destdir)
    verifyWindowsDownloads(destdir)    

def fileExists(path):    
    try:
        st = os.stat(path)
    except os.error:
        return False
    return True

# this function will return path to first file with name passed as a parameter    
def findFile(directory, filename):
    for root, subdirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, filename)
    #        print('\t- file %s (full path: %s)' % (filename, file_path))
            if file == filename:
                return file_path
    return ''

def mergeFiles(fileA, fileB):    
    subprocess.check_call(["meld", fileA, fileB])

#this function will update:
# - file size
# - MD5 checksum
def updateFileinfo(destdir, files):
    if destdir:
        destdir = destdir + "/"    

    for file in files:
        filePath = './'  + destdir + file['filename']
        if fileExists(filePath):
            file['size'] = os.stat(filePath).st_size    
            if file['checksum'].has_key('md5') == False:
                file['checksum']['md5'] = hashlib.md5(open(filePath,'rb').read()).hexdigest()    
        else:
            print "An error occurred, while updating file info: " + filePath
            exit(-1) 

def getMissingFiles(destdir, files):
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    if destdir:
        destdir = destdir + "/"    

    for file in files:
        filePath = './'  + destdir + file['filename']
        if fileExists(filePath) == False:    
            download(destdir, file['filename'], file['url'], file['checksum'])
        else:
            print "File exist, no need to download: " + filePath




def generateInnoSetupFile():
    with open('templates/microide.iss.template', 'r') as file:
        content = file.read()

    text = '#define AppVersion "' + microideVersion + '"\n\n'
    text = text + '#define ARM_GCC_TOOLCHAIN_URL "' + winArmGccToolchain['url'] + '"\n'
    text = text + '#define ARM_GCC_TOOLCHAIN_LICENSE_URL "' + winArmGccToolchain['licenseUrl'] + '"\n'
    text = text + '#define ARM_GCC_TOOLCHAIN_FILENAME "' + winArmGccToolchain['filename'] + '"\n'
    text = text + '#define ARM_GCC_TOOLCHAIN_VERSION "' + winArmGccToolchain['version'] + '"\n'
    text = text + '#define ARM_GCC_TOOLCHAIN_SIZE ' + str(winArmGccToolchain['size']) + '\n'
    text = text + '#define ARM_GCC_TOOLCHAIN_LOCATION "' + winArmGccToolchain['installationLocation'] + '\\' + re.sub('-.{5,6}-win32\.exe', '', winArmGccToolchain['filename']) + '"\n'

    text = text + '#define CLANG_TOOLCHAIN_URL "' + winClangToolchain['url'] + '"\n'
    text = text + '#define CLANG_TOOLCHAIN_FILENAME "' + winClangToolchain['filename'] + '"\n'
    text = text + '#define CLANG_TOOLCHAIN_VERSION "' + winClangToolchain['version'] + '"\n'
    text = text + '#define CLANG_TOOLCHAIN_SIZE ' + str(winClangToolchain['size']) + '\n'
    text = text + '#define CLANG_TOOLCHAIN_LOCATION "' + winClangToolchain['installationLocation'] + '"\n'  

    text = text + '#define OPENOCD_URL "' + winOpenOCD['url'] + '"\n'
    text = text + '#define OPENOCD_FILENAME "' + winOpenOCD['filename'] +'"\n'
    text = text + '#define OPENOCD_VERSION "' + winOpenOCD['version'] + '"\n'
    text = text + '#define OPENOCD_SIZE ' + str(winOpenOCD['size']) + '\n'
    text = text + '#define OPENOCD_LOCATION "' + winOpenOCD['installationLocation'] + '"\n'

    text = text + '#define DOXYGEN_URL "' + winDoxygen['url'] + '"\n'
    text = text + '#define DOXYGEN_LICENSE_URL "' + winDoxygen['licenseUrl'] + '"\n'
    text = text + '#define DOXYGEN_FILENAME "' + winDoxygen['filename'] +'"\n'
    text = text + '#define DOXYGEN_VERSION "' + winDoxygen['version'] + '"\n'
    text = text + '#define DOXYGEN_SIZE ' + str(winDoxygen['size']) + '\n'
    text = text + '#define DOXYGEN_LOCATION "' + winDoxygen['installationLocation'] + '"\n'

    text = text + '#define MINGW_URL "' + winMinGwToolchain['url'] + '"\n'
    text = text + '#define MINGW_LICENSE_URL "' + winMinGwToolchain['licenseUrl'] + '"\n'
    text = text + '#define MINGW_FILENAME "' + winMinGwToolchain['filename'] +'"\n'
    text = text + '#define MINGW_VERSION "' + winMinGwToolchain['version'] + '"\n'
    text = text + '#define MINGW_SIZE ' + str(winMinGwToolchain['size']) + '\n'
    text = text + '#define MINGW_LOCATION "' + winMinGwToolchain['installationLocation'] + '"\n'


    content = content.replace("#replace this text with instalation files information", text)

    with open('windows/microide.iss', 'w') as file:
        file.write(content)

def download7zipStandaloneConsoleVersion():
    filename = '7z1604-extra.7z'
    dest = 'norepo/windows'
    download(dest, filename, 'http://www.7-zip.org/a/7z1604-extra.7z', {})

    os.system("mkdir -p windows/tools/7z1604-extra >> output.log")
    parameters = '7za x ' + dest + '/' + filename + ' -y -owindows/tools/7z1604-extra'
    os.system(parameters + " >> output.log")

def compileWindowsInstaller():    
    downloadDir = 'norepo/windows'
    # do some clenup
    shutil.rmtree('windows/eclipse-installer', ignore_errors=True)
    shutil.rmtree('windows/toolchainPatch', ignore_errors=True)

    # prepare installer
    download7zipStandaloneConsoleVersion() # needed to unpack repositorys while installing on windows
    getMissingFiles(downloadDir, [winEclipse]) # we need to download and include pathed version of eclipse installer into microide installer
    #extracting eclipse files
    command = '7za x ' + downloadDir + '/' + winEclipse['filename'] + ' -y -owindows/eclipse-installer'
    os.system(command)
    os.remove('windows/eclipse-installer/extractor.exe')
    #pathing eclipse installer
    with open('windows/eclipse-installer/eclipse-inst.ini', 'a') as iniFile:
        iniFile.write('-Doomph.redirection.setups=http://git.eclipse.org/c/oomph/org.eclipse.oomph.git/plain/setups/->setups/')    
    generateWindowsProductSetup() # generate oomph setup files for windows
    # copying oomph setup files
    shutil.copytree('eclipse-installer/setups', 'windows/eclipse-installer/setups')
    os.remove('windows/eclipse-installer/setups/microIDE/microide.product.setup.linux')
    os.rename('windows/eclipse-installer/setups/microIDE/microide.product.setup.windows', 'windows/eclipse-installer/setups/microIDE/microide.product.setup')
    # include toolchain patch files into installer, firstly copy patch files into proper directory
    patchDirectoryName = re.sub('-.{5,6}-win32\.exe', '', winArmGccToolchain['filename'])
    shutil.copytree('toolchains/gcc-arm-none-eabi-patch/' + patchDirectoryName, 'windows/toolchainPatch/' + patchDirectoryName)
    
    generateInnoSetupFile()
    parameters = './iscc.sh windows/microide.iss'
    os.system(parameters  + " >> output.log")





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--onlyDownload', nargs='?', type=bool, const=True, help='Checking if all windows and linux files can be download from internet.')
    parser.add_argument('--verifyWindowsDownload', nargs='?', type=bool, const=True, help='Checking if all files required for windows installation can be download from internet.')
    parser.add_argument('--verifyLinuxDownload', nargs='?', type=bool, const=True, help='Checking if all files required for linux installation can be download from internet.')
    parser.add_argument('--replaceGthr', nargs='?', type=bool, const=True, help='Part of toolchain patching, replacing gthr.h file into microhal version.')
    parser.add_argument('--createToolchainPatch', nargs='?', type=bool, const=True, help='Create toolchain patch.')
    parser.add_argument('--makeLinuxInstaller', nargs='?', type=bool, const=True, help='Creating linux installation files.')
    parser.add_argument('--makeWindowsInstaller', nargs='?', type=bool, const=True, help='Creating windows installation files. This will work on linux with wine where Inno Setup and Inno Download Plugin was installed')

    args = parser.parse_args()

    if args.onlyDownload == True:
        getFiles('norepo')
    if args.verifyWindowsDownload == True:
        verifyWindowsDownloads('norepo')
    if args.verifyLinuxDownload == True:
        verifyLinuxDownloads('norepo')
    if args.makeLinuxInstaller == True:
        print "Generating instalation files..."
        getMissingFiles('norepo/linux', linuxFiles)
        updateFileinfo('norepo/linux', linuxFiles)
        generateLinuxProductSetup()
        generateLinuxInstaller()
    if args.makeWindowsInstaller == True:
        print "Generating windows instalation files..."
        getMissingFiles('norepo/windows', windowsFiles)
        updateFileinfo('norepo/windows', windowsFiles)        
        compileWindowsInstaller()
    if args.replaceGthr == True:
        print "Replacing gthr.h files..."
        toolchainDir = 'norepo/toolchains/gcc-arm-none-eabi-patch/gcc-arm-none-eabi-6-2017-q2-update'
        replaceRecursive(toolchainDir, 'toolchainPatchFiles', 'gthr.h')
    if args.createToolchainPatch == True:
        os.system("mkdir -p norepo/toolchains/gcc-arm-none-eabi-patch >> output.log")
        copyLocation = "toolchainPatchFiles/gcc-arm-none-eabi-7-2017-q4-major"
        toolchain = armGccToolchain_7_2017_q4
        print "Creating toolchain patch."
        getMissingFiles('norepo/linux', [toolchain])
        print "Extracting toolchain files..."
        os.system("tar --extract --file=" +  'norepo/linux/' + toolchain['filename'] + ' -C norepo/toolchains/gcc-arm-none-eabi-patch')        
        toolchainDir = 'norepo/toolchains/gcc-arm-none-eabi-patch/gcc-arm-none-eabi-7-2017-q4-major'
        print "Create copy of original files"
        #make directory for copies
        os.system("mkdir -p " + copyLocation + " >> output.log")
        #copy gthr.h
        filePath = findFile(toolchainDir, 'gthr.h')
        shutil.copyfile(filePath, copyLocation +'/gthr.h.oryg')
        #copy thread 
        shutil.copyfile(toolchainDir + '/arm-none-eabi/include/c++/7.2.1/thread', copyLocation +'/thread.oryg')
        #copy mutex
        shutil.copyfile(toolchainDir + '/arm-none-eabi/include/c++/7.2.1/mutex', copyLocation +'/mutex.oryg')
        #copy condition_variable
        shutil.copyfile(toolchainDir + '/arm-none-eabi/include/c++/7.2.1/condition_variable', copyLocation +'/condition_variable.oryg')
        print "Replacing gthr.h ..."
        shutil.copyfile(copyLocation +'/gthr.h.oryg', copyLocation + '/gthr.h')
        mergeFiles('toolchainPatchFiles/gthr.h', copyLocation + '/gthr.h')       
        replaceRecursive(toolchainDir, copyLocation, 'gthr.h')
        print "Replacing thread ..."
        mergeFiles('toolchainPatchFiles/thread', toolchainDir + '/arm-none-eabi/include/c++/7.2.1/thread')
        print "Replacing mutex ..."
        mergeFiles('toolchainPatchFiles/mutex', toolchainDir + '/arm-none-eabi/include/c++/7.2.1/mutex')
        print "Replacing condition_variable ..."
        mergeFiles('toolchainPatchFiles/condition_variable', toolchainDir + '/arm-none-eabi/include/c++/7.2.1/condition_variable')
        print "Removing unchanged files"
        recursiveRemoveNotListedFiles(toolchainDir, ['gthr.h', 'condition_variable', 'mutex', 'thread'])
        print "Copying newly created patch to patches directory"
        shutil.copytree('norepo/toolchains/gcc-arm-none-eabi-patch/gcc-arm-none-eabi-7-2017-q4-major', 'toolchains/gcc-arm-none-eabi-patch/gcc-arm-none-eabi-7-2017-q4')
    

if __name__ == "__main__":
    main()



