#!/usr/bin/env python

import os
import hashlib
import shutil
import re
import argparse

#armGccToolchain = {
#    'filename' : 'gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2',
#    'size' : '0',
#    'version' : '6-2017-q2',
#    'url' : 'https://developer.arm.com/-/media/Files/downloads/gnu-rm/6-2017q2/gcc-arm-none-eabi-6-2017-q2-update-linux.tar.bz2?product=GNU%20ARM%20Embedded%20Toolchain,64-bit,,Linux,6-2017-q2-update', 
#    'checksum' : {'md5' : '13747255194398ee08b3ba42e40e9465'},
#    'licenseUrl' : 'https://developer.arm.com/GetEula?Id=2d916619-954e-4adb-895d-b1ec657ae305',
#    'installationLocation' : 'toolchains/gcc-arm-none-eabi/microhal'
#}

armGccToolchain = {
    'filename' : 'gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2',
    'size' : '0',
    'version' : '5.3.0',
    'url' : 'https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2', 
    'checksum' : {'md5' : '5a261cac18c62d8b7e8c70beba2004bd'},
    'licenseUrl' : 'https://launchpadlibrarian.net/251686212/license.txt',
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

# ------------------------------------- windows version
winArmGccToolchain = {
    'filename' : 'gcc-arm-none-eabi-5_3-2016q1-20160330-win32.exe',
    'size' : '0',
    'version' : '5.3.0',
    'url' : 'https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-win32.exe', 
    'checksum' : {'md5' : ''},
    'licenseUrl' : 'https://launchpadlibrarian.net/251686212/license.txt',
    'installationLocation' : '{app}\\toolchains\\gcc-arm-none-eabi\\microhal\\gcc-arm-none-eabi-5_3-2016q1'
}

winClangToolchain = {
    'filename' : 'LLVM-3.8.0-win64.exe',
    'size' : '0',
    'version' : '3.8.0',
    'url' : 'http://llvm.org/releases/3.8.0/LLVM-3.8.0-win64.exe', 
    'checksum' : {'md5' : ''},
    'licenseUrl' : 'https://launchpadlibrarian.net/251686212/license.txt',
    'installationLocation' : '{app}\\toolchains\\LLVM\\3.8.0'
}

winOpenOCD = {
    'filename' : 'openocd-0.10.0.7z',
    'size' : '0',
    'version' : '0.10.0',
    'url' : 'http://www.freddiechopin.info/en/download/category/4-openocd?download=154%3Aopenocd-0.10.0',             
    'checksum' : {'SHA256' : 'f46687cd783a7a86716c78474e8132e32de84b773914f23f2226f81509ffcfca'},
    'installationLocation' : "{app}\\tools\\openocd\\0.10.0"
}

winEclipse = {
    'filename' : 'eclipse-inst-win64.exe',
    'size' : '0',
    'version' : 'oxygen',
    'url' : 'https://www.eclipse.org/downloads/download.php?file=/oomph/epp/oxygen/R/eclipse-inst-win64.exe\&r=1',
    'checksum' : {'SHA512' : 'c585b52bf9da53812a14c9cbf48fa6beb0af983f52aa45e589c7e9cc4edce2a1819ebc87ccb4cd39104515a6d4e6adc6a4d2681d9744a041e9f0883d995349ea'},
    'installationLocation' : 'eclipse'
}

# ------------------------------------ end of file declaration

def download(filename, url, checksum):
	parameters = "wget -O ./" + filename + ' ' + url
	os.system(parameters  + " >> output.log")
	if checksum.has_key('md5') == True:
		if hashlib.md5(open('./' + filename,'rb').read()).hexdigest() != checksum['md5']:
			return [False, 0]
	if checksum.has_key('SHA512') == True:
		if hashlib.sha512(open('./' + filename,'rb').read()).hexdigest() != checksum['SHA512']:
			return [False, 0]
	if checksum.has_key('SHA256') == True:
		if hashlib.sha256(open('./' + filename,'rb').read()).hexdigest() != checksum['SHA256']:
			return [False, 0]

        return [True, os.stat('./' + filename).st_size]
	

def generateLinuxProductSetup():
	with open('templates/microide.product.setup.linux.template', 'r') as file:
		content = file.read()
	toolchainPatch = armGccToolchain['installationLocation'] + '/' + re.sub('-\d{8}-linux.tar.bz2', '', armGccToolchain['filename'])
	content = content.replace("##microideToolchainPatch##", toolchainPatch)

	with open('eclipse-installer/setups/microIDE/microide.product.setup.linux', 'w') as file:
		file.write(content)

def generateLinuxInstaller():
	with open('templates/microide.iss.template', 'r') as file:
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


def getFiles():
	status = [False, False]
	status = download(armGccToolchain['filename'], armGccToolchain['url'], armGccToolchain['checksum'])
	if status[0] == True:
		armGccToolchain['size'] = status[1]
		if armGccToolchain['checksum'].has_key('md5') == False:
			armGccToolchain['checksum']['md5'] = hashlib.md5(open('./' + armGccToolchain['filename'],'rb').read()).hexdigest()	
	else:
		print "An error occurred"
		exit(-1) 

	status = download(openOCD['filename'], openOCD['url'], openOCD['checksum'])
	if status[0] == True:
		openOCD['size'] = status[1]
		if openOCD['checksum'].has_key('md5') == False:
			openOCD['checksum']['md5'] = hashlib.md5(open('./' + openOCD['filename'],'rb').read()).hexdigest()	
	else:
		print "An error occurred"
		exit(-1) 


	status = download(eclipse['filename'], eclipse['url'], eclipse['checksum'])
	if status[0] == True:
		eclipse['size'] = status[1]
		if eclipse['checksum'].has_key('md5') == False:
			eclipse['checksum']['md5'] = hashlib.md5(open('./' + eclipse['filename'], 'rb').read()).hexdigest()	
	else:
		print "An error occurred"
		exit(-1) 

def generateInnoSetupFile():
	with open('templates/microide.iss.template', 'r') as file:
		content = file.read()

	text = '#define ARM_GCC_TOOLCHAIN_URL "' + winArmGccToolchain['url'] + '"\n'
	text = text + '#define ARM_GCC_TOOLCHAIN_LICENSE_URL "' + winArmGccToolchain['licenseUrl'] + '"\n'
	text = text + '#define ARM_GCC_TOOLCHAIN_FILENAME "' + winArmGccToolchain['filename'] + '"\n'
	text = text + '#define ARM_GCC_TOOLCHAIN_VERSION "' + winArmGccToolchain['version'] + '"\n'
	text = text + '#define ARM_GCC_TOOLCHAIN_SIZE ' + str(winArmGccToolchain['size']) + '\n'
	text = text + '#define ARM_GCC_TOOLCHAIN_LOCATION "' + winArmGccToolchain['installationLocation'] + '"\n'

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

	content = content.replace("#replace this text with instalation files information", text)

	with open('windows/microide.iss', 'w') as file:
		file.write(content)

def download7zipStandaloneConsoleVersion():
	filename = '7z1604-extra.7z'
	download(filename, 'http://www.7-zip.org/a/7z1604-extra.7z', {})

	os.system("mkdir -p windows/tools/7z1604-extra >> output.log")
	parameters = '7za x ' + filename + ' -y -owindows/tools/7z1604-extra'
	os.system(parameters + " >> output.log")

def compileWindowsInstaller():
	parameters = './iscc.sh windows/microide.iss'
	os.system(parameters  + " >> output.log")



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--onlyDownload', nargs='?', type=bool, const=True, help='Checking if all files can be download from internet.')
	parser.add_argument('--replaceGthr', nargs='?', type=bool, const=True, help='Part of toolchain patching, replacing gthr.h file into microhal version.')
	parser.add_argument('--makeLinuxInstaller', nargs='?', type=bool, const=True, help='Creating windows installation files.')
	parser.add_argument('--makeWindowsInstaller', nargs='?', type=bool, const=True, help='Creating windows installation files. This will work on linux with wine where Inno Setup and Inno Download Plugin was installed')
	args = parser.parse_args()

	if args.onlyDownload == True:
		getFiles()
	if args.makeLinuxInstaller == True:
		print "Generating instalation files..."		
		getFiles()
		generateLinuxProductSetup()
		generateLinuxInstaller()
	if args.replaceGthr == True:
		print "Replacing gthr.h files..."
		replaceGthr()
	if args.makeWindowsInstaller == True:
		print "Generating windows instalation files..."
		generateInnoSetupFile()
		download7zipStandaloneConsoleVersion()
		download(winEclipse['filename'], winEclipse['url'], winEclipse['checksum'])
		#extracting files
		command = '7za x ' + winEclipse['filename'] + ' -y -owindows/eclipse-installer'
		os.system(command)
		with open('windows/eclipse-installer/eclipse-inst.ini', 'a') as iniFile:
			iniFile.write('-Doomph.redirection.setups=http://git.eclipse.org/c/oomph/org.eclipse.oomph.git/plain/setups/->setups/')
		compileWindowsInstaller()

	

if __name__ == "__main__":
    main()



