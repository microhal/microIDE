import os
import shutil
import subprocess
import files_utils as filesystem
import packages


# this function will return path to first file with name passed as a parameter
def findFile(directory, filename):
    for root, subdirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, filename)
            #        print('\t- file %s (full path: %s)' % (filename, file_path))
            if file == filename:
                return file_path
    return ''


def replaceRecursive(destination, sourcefiledir, sourcefilename):
    replaceCounter = 0
    for root, subdirs, files in os.walk(destination):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename == sourcefilename:
                shutil.copy(sourcefiledir + "/" + sourcefilename, file_path)
                replaceCounter = replaceCounter + 1
    print("Replaced " + str(replaceCounter) + " files")


def recursiveRemoveNotListedFiles(directory, filesToPath):
    for root, subdirs, files in os.walk(directory, topdown=False):
        for filename in files:
            file_path = os.path.join(root, filename)
            #        print('\t- file %s (full path: %s)' % (filename, file_path))
            if filename not in filesToPath:
                os.remove(file_path)

        for subdir in subdirs:
            # print('\t- subdirectory ' + subdir)
            if os.path.isdir(subdir):
                if not os.listdir(subdir):
                    os.rmdir(subdir)

        if not os.listdir(root):
            os.rmdir(root)


def manual_merge(from_previous_patch, current_file, oryginal_file):
    subprocess.check_call(["meld", from_previous_patch, current_file, oryginal_file])


def download_toolchain_if_needed(toolchain, download_dir):
    filesystem.make_directory_if_not_exist(download_dir)
    filesystem.getMissingFiles(download_dir, [toolchain])


def extract_toolchain(source, destynation):
    print("Extracting toolchain files...")
    filesystem.make_directory_if_not_exist(destynation)
    filesystem.untar(source, destynation)


def copy_files_to_tmp_patch_location(toolchain_unpack_dir, tmp_patch_dir):
    print("Create copy of original files")
    # make directory for copies
    filesystem.make_directory_if_not_exist(tmp_patch_dir)
    # copy gthr.h
    file_path = findFile(toolchain_unpack_dir, 'gthr.h')
    filesystem.copyfile(file_path, tmp_patch_dir + '/gthr.h.oryg')
    filesystem.copyfile(file_path, tmp_patch_dir + '/gthr.h')
    # copy thread
    file_path = findFile(toolchain_unpack_dir, 'thread')
    filesystem.copyfile(file_path, tmp_patch_dir + '/thread.oryg')
    filesystem.copyfile(file_path, tmp_patch_dir + '/thread')
    # copy mutex
    file_path = findFile(toolchain_unpack_dir, 'mutex')
    filesystem.copyfile(file_path, tmp_patch_dir + '/mutex.oryg')
    filesystem.copyfile(file_path, tmp_patch_dir + '/mutex')
    # copy condition_variable
    file_path = findFile(toolchain_unpack_dir, 'condition_variable')
    filesystem.copyfile(file_path, tmp_patch_dir + '/condition_variable.oryg')
    filesystem.copyfile(file_path, tmp_patch_dir + '/condition_variable')


def copy_files_from_last_patch(last_patch_location, tmp_patch_dir):
    print("Create copy of files from previous patch.")
    # make directory for copies
    filesystem.make_directory_if_not_exist(tmp_patch_dir)
    # copy gthr.h
    file_path = findFile(last_patch_location, 'gthr.h')
    filesystem.copyfile(file_path, tmp_patch_dir + '/gthr.h.old')
    # copy thread
    file_path = findFile(last_patch_location, 'thread')
    filesystem.copyfile(file_path, tmp_patch_dir + '/thread.old')
    # copy mutex
    file_path = findFile(last_patch_location, 'mutex')
    filesystem.copyfile(file_path, tmp_patch_dir + '/mutex.old')
    # copy condition_variable
    file_path = findFile(last_patch_location, 'condition_variable')
    filesystem.copyfile(file_path, tmp_patch_dir + '/condition_variable.old')


def main():
    last_patch_location = '../toolchains/gcc-arm-none-eabi-patch/gcc-arm-none-eabi-7-2017-q4'
    toolchain_version = 'gcc-arm-none-eabi-7-2018-q2-update'
    toolchain = packages.toolchains['gcc-arm-none-eabi'][toolchain_version]['linux']

    toolchain_download_dir = '../norepo/linux/toolchain'
    toolchain_unpack_dir = '../norepo/toolchain'
 
    print("Creating toolchain patch.")
    download_toolchain_if_needed(toolchain, toolchain_download_dir)
    extract_toolchain(toolchain_download_dir + '/' + toolchain['filename'], toolchain_unpack_dir)

    tmp_patch_dir = '../norepo/tmp_gcc-arm-none-eabi-patch'
    copy_files_to_tmp_patch_location(toolchain_unpack_dir, tmp_patch_dir)
    copy_files_from_last_patch(last_patch_location, tmp_patch_dir)

    print("Merging gthr.h ...")
    manual_merge(tmp_patch_dir + '/gthr.h.old', tmp_patch_dir + '/gthr.h', tmp_patch_dir + '/gthr.h.oryg')
    print("Merging thread ...")
    manual_merge(tmp_patch_dir + '/thread.old', tmp_patch_dir + '/thread', tmp_patch_dir + '/thread.oryg')
    print("Merging mutex ...")
    manual_merge(tmp_patch_dir + '/mutex.old', tmp_patch_dir + '/mutex', tmp_patch_dir + '/mutex.oryg')
    print("Merging mutex ...")
    manual_merge(tmp_patch_dir + '/condition_variable.old', tmp_patch_dir + '/condition_variable',
                 tmp_patch_dir + '/condition_variable.oryg')

    replaceRecursive(toolchain_unpack_dir, tmp_patch_dir, 'gthr.h')
    replaceRecursive(toolchain_unpack_dir, tmp_patch_dir, 'thread')
    replaceRecursive(toolchain_unpack_dir, tmp_patch_dir, 'mutex')
    replaceRecursive(toolchain_unpack_dir, tmp_patch_dir, 'condition_variable')

    print("Removing unchanged files")
    recursiveRemoveNotListedFiles(toolchain_unpack_dir, ['gthr.h', 'condition_variable', 'mutex', 'thread'])
    print("Copying newly created patch to patches directory")
    shutil.copytree(toolchain_unpack_dir,
                    '../toolchains/gcc-arm-none-eabi-patch/' + toolchain_version)


if __name__ == "__main__":
    main()
