#!/usr/bin/env python

import os
import hashlib
import shutil

armGccToolchain = {
    'filename' : 'gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2',
    'size' : '0',
    'version' : '6-2017-q2',
    'url' : 'https://developer.arm.com/-/media/Files/downloads/gnu-rm/6-2017q2/gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2?product=GNU%20ARM%20Embedded%20Toolchain,64-bit,,Linux,6-2017-q2-update', 
    'checksum' : {'md5' : '13747255194398ee08b3ba42e40e9465'},
    'licenseUrl' : 'https://developer.arm.com/GetEula?Id=2d916619-954e-4adb-895d-b1ec657ae305',
    'installationLocation' : 'toolchains/gcc-arm-none-eabi/microhal'
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
    'url' : 'https://www.eclipse.org/downloads/download.php?file=/oomph/epp/oxygen/R/eclipse-inst-linux64.tar.gz\&r=1',
    'checksum' : {'SHA512' : '2bbb38475b3f3b13b9c6c5db5895fe25ce24b4a8df6a24c6822a348a9652dc8df49ca19152495f34156c39022b8c2ed6b5bb1e84db3edc751302d73bdc1d56da'},
    'installationLocation' : 'eclipse'
}

def download(filename, url, checksum):
	parameters = "wget -O ./" + filename + ' ' + url
	os.system(parameters)
	if checksum.has_key('md5') == True:
		if hashlib.md5(open('./' + filename,'rb').read()).hexdigest() != checksum['md5']:
			return [False, 0]
	if checksum.has_key('SHA512') == True:
		if hashlib.sha512(open('./' + filename,'rb').read()).hexdigest() != checksum['SHA512']:
			return [False, 0]

        return [True, os.stat('./' + filename).st_size]
	

def generateLinuxInstaller():
	with open('linux/microide_install.template', 'r') as file:
		content = file.read()
	text = 'ARM_GCC_TOOLCHAIN_URL=' + armGccToolchain['url'] + '\nARM_GCC_TOOLCHAIN_LICENSE_URL=' + armGccToolchain['licenseUrl'] + '\nARM_GCC_TOOLCHAIN_FILENAME=' + armGccToolchain['filename'] + '\nARM_GCC_TOOLCHAIN_VERSION=' + armGccToolchain['version'] + '\nARM_GCC_TOOLCHAIN_SIZE=' + str(armGccToolchain['size']) + '\nARM_GCC_TOOLCHAIN_CHECKSUM=' + armGccToolchain['checksum']['md5'] + '\nARM_GCC_TOOLCHAIN_LOCATION=' + armGccToolchain['installationLocation']
	text = text + '\n\nOPENOCD_URL=' + openOCD['url'] + '\nOPENOCD_FILENAME=' + openOCD['filename'] + '\nOPENOCD_VERSION=' + openOCD['version'] + '\nOPENOCD_SIZE=' + str(openOCD['size']) + '\nOPENOCD_CHECKSUM=' + openOCD['checksum']['md5'] + '\nOPENOCD_LOCATION=' + openOCD['installationLocation'] 
	text = text + '\n\nECLIPSE_URL=' + eclipse['url'] + '\nECLIPSE_FILENAME=' + eclipse['filename'] + '\nECLIPSE_VERSION=' + eclipse['version'] + '\nECLIPSE_SIZE=' + str(eclipse['size']) + '\nECLIPSE_CHECKSUM=' + eclipse['checksum']['md5'] + '\nECLIPSE_LOCATION=' + eclipse['installationLocation']

	content = content.replace("#replace this text with instalation files information", text)

	with open('linux/microide_install.sh', 'w') as file:
		file.write(content)

def createToolchainPatch():
	os.system("tar --extract --file=" +  armGccToolchain['filename'] +' -C toolchains/gcc-arm-none-eabi-patch')
	for root, subdirs, files in os.walk('toolchains/gcc-arm-none-eabi-patch/gcc-arm-none-eabi-6-2017-q2-update', topdown=False):
		for filename in files:
			file_path = os.path.join(root, filename)
	#		print('\t- file %s (full path: %s)' % (filename, file_path))
			if filename not in ['gthr.h', 'condition_variable', 'mutex', 'thread']:
				os.remove(file_path)

		for subdir in subdirs:
			#print('\t- subdirectory ' + subdir)
			if os.path.isdir(subdir):
				if not os.listdir(subdir):
					os.rmdir(subdir)

		if not os.listdir(root):
			os.rmdir(root)

def replaceGthr():
	for root, subdirs, files in os.walk('toolchains/gcc-arm-none-eabi-patch/gcc-arm-none-eabi-6-2017-q2-update'):
		for filename in files:
			file_path = os.path.join(root, filename)	
			if filename == 'gthr.h':
				shutil.copy('gthr.h', file_path)


#createToolchainPatch()
replaceGthr()

status = [False, False]
#status = download(armGccToolchain['filename'], armGccToolchain['url'], armGccToolchain['checksum'])
if status[0] == True:
	armGccToolchain['size'] = status[1]
	if armGccToolchain['checksum'].has_key('md5') == False:
		armGccToolchain['checksum']['md5'] = hashlib.md5(open('./' + armGccToolchain['filename'],'rb').read()).hexdigest()	
else:
	print "An error occurred"
	exit() 

#status = download(openOCD['filename'], openOCD['url'], openOCD['checksum'])
if status[0] == True:
	openOCD['size'] = status[1]
	if openOCD['checksum'].has_key('md5') == False:
		openOCD['checksum']['md5'] = hashlib.md5(open('./' + openOCD['filename'],'rb').read()).hexdigest()	
else:
	print "An error occurred"
	exit() 


#status = download(eclipse['filename'], eclipse['url'], eclipse['checksum'])
if status[0] == True:
	eclipse['size'] = status[1]
	if eclipse['checksum'].has_key('md5') == False:
		eclipse['checksum']['md5'] = hashlib.md5(open('./' + eclipse['filename'], 'rb').read()).hexdigest()	
else:
	print "An error occurred"
	exit() 

#generateLinuxInstaller()



