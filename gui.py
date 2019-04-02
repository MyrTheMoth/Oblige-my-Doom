import PySimpleGUIQt as sg
import config as conf
import commands as comm
import assets as asse
import os

configList = ["", "", "", "", ""]
pwadList = []


def setValues(configList, pwadList):
    window.Element("oblige").Update(configList[0])
    window.Element("oblige_config").Update(configList[1])
    window.Element("source_port").Update(configList[2])
    window.Element("iwad").Update(configList[3])
    window.Element("arguments").Update(configList[4])
    window.Element("pwads").Update(pwadList)


def getValues():
    configList = ["", "", "", "", ""]
    pwadList = []
    configList[0] = window.Element("oblige").Get()
    configList[1] = window.Element("oblige_config").Get()
    configList[2] = window.Element("source_port").Get()
    configList[3] = window.Element("iwad").Get()
    configList[4] = window.Element("arguments").Get()
    fileList = window.Element("pwads").GetListValues()
    if len(fileList) is not 0:
        for pwad in fileList:
            pwadList.append(pwad)
    return configList, pwadList


def saveConfig(configList, pwadList, name):
    conf.writeXML(conf.buildConfig(configList, pwadList), name)


def loadConfig(name):
    configList, pwadList = conf.readXML(name)
    configCheck = 0
    while configCheck <= 4:
        if configList[configCheck] is None:
            configList[configCheck] = ""
        configCheck += 1
    return configList, pwadList


def updateLastConfig():
    print("Saving Last Config")
    configList, pwadList = getValues()
    print(configList)
    print(pwadList)
    saveConfig(configList, pwadList, "config")


if os.path.isfile("config.xml") is False:
    print("Last Config does not exist")
    saveConfig(configList, pwadList, "config")
else:
    print("Last Config exists")
    configList, pwadList = loadConfig("config")

game_layout = [
    [sg.Text("Oblige Executable")],
    [sg.InputText(default_text=configList[0], key="oblige", do_not_clear=True),
     sg.FileBrowse(target="oblige")],
    [sg.Text("Oblige Config")],
    [sg.InputText(default_text=configList[1], key="oblige_config", do_not_clear=True), sg.FileBrowse(
        target="oblige_config", file_types=(("Text Files", "*.txt"),))],
    [sg.Text("Source Port")],
    [sg.InputText(default_text=configList[2], key="source_port", do_not_clear=True),
     sg.FileBrowse(target="source_port")],
    [sg.Text("IWAD")],
    [sg.InputText(default_text=configList[3], key="iwad", do_not_clear=True), sg.FileBrowse(
        target="iwad", file_types=(("IWAD Files", "*.wad"),))]
]

mod_layout = [
    [sg.Listbox(key="pwads", values=pwadList, size=(50, 5))],
    [sg.FilesBrowse("Add", key="Add", target=(
        "Add"), enable_events=True, file_types=(("PWAD Files", "*.wad;*.pk3"),)), sg.Button("Remove"), sg.Button("Clear"), sg.Text("", visible=False), sg.Button("▲"), sg.Button("▼")]
]

layout = [
    [sg.Frame("Game", game_layout)],
    [sg.Frame("PWADs", mod_layout)],
    [sg.Text("Arguments"), sg.InputText(
        default_text=configList[4], key="arguments", do_not_clear=True)],
    [sg.Button("Launch"), sg.FileSaveAs("Save Game", key="SaveConfig", target=("SaveConfigStore"), enable_events=True, file_types=(("XML Files", "*.xml"),)),
     sg.FileBrowse("Load Game", key="LoadConfig", target=(
         "LoadConfigStore"), enable_events=True, file_types=(("XML Files", "*.xml"),)),
     sg.Button("Oblige")],
    [sg.InputText("SaveConfigStore", key="SaveConfigStore", visible=False, enable_events=True), sg.InputText(
        "LoadConfigStore", key="LoadConfigStore", visible=False, enable_events=True)]
]

generate_layout = [
    [sg.Text("Generating Map, Time Depends on your Oblige Config",
             justification="center", font=("Helvetica", 25))],
    [sg.Text("Please wait until your game starts",
             justification="center", font=("Helvetica", 25))]
]

window = sg.Window("Oblige my Doom", auto_size_text=True, auto_size_buttons=True,
                   default_element_size=(40, 1), resizable=False).Layout(layout)

pop = sg.Window("Oblige", no_titlebar=True, keep_on_top=True,
                auto_size_text=True, resizable=False).Layout(generate_layout)


while True:
    event, values = window.Read()
    print(event, values)

    if event is None:
        updateLastConfig()
        break

    if event == "Add":
        if values["Add"] is not "":
            pwadList = window.Element("pwads").GetListValues()
            if len(pwadList) is not 0 and pwadList[0] is "":
                pwadList.remove("")
            fileList = values["Add"].split(";")
            for pwad in fileList:
                if pwad not in pwadList:
                    pwadList.append(pwad)
                    window.Element("pwads").Update(pwadList)

    if event == "Remove":
        pwad = "".join(values["pwads"])
        pwadList = window.Element("pwads").GetListValues()
        if len(pwadList) is not 0 and pwad is not "":
            pwadList.remove(pwad)
        window.Element("pwads").Update(pwadList)

    if event == "Clear":
        window.Element("pwads").Update([])

    if event == "▲":
        pwad = "".join(values["pwads"])
        pwadList = window.Element("pwads").GetListValues()
        if len(pwadList) is not 0 and pwad is not "":
            if pwadList.index(pwad) is not 0:
                a, b = pwadList.index(pwad), pwadList.index(pwad)-1
                pwadList[b], pwadList[a] = pwadList[a], pwadList[b]
        window.Element("pwads").Update(pwadList)
        window.Element("pwads").SetValue(pwad)

    if event == "▼":
        pwad = "".join(values["pwads"])
        pwadList = window.Element("pwads").GetListValues()
        if len(pwadList) is not 0 and pwad is not "":
            if pwadList.index(pwad) is not len(pwadList)-1:
                a, b = pwadList.index(pwad), pwadList.index(pwad)+1
                pwadList[b], pwadList[a] = pwadList[a], pwadList[b]
        window.Element("pwads").Update(pwadList)
        window.Element("pwads").SetValue(pwad)

    if event == "SaveConfigStore":
        if values["SaveConfigStore"] is not "":
            configList, pwadList = getValues()
            saveConfig(configList, pwadList, values["SaveConfigStore"])

    if event == "LoadConfigStore":
        if values["LoadConfigStore"] is not "":
            configList, pwadList = loadConfig(values["LoadConfigStore"])
            setValues(configList, pwadList)

    if event == "Launch":
        configList, pwadList = getValues()
        launchReady = True
        launchCheck = 0
        while launchCheck < 4:
            if configList[launchCheck] is "":
                launchReady = False
            launchCheck += 1
        if launchReady is True:
            pop.Finalize()
            comm.updateOutput()
            comm.runOblige(configList)
            pop.Close()
            comm.runSourcePort(configList, pwadList)
        elif launchReady is False:
            sg.PopupError("Cannot Launch with missing Config",
                          keep_on_top=True)

    if event == "Oblige":
        obligeFile = values["oblige"]
        if obligeFile is "":
            sg.PopupError("Cannot Launch Oblige without file path",
                          keep_on_top=True)
        else:
            comm.launchOblige(obligeFile)
