import subprocess
from os import path, makedirs
from datetime import datetime
import shutil

outputDirectory = ""
outputFile = ""

# Get the current date and time to timestamp the new Oblige Map .wad to Generate


def updateOutput():
    global outputDirectory
    global outputFile
    outputDirectory = 'output/'
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outputFile = "output-" + str(now) + ".wad"
    print(outputDirectory)
    print(outputFile)

# Execute Oblige in Batch mode to generate the Map .wad given a list of available settings


def runOblige(configList):
    global outputDirectory
    global outputFile
    obligeArgs = [configList[0], "--batch",
                  outputFile, '--load', configList[1]]
    print(obligeArgs)
    subprocess.run(obligeArgs)
    if path.exists(outputDirectory) is False:
        makedirs(outputDirectory)
    shutil.move(outputFile, outputDirectory)
    outputFile = outputDirectory + outputFile

# Execute Oblige in Window mode given the filepath for the executable


def launchOblige(obligeFile):
    subprocess.Popen(obligeFile)

# Execute the source port given a pair of lists with the available settings and pwads


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
