import os
import hashlib
import shutil


def get_file_extension(file):
    filename, extension = os.path.splitext(file)
    return extension


def make_directory_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def copyfile(source, destination):
    shutil.copyfile(source, destination)


def untar(source, destination):
    os.system("tar --extract --file=" + source + ' -C ' + destination)


def extract(source, destination, fource_7za = False):
    if get_file_extension(source) == '.exe' and fource_7za is False:
        os.system("file-roller --force -e " + destination + ' ' + source)
    else:
        os.system("7za x " + source + ' -o' + destination + ' -y')


def validate_checksum(filename, checksum):
    if 'md5' in checksum:
        if hashlib.md5(open(filename, 'rb').read()).hexdigest() != checksum['md5']:
            return [False, 0]
    if 'SHA512' in checksum:
        if hashlib.sha512(open(filename, 'rb').read()).hexdigest() != checksum['SHA512']:
            return [False, 0]
    if 'SHA256' in checksum:
        if hashlib.sha256(open(filename, 'rb').read()).hexdigest() != checksum['SHA256']:
            return [False, 0]
    return True


def download(destynation, filename, url, checksum):
    print('Downloading : ' + filename)
    if destynation:
        destynation = destynation + "/"

    parameters = "wget -O ./" + destynation + filename + ' ' + url
    os.system(parameters + " >> output.log 2>> output.err")
    checksum_status = validate_checksum('./' + destynation + filename, checksum)
    return [checksum_status, os.stat('./' + destynation + filename).st_size]


def get_directory_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def fileExists(path):
    try:
        st = os.stat(path)
    except os.error:
        return False
    return True


def updateFileinfo(destdir, files):
    if destdir:
        destdir = destdir + "/"

    for file in files:
        filePath = destdir + file['filename']
        if fileExists(filePath):
            file['size'] = os.stat(filePath).st_size
            if 'md5' not in file['checksum']:
                file['checksum']['md5'] = hashlib.md5(open(filePath, 'rb').read()).hexdigest()
        else:
            print("An error occurred, while updating file info: " + filePath)
            exit(-1)


def getMissingFiles(destdir, files):
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    if destdir:
        destdir = destdir + "/"

    for file in files:
        filePath = destdir + file['filename']
        if fileExists(filePath) == False:
            download(destdir, file['filename'], file['url'], file['checksum'])
        else:
            print("File exist, no need to download: " + filePath)
