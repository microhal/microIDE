#!/usr/bin/env python3

import shutil
import os
import files_utils as fs
import packages
import re
from distutils import dir_util
import subprocess

microideVersion = '0.3.4'
gcc_arm_none_eabi = packages.toolchains['gcc-arm-none-eabi']['gcc-arm-none-eabi-7-2018-q2-update']['windows']
clang = packages.toolchains['clang']['6.0.1']['windows']
mingw = packages.toolchains['mingw']['8.1.0']['windows']
openOCD = packages.openOCD['windows']
eclipse = packages.eclipse['windows']
doxygen = packages.doxygen['1.8.14']['windows']
cppcheck = packages.cppcheck['1.84']['windows']
graphviz = packages.graphviz['2.38']['windows']
msys = packages.msys['13']['windows']


def main():
    components_dir = '../norepo/windows/components'
    fs.make_directory_if_not_exist('../norepo/windows/downloads')
    download_files('../norepo/windows/downloads')
    # do some clenup
    shutil.rmtree(components_dir, ignore_errors=True)
    # start creating installers
    extract_files('../norepo/windows/downloads/', components_dir)
    generateWindowsProductSetup()  # generate oomph setup files for windows
    patch_eclipse_installer(components_dir + '/eclipse-installer', '../eclipse-installer/microideLocalSetups/')
    update_files_information()
    generateInnoSetupFile(microideVersion, '../norepo/windows')
    compile_online_installer()
    compile_offline_installer()


def compile_online_installer():
    # do some clenup
    shutil.rmtree('../norepo/windows/toolchainPatch', ignore_errors=True)

    # prepare installer
    download7zipStandaloneConsoleVersion()  # needed to unpack repositories while installing on windows

    # include toolchain patch files into installer, firstly copy patch files into proper directory
    patchDirectoryName = re.sub('-win32(-sha2)?\.(exe|zip)', '',
                                packages.toolchains['gcc-arm-none-eabi']['gcc-arm-none-eabi-7-2018-q2-update'][
                                    'windows']['filename'])
    shutil.copytree('../toolchains/gcc-arm-none-eabi-patch/' + patchDirectoryName,
                    '../norepo/windows/toolchainPatch/' + patchDirectoryName)

    fs.copyfile('inno setup/microide_online.iss', '../norepo/windows/microide_online.iss')
    print("Compiling online installer...")
    subprocess.run(['./inno setup/iscc.sh', '../norepo/windows/microide_online.iss'])
    print("Online installer ready.")


def compile_offline_installer():
    components_dir = '../norepo/windows/components'

    # include toolchain patch files into installer, firstly copy patch files into proper directory
    patchDirectoryName = re.sub('-win32(-sha2)?\.(exe|zip)', '',
                                packages.toolchains['gcc-arm-none-eabi']['gcc-arm-none-eabi-7-2018-q2-update'][
                                    'windows']['filename'])
    dir_util.copy_tree('../toolchains/gcc-arm-none-eabi-patch/' + patchDirectoryName,
                                 components_dir + '/gcc_arm_none_eabi')

    fs.copyfile('inno setup/microide_offline.iss', '../norepo/windows/microide_offline.iss')
    print("Compiling offline installer...")
    subprocess.run(['./inno setup/iscc.sh', '../norepo/windows/microide_offline.iss'])
    print("Offline installer ready.")


def generateWindowsProductSetup():
    with open('../templates/microide.product.setup.template', 'r') as file:
        content = file.read()

    #  gcc_arm_none_eabi = packages.toolchains['gcc-arm-none-eabi']['gcc-arm-none-eabi-7-2018-q2-update']['windows']
    toolchainPatch = gcc_arm_none_eabi['installationLocation'].replace('{app}', 'microideDir') + '/' + re.sub(
        '-.{5,6}-win32\.(exe|zip)', '', gcc_arm_none_eabi['filename'])
    content = content.replace("##microideToolchainPatch##", toolchainPatch.replace('\\', '/'))

    #    clang = packages.toolchains['clang']['6.0.1']['windows']
    clangPath = clang['installationLocation']
    clangPath = clangPath.replace('{app}', '${microideDir') + '/bin|file}'
    clangFormatLocation = clangPath + '/clang-format.exe'
    content = content.replace("##clangFormatLocation##", clangFormatLocation.replace('\\', '/'))
    content = content.replace("##clangToolchainPatch##", clangPath.replace('\\', '/'))

    #   mingw = packages.toolchains['mingw']['8.1.0']['windows']
    mingwPath = mingw['installationLocation'] + '\\' + mingw['version']
    mingwPath = mingwPath.replace('{app}', '${microideDir') + '|file}'
    content = content.replace("##MinGWToolchainPatch##", mingwPath.replace('\\', '/'))

    #   doxygen = packages.doxygen['1.8.14']['windows']
    doxygenPath = doxygen['installationLocation']
    doxygenPath = doxygenPath.replace('{app}', '${microideDir|file}')
    content = content.replace("##DoxygenPatch##", doxygenPath.replace('\\', '/'))

    with open('../eclipse-installer/microideLocalSetups/microide.product.setup.windows', 'w') as file:
        file.write(content)


def generateInnoSetupFile(microide_version, destination):
    with open(destination + '/microide_components.iss', 'w') as file:
        file.write('#define AppVersion "' + microide_version + '"\n\n')
        file.write('#define ARM_GCC_TOOLCHAIN_URL "' + gcc_arm_none_eabi['url'] + '"\n')
        file.write('#define ARM_GCC_TOOLCHAIN_LICENSE_URL "' + gcc_arm_none_eabi['licenseUrl'] + '"\n')
        file.write('#define ARM_GCC_TOOLCHAIN_FILENAME "' + gcc_arm_none_eabi['filename'] + '"\n')
        file.write('#define ARM_GCC_TOOLCHAIN_VERSION "' + gcc_arm_none_eabi['version'] + '"\n')
        file.write('#define ARM_GCC_TOOLCHAIN_SIZE ' + str(gcc_arm_none_eabi['installation size']) + '\n')
        file.write('#define ARM_GCC_TOOLCHAIN_LOCATION "' + gcc_arm_none_eabi['installationLocation'] + '\\' + re.sub(
            '-win32(-sha2)?\.(exe|zip)', '', gcc_arm_none_eabi['filename']) + '"\n')
        file.write('#define ARM_GCC_TOOLCHAIN_CHECKSUM_MD5 "' + gcc_arm_none_eabi['checksum']['md5'] + '"\n')
        file.write('\n')

        file.write('#define CLANG_TOOLCHAIN_URL "' + clang['url'] + '"\n')
        file.write('#define CLANG_TOOLCHAIN_FILENAME "' + clang['filename'] + '"\n')
        file.write('#define CLANG_TOOLCHAIN_VERSION "' + clang['version'] + '"\n')
        file.write('#define CLANG_TOOLCHAIN_SIZE ' + str(clang['installation size']) + '\n')
        file.write('#define CLANG_TOOLCHAIN_LOCATION "' + clang['installationLocation'] + '"\n')
        file.write('#define ClANG_TOOLCHAIN_CHECKSUM_MD5 "' + clang['checksum']['md5'] + '"\n')
        file.write('\n')
        #  openOCD
        file.write('#define OPENOCD_URL "' + openOCD['url'] + '"\n')
        file.write('#define OPENOCD_FILENAME "' + openOCD['filename'] + '"\n')
        file.write('#define OPENOCD_VERSION "' + openOCD['version'] + '"\n')
        file.write('#define OPENOCD_SIZE ' + str(openOCD['installation size']) + '\n')
        file.write('#define OPENOCD_LOCATION "' + openOCD['installationLocation'] + '"\n')
        file.write('#define OPENOCD_CHECKSUM_MD5 "' + openOCD['checksum']['md5'] + '"\n')
        file.write('\n')
        # doxygen
        file.write('#define DOXYGEN_URL "' + doxygen['url'] + '"\n')
        file.write('#define DOXYGEN_LICENSE_URL "' + doxygen['licenseUrl'] + '"\n')
        file.write('#define DOXYGEN_FILENAME "' + doxygen['filename'] + '"\n')
        file.write('#define DOXYGEN_VERSION "' + doxygen['version'] + '"\n')
        file.write('#define DOXYGEN_SIZE ' + str(doxygen['installation size']) + '\n')
        file.write('#define DOXYGEN_LOCATION "' + doxygen['installationLocation'] + '"\n')
        file.write('#define DOXYGEN_CHECKSUM_MD5 "' + doxygen['checksum']['md5'] + '"\n')
        file.write('\n')
        #  mingw
        file.write('#define MINGW_URL "' + mingw['url'] + '"\n')
        file.write('#define MINGW_LICENSE_URL "' + mingw['licenseUrl'] + '"\n')
        file.write('#define MINGW_FILENAME "' + mingw['filename'] + '"\n')
        file.write('#define MINGW_VERSION "' + mingw['version'] + '"\n')
        file.write('#define MINGW_SIZE ' + str(mingw['installation size']) + '\n')
        file.write('#define MINGW_LOCATION "' + mingw['installationLocation'] + '"\n')
        file.write('#define MINGW_CHECKSUM_MD5 "' + mingw['checksum']['md5'] + '"\n')
        file.write('\n')
        # cppcheck
        file.write('#define CPPCHECK_URL "' + cppcheck['url'] + '"\n')
        file.write('#define CPPCHECK_LICENSE_URL "' + cppcheck['licenseUrl'] + '"\n')
        file.write('#define CPPCHECK_FILENAME "' + cppcheck['filename'] + '"\n')
        file.write('#define CPPCHECK_VERSION "' + cppcheck['version'] + '"\n')
        file.write('#define CPPCHECK_SIZE ' + str(cppcheck['installation size']) + '\n')
        file.write('#define CPPCHECK_LOCATION "' + cppcheck['installationLocation'] + '"\n')
        file.write('#define CPPCHECK_CHECKSUM_MD5 "' + cppcheck['checksum']['md5'] + '"\n')
        file.write('\n')
        # graphviz
        file.write('#define GRAPHVIZ_URL "' + graphviz['url'] + '"\n')
        file.write('#define GRAPHVIZ_LICENSE_URL "' + graphviz['licenseUrl'] + '"\n')
        file.write('#define GRAPHVIZ_FILENAME "' + graphviz['filename'] + '"\n')
        file.write('#define GRAPHVIZ_VERSION "' + graphviz['version'] + '"\n')
        file.write('#define GRAPHVIZ_SIZE ' + str(graphviz['installation size']) + '\n')
        file.write('#define GRAPHVIZ_LOCATION "' + graphviz['installationLocation'] + '"\n')
        file.write('#define GRAPHVIZ_CHECKSUM_MD5 "' + graphviz['checksum']['md5'] + '"\n')
        file.write('\n')


def download7zipStandaloneConsoleVersion():
    filename = '7z1604-extra.7z'
    dest = '../norepo/windows'
    fs.download(dest, filename, 'http://www.7-zip.org/a/7z1604-extra.7z', {})

    os.system("mkdir -p ../norepo/windows/tools/7z1604-extra >> output.log")
    parameters = '7za x ' + dest + '/' + filename + ' -y -o../norepo/windows/tools/7z1604-extra'
    os.system(parameters + " >> output.log")


def extract_eclipse_files(source, destination):
    command = 'unzip -q ' + source + ' -d ' + destination
    os.system(command)
    os.remove(destination + '/extractor.exe')


def patch_eclipse_installer(location, oomph_file_location):
    with open(location + '/eclipse-inst.ini', 'a') as iniFile:
        iniFile.write(
            '-Doomph.redirection.myProjectsCatalog=index:/redirectable.projects.setup->https://raw.githubusercontent.com/microHAL/microIDE/devel/eclipse-installer/microideSetups/microhal.projects.setup\n')
        iniFile.write('-Doomph.setup.product.catalog.filter=microide')
    # copying oomph setup files
    fs.make_directory_if_not_exist(location + '/microideLocalSetups')
    fs.copyfile(oomph_file_location + '/microide.product.setup.windows',
                location + '/microideLocalSetups/microide.product.setup')


def install_missing_packages():
    pass


def download_files(destination):
    print("Generating windows instalation files...")
    fs.getMissingFiles(destination,
                       [gcc_arm_none_eabi, clang, mingw, openOCD, eclipse, doxygen, cppcheck, graphviz, msys])


def extract_files(download_dir, destination):
    print("Extracting windows instalation files...")
    fs.make_directory_if_not_exist(destination)
    # do some clenup
    shutil.rmtree(destination, ignore_errors=True)

    fs.extract(download_dir + cppcheck['filename'], destination + '/cppcheck')
    fs.extract(download_dir + doxygen['filename'], destination + '/doxygen')
    extract_eclipse_files(download_dir + eclipse['filename'], destination + '/eclipse-installer')
    fs.extract(download_dir + gcc_arm_none_eabi['filename'], destination + '/gcc_arm_none_eabi')
    fs.extract(download_dir + graphviz['filename'], destination + '/graphviz')
    fs.extract(download_dir + clang['filename'], destination + '/clang')
    fs.extract(download_dir + msys['filename'], destination + '/msys')
    fs.extract(download_dir + openOCD['filename'], destination + '/openocd')
    fs.extract(download_dir + mingw['filename'], destination + '/mingw')


def update_files_information():
    clang['installation size'] = fs.get_directory_size('../norepo/windows/components/clang')
    doxygen['installation size'] = fs.get_directory_size('../norepo/windows/components/doxygen')
    eclipse['installation size'] = fs.get_directory_size('../norepo/windows/components/eclipse-installer')
    gcc_arm_none_eabi['installation size'] = fs.get_directory_size('../norepo/windows/components/gcc_arm_none_eabi')
    graphviz['installation size'] = fs.get_directory_size('../norepo/windows/components/graphviz')
    mingw['installation size'] = fs.get_directory_size('../norepo/windows/components/mingw')
    msys['installation size'] = fs.get_directory_size('../norepo/windows/components/msys')
    openOCD['installation size'] = fs.get_directory_size('../norepo/windows/components/openocd')

    fs.updateFileinfo('../norepo/windows/openocd', [openOCD])
    fs.updateFileinfo('../norepo/windows/eclipse', [eclipse])
    fs.updateFileinfo('../norepo/windows/doxygen', [doxygen])
    fs.updateFileinfo('../norepo/windows/cppcheck', [cppcheck])
    fs.updateFileinfo('../norepo/windows/toolchains', [clang])
    fs.updateFileinfo('../norepo/windows/graphviz', [graphviz])
    fs.updateFileinfo('../norepo/windows/msys', [msys])


if __name__ == "__main__":
    main()
