import PySimpleGUI as sg
import config as conf
import commands as comm
import os

loading_animation = b'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'

game_layout = [
    [sg.Text("Oblige Executable")],
    [sg.InputText(key="oblige", do_not_clear=True),
     sg.FileBrowse(target="oblige")],
    [sg.Text("Oblige Config")],
    [sg.InputText(key="oblige_config", do_not_clear=True), sg.FileBrowse(
        target="oblige_config", file_types=(("Text Files", "*.txt"),))],
    [sg.Text("Source Port")],
    [sg.InputText(key="source_port", do_not_clear=True),
     sg.FileBrowse(target="source_port")],
    [sg.Text("IWAD")],
    [sg.InputText(key="iwad", do_not_clear=True), sg.FileBrowse(
        target="iwad", file_types=(("IWAD Files", "*.wad"),))]
]

column_layout = [
    [sg.Button("▲")],
    [sg.Button("▼")]
]

mod_layout = [
    [sg.Text("PWADs")],
    [sg.Listbox(key="pwads", values=[], size=(60, 9)),
     sg.Column(column_layout)],
    [sg.FilesBrowse("Add", key="Add", target=("Add"), enable_events=True, file_types=(("PWAD Files", "*.wad;*.pk3"),)),
     sg.Button("Remove"), sg.Button("Clear")]
]

layout = [
    [sg.Frame("Game", game_layout), sg.Frame("Mods", mod_layout)],
    [sg.Button("Launch"), sg.FileSaveAs("Save Game", key="SaveConfig", target=("SaveConfig"), enable_events=True, file_types=(("XML Files", "*.xml"),)),
     sg.FileBrowse("Load Game", key="LoadConfig", target=(
         "LoadConfig"), enable_events=True, file_types=(("XML Files", "*.xml"),)),
     sg.Button("Oblige"), sg.Text("Arguments"), sg.InputText(key="arguments", do_not_clear=True)]
]

window = sg.Window("Oblige my Doom", auto_size_text=True, auto_size_buttons=True,
                   default_element_size=(60, 1)).Layout(layout)

while True:
    event, values = window.Read()
    print(event, values)

    if event is None:
        break

    if event == "Add":
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
        pwadList = []
        window.Element("pwads").Update(pwadList)

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

    if event == "SaveConfig":
        configList = ["", "", "", ""]
        pwadList = []
        configList[0] = values["oblige"]
        configList[1] = values["oblige_config"]
        configList[2] = values["source_port"]
        configList[3] = values["iwad"]
        fileList = window.Element("pwads").GetListValues()
        if len(fileList) is not 0:
            for pwad in fileList:
                pwadList.append(pwad)
        argumentString = values["arguments"]
        conf.writeXML(conf.buildConfig(
            configList, pwadList, argumentString), values["SaveConfig"])

    if event == "LoadConfig":
        configList, pwadList = conf.readXML(values["LoadConfig"])
        print(configList)
        print(pwadList)
        window.Element("oblige").Update(configList[0])
        window.Element("oblige_config").Update(configList[1])
        window.Element("source_port").Update(configList[2])
        window.Element("iwad").Update(configList[3])
        window.Element("pwads").Update(pwadList)
        window.Element("arguments").Update(configList[4])

    if event == "Launch":
        configList = ["", "", "", ""]
        pwadList = []
        configList[0] = values["oblige"]
        configList[1] = values["oblige_config"]
        configList[2] = values["source_port"]
        configList[3] = values["iwad"]
        fileList = window.Element("pwads").GetListValues()
        if len(fileList) is not 0:
            for pwad in fileList:
                pwadList.append(pwad)
        argumentString = values["arguments"]
        print(configList)
        launchReady = True
        for config in configList:
            if config is "":
                launchReady = False
        if launchReady is True:
            sg.PopupAnimated(image_source=loading_animation,
                             message="Generating Map, Time Depends on your Oblige Config", alpha_channel=1, time_between_frames=10)
            comm.updateOutput()
            comm.runOblige(configList)
            sg.PopupAnimated(image_source=None)
            comm.runSourcePort(configList, pwadList, argumentString)
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
