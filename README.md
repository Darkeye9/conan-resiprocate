[![Build Status](https://travis-ci.org/uilianries/conan-resiprocate.svg?branch=release/1.10.2)](https://travis-ci.org/uilianries/conan-resiprocate)
[![License: Generous BSD-like](https://img.shields.io/badge/license-Generous%20BSD--like-blue.svg)](https://github.com/resiprocate/resiprocate/blob/master/COPYING)
[![Download](https://api.bintray.com/packages/uilianries/conan/resiprocate%3Auilianries/images/download.svg?version=1.10.2%3Astable)](https://bintray.com/uilianries/conan/resiprocate%3Auilianries/1.10.2%3Astable/link)

# conan-reSIProcate

![Conan reSIProcate](conan-resiprocate.png)

#### C++ implementation of SIP, ICE, TURN and related protocols

[Conan.io](https://conan.io) package for [reSIProcate](https://www.resiprocate.org/) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/uilianries/conan/resiprocate%3Auilianries).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

If your are in Windows you should run it from a VisualStudio console in order to get "mc.exe" in path.

## Upload packages to server

    $ conan upload resiprocate/1.10.2@uilianries/stable --all

## Reuse the packages

### Basic setup

    $ conan install resiprocate/1.10.2@uilianries/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    resiprocate/1.10.2@uilianries/stable

    [options]
    resiprocate:shared=True # False

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

### License
[Generous BSD-like](LICENSE)
