import subprocess


def runOblige(configList):
    obligeArgs = [configList[0], "--batch",
                  'OUTPUT.wad', '--load', configList[1]]
    subprocess.run(obligeArgs)


def runSourcePort(configList, pwadList):
    sourcePortArgs = [configList[2], "-iwad",
                      configList[3], "-file", "OUTPUT.wad"]
    if len(pwadList) is 0:
        subprocess.Popen(sourcePortArgs)
    else:
        for pwad in pwadList:
            sourcePortArgs.append(pwad)
        subprocess.Popen(sourcePortArgs)
