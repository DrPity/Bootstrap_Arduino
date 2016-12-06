import fileinput
import subprocess
import sys
import argparse
import os
import shutil
from distutils.dir_util import copy_tree

# color da bash
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
NOCOLOR = '\033[0m'

validResponse = {"yes": True, "y": True, "ye": True, "no": False, "n": False, '': True}
validBaudrate = {"9600": "9600", "57600": "57600", "115200": "115200", '': "9600"}


def options(option, valid, errorMessage):
    choice = raw_input(option).lower()
    if valid is None:
        return choice
    if choice == '':
        return valid[choice]
    elif choice in valid:
        return valid[choice]
    else:
        print FAIL + "[Error] - " + NOCOLOR + "Please enter a valid answer: " + errorMessage + "\n"
        return options(option, valid, errorMessage)


def bootstrap(directory):
    check_dep()

    if os.path.isdir(directory):
        shutil.rmtree(directory)

    serial = options("Configure serial communication?" + BLUE + " [Yes/No]: " + NOCOLOR, validResponse,
                     "[Yes/No - y/n]")
    if serial:
        baudrate = options("Enter Baudrate" + BLUE + " [9600,57600,115200]: " + NOCOLOR, validBaudrate,
                           "[9600,57600,115200]")

    neoPixel = options("Import and set up NeoPixel library and wrapper?" + BLUE + " [Yes/No]: " + NOCOLOR,
                       validResponse, "[Yes/No - y/n]")
    if neoPixel:
        strips = options("Number of strips?" + BLUE + " [Any Nr.]: " + NOCOLOR, None, "[Number of strips]")
        numPixl = options("Number of pixels" + BLUE + " [Any Nr.]: " + NOCOLOR, None, "[Number of pixel per strip]")
        strips = "1" if strips == "" else strips
        numPixl = "1" if numPixl == "" else numPixl

    timers = options("Set up some timers?" + BLUE + " [Yes/No]: " + NOCOLOR, validResponse, "[Yes/No - y/n]")
    git = options("Make it git" + BLUE + " [Yes/No]: " + NOCOLOR, validResponse, "[Yes/No - y/n]")

    try:
        subprocess.check_call(['mkdir', directory])
        subprocess.check_call(['platformio', 'init', '--board', 'uno', '--board', 'teensy31', '-d', directory])
    except:
        print FAIL + "[Installation Error] "
        sys.exit(0)

    copyFrom = "./src/main"
    copy_tree(copyFrom, directory + "/src")

    copyFrom = "./src/lib"
    copy_tree(copyFrom, directory + "/lib")

    if serial:
        replaceAll(directory + '/src/main.cpp', "//linefeed\n", "char lf = \'\\n\';\n")
        replaceAll(directory + '/src/main.cpp', "//setup\n", "Serial.begin(" + baudrate + ");\n")
        replaceAll(directory + '/src/main.cpp', "//loop\n", "checkSerial();\n")
        replaceAll(directory + '/src/main.cpp', "//chSerialIn\n", "void checkSerial();\n")
        replaceAll(directory + '/src/main.cpp', "//inByte\n", "String inByte;\n")
        file = open('./helpers/serial.h', "r")
        lines = "".join(file.readlines())
        file.close
        replaceAll(directory + '/src/main.cpp', "//serial\n", lines)
    else:
        replaceAll(directory + '/src/main.cpp', "//linefeed\n", "")
        replaceAll(directory + '/src/main.cpp', "//setup\n", "")
        replaceAll(directory + '/src/main.cpp', "//loop\n", "")
        replaceAll(directory + '/src/main.cpp', "//serial\n", "")
        replaceAll(directory + '/src/main.cpp', "//chSerialIn\n", "")
        replaceAll(directory + '/src/main.cpp', "//inByte\n", "")

    if neoPixel:
        replaceAll(directory + '/src/main.cpp', "//neopixel\n", "#include \"neoPixelWrapper.h\";\n")
        # replaceAll(directory + '/src/main.cpp',"//strips\n", "#include \"stripSegments.h\";\n")
        file = open('./helpers/wrapper.h', "r")
        lines = "".join(file.readlines())
        replaceAll(directory + '/src/main.cpp', "//wrapper\n", lines)
        file.close
        wrapper = ""
        stripmapping = ""

        for i in range(0, int(strips)):
            wrapper += "\tWrapper_class(NUMBEROFPIXELS, STRIP_PIN_" + str(i) + "),\n"
            stripmapping += "#define STRIP_PIN_" + str(i) + " " + str(i) + "\n"

        replaceAll(directory + '/src/main.cpp', "//stripdetails\n", wrapper)
        replaceAll(directory + '/lib/mapping/MAPPING.h', "//stripmapping\n", stripmapping)
        replaceAll(directory + '/lib/mapping/MAPPING.h', "//numberofpixels\n", "#define NUMBEROFPIXELS " + numPixl)
        subprocess.check_call(['platformio', 'lib', 'install', 'Adafruit NeoPixel'], cwd=directory)
    else:
        replaceAll(directory + '/src/main.cpp', "//neopixel\n", "")
        replaceAll(directory + '/src/main.cpp', "//strips\n", "")
        replaceAll(directory + '/src/main.cpp', "//stripdetails\n", "")
        replaceAll(directory + '/lib/mapping/MAPPING.h', "//stripmapping\n", "")
        replaceAll(directory + '/lib/mapping/MAPPING.h', "//numberofpixels\n", "")

    if timers:
        file = open('./helpers/timer.h', "r")
        lines = "".join(file.readlines())
        replaceAll(directory + '/src/main.cpp', "//timerfunctions\n", lines)
        file.close
        replaceAll(directory + '/src/main.cpp', "//timer\n", "long currentTime[8];\nlong waitTime[8];\n")
    else:
        replaceAll(directory + '/src/main.cpp', "//timerfunctions\n", "")
        replaceAll(directory + '/src/main.cpp', "//timer\n", "")

    if git:
        subprocess.check_call(['git', 'init'], cwd=directory)


def check_dep():
    # check dependencies
    print NOCOLOR + "Checking for dependencies..."
    try:
        subprocess.check_output(['platformio'])
    except:
        print FAIL + "[Error] - " + NOCOLOR + " could not find platformio dependencie - "  "Trying to install platfromio with brew"
        try:
            subprocess.check_call(['brew', 'install', 'platformio'])
        except:
            print FAIL + "[Error] - " + NOCOLOR + " could not execute 'brew install platformio'"
            sys.exit(0)


def replaceAll(file, searchExp, replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=GREEN + 'Bootstraps a C++ Arduino project for quick prototyping' + NOCOLOR)
    parser.add_argument('--directory', '-d', help='path to directory')
    args = parser.parse_args()
    if args.directory == None:
        bootstrap('dist')
    else:
        bootstrap(directory)
