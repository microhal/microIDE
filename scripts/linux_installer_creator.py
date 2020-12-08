import packages
import re
import files_utils

# oomph repository: https://git.eclipse.org/r/oomph/org.eclipse.oomph.git

microideVersion = '0.3.7'
gcc_arm_none_eabi = packages.toolchains['gcc-arm-none-eabi']['gcc-arm-none-eabi-9-2020-q2-update']['linux']
gcc_arm_linux_gnueabihf = \
    packages.toolchains['gcc-arm-linux-gnueabihf']['gcc-linaro-7.3.1-2018.05-arm-linux-gnueabihf']['linux']
xtensa_esp32_elf = packages.toolchains['xtensa-esp32-elf']['xtensa-esp32-elf-1.22.0-80-g6c4433a-5.2.0']['linux']
openOCD = packages.openOCD['linux']
eclipse = packages.eclipse['linux']


def generate_linux_product_setup():
    with open('../templates/microide.product.setup.template', 'r') as file:
        content = file.read()
    toolchain_patch = gcc_arm_none_eabi['installationLocation'] + '/' + re.sub('-linux\.tar\.bz2', '',
                                                                               gcc_arm_none_eabi['filename'])
    gcc_arm_linux_gnueabihf_toolchain_patch = gcc_arm_linux_gnueabihf['installationLocation'] + '/' + re.sub(
        '\.tar\.xz', '', gcc_arm_linux_gnueabihf['filename'])

    content = content.replace("##microideToolchainPatch##", toolchain_patch)

    content = content.replace("##gccArmLunuxGnueabihfLatestToolchainPatch##", gcc_arm_linux_gnueabihf_toolchain_patch)

    content = content.replace("##xtensaEsp32ElfLatestToolchainPatch##", gcc_arm_none_eabi['installationLocation'] + '/xtensa-esp32-elf')

    content = content.replace("##clangFormatLocation##", "${binaryDir/clang-format-9|file}")
    content = content.replace("##clangToolchainPatch##", "${binaryDir|file}")

    content = content.replace("##DoxygenPatch##", "${binaryDir|file}")
    content = content.replace('##microideVersion##', microideVersion)

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
    text = text + 'GCC_ARM_LINUX_GNUEABIHF_LOCATION=' + gcc_arm_linux_gnueabihf['installationLocation'].replace(
        'microideDir/', '')

    text = text + '\n\nXTENSA_ESP32_ELF_TOOLCHAIN_URL=' + xtensa_esp32_elf['url'] + '\n'
    text = text + 'XTENSA_ESP32_ELF_LICENSE_URL=' + xtensa_esp32_elf['licenseUrl'] + '\n'
    text = text + 'XTENSA_ESP32_ELF_FILENAME=' + xtensa_esp32_elf['filename'] + '\n'
    text = text + 'XTENSA_ESP32_ELF_VERSION=' + xtensa_esp32_elf['version'] + '\n'
    text = text + 'XTENSA_ESP32_ELF_SIZE=' + str(xtensa_esp32_elf['size']) + '\n'
    text = text + 'XTENSA_ESP32_ELF_CHECKSUM=' + xtensa_esp32_elf['checksum']['md5'] + '\n'
    text = text + 'XTENSA_ESP32_ELF_LOCATION=' + xtensa_esp32_elf['installationLocation'].replace(
        'microideDir/', '')

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

    content = content.replace("#replace this text with installation files information", text)

    with open('../linux/microide_install_linux.sh', 'w') as file:
        file.write(content)


def main():
    file_list = [gcc_arm_none_eabi, gcc_arm_linux_gnueabihf, xtensa_esp32_elf, openOCD, eclipse]

    files_utils.make_directory_if_not_exist('../norepo/linux/downloads')
    print("Generating installation files...")
    files_utils.get_missing_or_corrupted_files('../norepo/linux/downloads', file_list)
    files_utils.updateFileinfo('../norepo/linux/downloads', file_list)
    print(file_list)

    generate_linux_product_setup()
    generate_linux_installer()


if __name__ == "__main__":
    main()
