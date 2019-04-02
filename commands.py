import subprocess
import os
from datetime import datetime
import shutil

outputDirectory = ""
outputFile = ""


def updateOutput():
    global outputDirectory
    global outputFile
    outputDirectory = 'output/'
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
    outputFile = outputDirectory + outputFile


def launchOblige(obligeFile):
    subprocess.Popen(obligeFile)


def runSourcePort(configList, pwadList):
    global outputFile
    sourcePortArgs = [configList[2], "-iwad",
                      configList[3], "-file", outputFile]

    if len(pwadList) is 0:
        if configList[4] is not "":
            argumentList = configList[4].split(" ")
            for arguments in argumentList:
                sourcePortArgs.append(arguments)
        print(sourcePortArgs)
        subprocess.Popen(sourcePortArgs)
    else:
        for pwad in pwadList:
            sourcePortArgs.append(pwad)
        if configList[4] is not "":
            argumentList = configList[4].split(" ")
            for arguments in argumentList:
                sourcePortArgs.append(arguments)
        print(sourcePortArgs)
        subprocess.Popen(sourcePortArgs)
