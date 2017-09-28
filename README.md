## Microide is eclipse based IDE dedicated for embedded development. 

### Windows
To install microide on Windows operating system you should go to our Source Forge project site and download windows binary installer.

[![Download microHAL](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/microhal/files/latest/download)
### Linux
To install microide on Linux operating system download <b>linux/microide_install.sh</b> file from this repository and run it in directory where you want to install microide.

## Importing microhal examples
Microhal is integrated with microide, to import microhal examples you should follow importing tutorial on our website:
http://microhal.org/quickstartguide

### About microide
Microide is dedicated for embedded development, its integrate tools like:
 - Eclipse CDT for C/C++ development
 - ARM Toolchain
 - Mingw Toolchain
 - Clang Toolchain
 - OpenOCD Debbuger
 - Doxygen for generate documentation from code
 - Graphiz is component required by Doxygen
 - GNU MCU Eclipse plugin that can integrate eclipse with OpenOCD and ARM Toolchain
 
All packages are preconfigured and IDE is redy for use after installing. This installer contain script that will download and install all comptonents.

### Changelog

#### 0.3.1
- updated Eclipse to newest version (oxygen)
- updated OpenOCD to 0.10.0 Release 
- replaced GNU ARM Eclipse plugin with GNU MCU Eclipse
- updated MinGW-w64 to 7.1.0
