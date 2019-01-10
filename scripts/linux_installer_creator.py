import packages
import re
import files_utils

# oomph repository: https://git.eclipse.org/r/oomph/org.eclipse.oomph.git

microideVersion = '0.3.5'
gcc_arm_none_eabi = packages.toolchains['gcc-arm-none-eabi']['gcc-arm-none-eabi-8-2018-q4-major']['linux']
gcc_arm_linux_gnueabihf = packages.toolchains['gcc-arm-linux-gnueabihf']['gcc-linaro-7.3.1-2018.05-arm-linux-gnueabihf']['linux']
openOCD = packages.openOCD['linux']
eclipse = packages.eclipse['linux']


def generate_linux_product_setup():
    with open('../templates/microide.product.setup.template', 'r') as file:
        content = file.read()
    toolchain_patch = gcc_arm_none_eabi['installationLocation'] + '/' + re.sub('-linux\.tar\.bz2', '',
                                                                               gcc_arm_none_eabi['filename'])
    content = content.replace("##microideToolchainPatch##", toolchain_patch)

    content = content.replace("##clangFormatLocation##", "${binaryDir/clang-format-6.0|file}")
    content = content.replace("##clangToolchainPatch##", "${binaryDir|file}")

    content = content.replace("##DoxygenPatch##", "${binaryDir|file}")

    with open('../eclipse-installer/microideLocalSetups/microide.product.setup.linux', 'w') as file:
        file.write(content)


def generate_linux_installer():
    with open('../templates/microide_install.template', 'r') as file:
        content = file.read()
    text = 'VERSION=' + microideVersion + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_URL=' + gcc_arm_none_eabi['url'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_LICENSE_URL=' + gcc_arm_none_eabi['licenseUrl'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_FILENAME=' + gcc_arm_none_eabi['filename'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_VERSION=' + gcc_arm_none_eabi['version'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_SIZE=' + str(gcc_arm_none_eabi['size']) + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_CHECKSUM=' + gcc_arm_none_eabi['checksum']['md5'] + '\n'
    text = text + 'ARM_GCC_TOOLCHAIN_LOCATION=' + gcc_arm_none_eabi['installationLocation'].replace('microideDir/', '')
    text = text + '\n\nGCC_ARM_LINUX_GNUEABIHF_TOOLCHAIN_URL=' + gcc_arm_linux_gnueabihf['url'] + '\n'
    text = text + 'GCC_ARM_LINUX_GNUEABIHF_LICENSE_URL=' + gcc_arm_linux_gnueabihf['licenseUrl'] + '\n'
    text = text + 'GCC_ARM_LINUX_GNUEABIHF_FILENAME=' + gcc_arm_linux_gnueabihf['filename'] + '\n'
    text = text + 'GCC_ARM_LINUX_GNUEABIHF_VERSION=' + gcc_arm_linux_gnueabihf['version'] + '\n'
    text = text + 'GCC_ARM_LINUX_GNUEABIHF_SIZE=' + str(gcc_arm_linux_gnueabihf['size']) + '\n'
    text = text + 'GCC_ARM_LINUX_GNUEABIHF_CHECKSUM=' + gcc_arm_linux_gnueabihf['checksum']['md5'] + '\n'
    text = text + 'GCC_ARM_LINUX_GNUEABIHF_LOCATION=' + gcc_arm_linux_gnueabihf['installationLocation'].replace('microideDir/', '')
    text = text + '\n\nOPENOCD_URL=' + openOCD['url']
    text = text + '\nOPENOCD_FILENAME=' + openOCD['filename']
    text = text + '\nOPENOCD_VERSION=' + openOCD['version']
    text = text + '\nOPENOCD_SIZE=' + str(openOCD['size'])
    text = text + '\nOPENOCD_CHECKSUM=' + openOCD['checksum']['md5']
    text = text + '\nOPENOCD_LOCATION=' + openOCD['installationLocation']
    text = text + '\n\nECLIPSE_URL=' + eclipse['url'] + '\nECLIPSE_FILENAME=' + eclipse[
        'filename'] + '\nECLIPSE_VERSION=' + eclipse['version'] + '\nECLIPSE_SIZE=' + str(
        eclipse['size']) + '\nECLIPSE_CHECKSUM=' + eclipse['checksum']['md5'] + '\nECLIPSE_LOCATION=' + eclipse[
               'installationLocation']

    content = content.replace("#replace this text with instalation files information", text)

    with open('../linux/microide_install_linux.sh', 'w') as file:
        file.write(content)


def main():
    files_utils.make_directory_if_not_exist('../norepo/linux/toolchains')
    files_utils.make_directory_if_not_exist('../norepo/linux/openocd')
    files_utils.make_directory_if_not_exist('../norepo/linux/eclipse')

    print("Generating instalation files...")
    files_utils.getMissingFiles('../norepo/linux/toolchains', [gcc_arm_none_eabi, gcc_arm_linux_gnueabihf])
    files_utils.getMissingFiles('../norepo/linux/openocd', [openOCD])
    files_utils.getMissingFiles('../norepo/linux/eclipse', [eclipse])
    files_utils.updateFileinfo('../norepo/linux/toolchains', [gcc_arm_none_eabi, gcc_arm_linux_gnueabihf])
    files_utils.updateFileinfo('../norepo/linux/openocd', [openOCD])
    files_utils.updateFileinfo('../norepo/linux/eclipse', [eclipse])

    generate_linux_product_setup()
    generate_linux_installer()


if __name__ == "__main__":
    main()
