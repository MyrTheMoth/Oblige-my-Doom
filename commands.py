import subprocess
import os
from datetime import datetime
import shutil

outputDirectory = ""
outputFile = ""


def updateOutput():
    global outputDirectory
    global outputFile
    directory = os.path.dirname(os.path.realpath(__file__))
    outputDirectory = os.path.join(directory, "output")
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outputFile = "output-" + str(now) + ".wad"
    print(outputDirectory)
    print(outputFile)


def runOblige(configList):
    global outputDirectory
    global outputFile
    obligeArgs = [configList[0], "--batch",
                  outputFile, '--load', configList[1]]
    print(obligeArgs)
    subprocess.run(obligeArgs)
    if os.path.exists(outputDirectory) is False:
        os.makedirs(outputDirectory)
    shutil.move(outputFile, outputDirectory)
    outputFile = os.path.join(outputDirectory, outputFile)


def launchOblige(obligeFile):
    subprocess.Popen(obligeFile)


def runSourcePort(configList, pwadList, argumentString):
    global outputFile
    sourcePortArgs = [configList[2], "-iwad",
                      configList[3], "-file", outputFile]

    if len(pwadList) is 0:
        if argumentString is not "":
            argumentList = argumentString.split(" ")
            for arguments in argumentList:
                sourcePortArgs.append(arguments)
        print(sourcePortArgs)
        subprocess.Popen(sourcePortArgs)
    else:
        for pwad in pwadList:
            sourcePortArgs.append(pwad)
        if argumentString is not "":
            argumentList = argumentString.split(" ")
            for arguments in argumentList:
                sourcePortArgs.append(arguments)
        print(sourcePortArgs)
        subprocess.Popen(sourcePortArgs)
