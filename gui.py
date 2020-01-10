import PySimpleGUIQt as sg
import config as conf
import commands as comm
import data
from os import path, remove

configList = ["", "", "", "", "", ""]
pwadList = []
sessionsList = []
sessionsListBox = []

# Set the Values of each element in the Window given a pair of lists of available settings and pwads


def setConfigValues(configList, pwadList):
    window.Element("oblige").Update(configList[0])
    window.Element("oblige_config").Update(configList[1])
    window.Element("source_port").Update(configList[2])
    window.Element("iwad").Update(configList[3])
    window.Element("arguments").Update(configList[4])
    window.Element("pwads").Update(pwadList)
    window.Element("output").Update(configList[5])

# Set the Values of the Session List in the Window given a list of available formatted sessions


def setSessionsValues(sessionsListBox):
    window.Element("session_list").Update(sessionsListBox)
    return sessionsListBox

# Format the Values of the Session List in the Window given a list of available sessions


def formatSessionsValues(sessionsList):
    sessionsListBox = []
    if len(sessionsList) is not 0:
        for session in sessionsList:
            sessionsListBox.append(session["id"] + ": " + session["name"])
    return sessionsListBox

# Get the values of each element in the Window and return it as a pair of lists of available settings and pwads


def getConfigValues():
    configList = ["", "", "", "", "", ""]
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
    configList[5] = window.Element("output").Get()
    return configList, pwadList

# Get the values of the Session List in the Window and return it as a list of available sessions


def getSessionsValues():
    sessionsListBox = []
    sessionList = window.Element("session_list").GetListValues()
    if len(sessionList) is not 0:
        for session in sessionList:
            sessionsListBox.append(session)
    return sessionsListBox

# Save a XML Config File given a pair of lists of available settings and pwads, and a file name


def saveConfig(configList, pwadList, name):
    conf.writeConfigXML(conf.buildConfig(configList, pwadList), name)

# Load a XML Config File given a file name


def loadConfig(name):
    configList, pwadList = conf.readConfigXML(name)
    configCheck = 0
    while configCheck <= 5:
        if configList[configCheck] is None:
            print(configList[configCheck])
            configList[configCheck] = ""
            print(configList[configCheck])
        configCheck += 1
    print(configList)
    print(pwadList)
    return configList, pwadList

# Save the Sessions XML


def saveSessions(sessionsList):
    conf.writeSessionsXML(conf.buildSession(sessionsList))

# Load the Sessions XML


def loadSessions():
    sessionsList = conf.readSessionsXML()
    return sessionsList

# Update the Last Used Configuration


def updateLastConfig():
    print("Saving Last Config")
    configList, pwadList = getConfigValues()
    print(configList)
    print(pwadList)
    saveConfig(configList, pwadList, "config")

# Add a Session to the Session List


def addSession(sessionsList, dic):
    sessionsList.append(dic)
    return sessionsList

# Remove a Session from the Session List


def removeSession(sessionsList, id):
    if len(sessionsList) is not 0:
        for session in sessionsList:
            if session["id"] is id:
                sessionsList.remove(session)
    return sessionsList

# Rename a Session from the Session List


def renameSession(sessionsList, id, name):
    if len(sessionsList) is not 0:
        for session in sessionsList:
            if session["id"] is id:
                session["name"] = name
    return sessionsList

# Get the latest Session ID


def updateSessionId(sessionsList):
    sessionId = 1
    if len(sessionsList) is not 0:
        for session in sessionsList:
            if int(session["id"]) >= sessionId:
                sessionId = int(session["id"]) + 1
    return sessionId

# Turn XML Attrib Lists into Python Lists


def stringToList(stringList):
    stringList = "".join(stringList)
    stringList = stringList.replace("[", "")
    stringList = stringList.replace("]", "")
    stringList = stringList.replace("\'", "")
    stringList = stringList.split(", ")
    if len(stringList) < 2:
        if stringList[0] is None or "None":
            stringList = []
    return stringList

# Check if there is already Last Used Configuration XML File, if there is, Load it, if there isn't, Create one


if path.isfile("config.xml") is False:
    print("Last Config does not exist")
    saveConfig(configList, pwadList, "config")
else:
    print("Last Config exists")
    configList, pwadList = loadConfig("config")

# Check if there is already an existing Sessions XML File, if there is, Load it, if there isn't, Create one

if path.isfile("sessions.xml") is False:
    print("Sessions File does not exist")
    saveSessions(sessionsList)
else:
    print("Sessions File exists")
    sessionsList = loadSessions()
    sessionsListBox = formatSessionsValues(sessionsList)

# Window Layout declarations

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

sessions_layout = [
    [sg.Listbox(key="session_list", values=sessionsListBox, size=(50, 5))],
    [sg.Button("Select"), sg.InputText(
        default_text="", key="session_name", do_not_clear=True), sg.Button("Rename"), sg.Button("Delete")]
]

layout = [
    [sg.Frame("Game", game_layout)],
    [sg.Frame("PWADs", mod_layout)],
    [sg.Text("Arguments"), sg.InputText(
        default_text=configList[4], key="arguments", do_not_clear=True)],
    [sg.Button("Create"), sg.FileSaveAs("Save Config", key="SaveConfig", target=("SaveConfigStore"), enable_events=True, file_types=(("XML Files", "*.xml"),)),
     sg.FileBrowse("Load Config", key="LoadConfig", target=(
         "LoadConfigStore"), enable_events=True, file_types=(("XML Files", "*.xml"),)),
     sg.Button("Oblige")],
    [sg.Text("Oblige Map: "), sg.InputText(default_text=configList[5],
                                           key="output", do_not_clear=True, disabled=True)],
    [sg.InputText("SaveConfigStore", key="SaveConfigStore", visible=False, enable_events=True), sg.InputText(
        "LoadConfigStore", key="LoadConfigStore", visible=False, enable_events=True)],
    [sg.Frame("Sessions", sessions_layout)],
    [sg.Button("Play")]
]

generate_layout = [
    [sg.Text("Generating Map, Time Depends on your Oblige Config",
             justification="center", font=("Helvetica", 25))]
]

# Assemble the Windows

window = sg.Window("Oblige my Doom", auto_size_text=True, auto_size_buttons=True,
                   default_element_size=(40, 1), resizable=False, icon=data.default_icon).Layout(layout)

pop = sg.Window("Oblige", no_titlebar=True, keep_on_top=True,
                auto_size_text=True, resizable=False).Layout(generate_layout)

# Persistent PySimpleGUI Window Loop

while True:
    event, values = window.Read()
    print(event, values)

    # Event Actions for Closing the Window

    if event is None:
        updateLastConfig()
        break

    # Event Actions for Adding PWADs to the List

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

    # Event Actions for Removing a PWAD from the List

    if event == "Remove":
        pwad = "".join(values["pwads"])
        pwadList = window.Element("pwads").GetListValues()
        if len(pwadList) is not 0 and pwad is not "":
            pwadList.remove(pwad)
        window.Element("pwads").Update(pwadList)

    # Event Actions to Clear all PWADs from the List

    if event == "Clear":
        window.Element("pwads").Update([])

    # Event Actions to Increase a PWAD in the List Loading Order

    if event == "▲":
        pwad = "".join(values["pwads"])
        pwadList = window.Element("pwads").GetListValues()
        if len(pwadList) is not 0 and pwad is not "":
            if pwadList.index(pwad) is not 0:
                a, b = pwadList.index(pwad), pwadList.index(pwad)-1
                pwadList[b], pwadList[a] = pwadList[a], pwadList[b]
        window.Element("pwads").Update(pwadList)
        window.Element("pwads").SetValue(pwad)

    # Event Actions to Decrease a PWAD in the List Loading Order

    if event == "▼":
        pwad = "".join(values["pwads"])
        pwadList = window.Element("pwads").GetListValues()
        if len(pwadList) is not 0 and pwad is not "":
            if pwadList.index(pwad) is not len(pwadList)-1:
                a, b = pwadList.index(pwad), pwadList.index(pwad)+1
                pwadList[b], pwadList[a] = pwadList[a], pwadList[b]
        window.Element("pwads").Update(pwadList)
        window.Element("pwads").SetValue(pwad)

    # Event Actions to Save a Game Configuration

    if event == "SaveConfigStore":
        if values["SaveConfigStore"] is not "":
            configList, pwadList = getConfigValues()
            saveConfig(configList, pwadList, values["SaveConfigStore"])

    # Event Actions to Load a Game Configuration

    if event == "LoadConfigStore":
        if values["LoadConfigStore"] is not "":
            configList, pwadList = loadConfig(values["LoadConfigStore"])
            setConfigValues(configList, pwadList)

    # Event Actions to Create a Game

    if event == "Create":
        configList, pwadList = getConfigValues()
        launchReady = True
        launchCheck = 0
        sessionDict = {}
        while launchCheck < 4:
            if configList[launchCheck] is "":
                launchReady = False
            launchCheck += 1
        if launchReady is True:
            pop.Finalize()
            configList[5] = comm.updateOutput()
            comm.runOblige(configList)
            pop.Close()
            sessionDic = {
                "id": str(updateSessionId(sessionsList)),
                "name": configList[5],
                "configList": configList,
                "pwadList": pwadList
            }
            sessionsList = addSession(sessionsList, sessionDic)
            saveSessions(sessionsList)
            sessionsList = loadSessions()
            setSessionsValues(formatSessionsValues(sessionsList))
            setConfigValues(configList, pwadList)
        elif launchReady is False:
            sg.PopupError("Cannot Create Game with missing Config",
                          keep_on_top=True)

    # Event Actions to Play a Game

    if event == "Play":
        configList, pwadList = getConfigValues()
        launchReady = True
        launchCheck = 0
        while launchCheck <= 5:
            if configList[launchCheck] is "" and launchCheck is not 4:
                launchReady = False
            launchCheck += 1
        if launchReady is True:
            comm.runSourcePort(configList, pwadList)
        elif launchReady is False:
            sg.PopupError("Cannot Create Game with missing Config",
                          keep_on_top=True)

    # Event Actions to Launch Oblige

    if event == "Oblige":
        obligeFile = values["oblige"]
        if obligeFile is "":
            sg.PopupError("Cannot Launch Oblige without file path",
                          keep_on_top=True)
        else:
            comm.launchOblige(obligeFile)

    # Event Actions to Select a Session

    if event == "Select":
        selectedSessionId = ("".join(values["session_list"])).split(": ")[0]
        selectedSession = {}
        if selectedSessionId is not "":
            if len(sessionsList) is not 0:
                for session in sessionsList:
                    if session["id"] is selectedSessionId:
                        selectedSession = session
                        configList = stringToList(
                            selectedSession["configList"])
                        pwadList = stringToList(selectedSession["pwadList"])
                        setConfigValues(configList, pwadList)
        else:
            sg.PopupError("No Session Selected",
                          keep_on_top=True)

    # Event Actions to Rename a Session

    if event == "Rename":
        sessionName = window.Element("session_name").Get()
        window.Element("session_name").Update("")
        selectedSessionId = ("".join(values["session_list"])).split(": ")[0]
        if sessionName is not "":
            if len(sessionsList) is not 0:
                for session in sessionsList:
                    if session["id"] is selectedSessionId:
                        sessionsList = renameSession(
                            sessionsList, selectedSessionId, sessionName)
                        saveSessions(sessionsList)
                        sessionsList = loadSessions()
                        setSessionsValues(formatSessionsValues(sessionsList))
        else:
            sg.PopupError("Session Name cannot be empty",
                          keep_on_top=True)

    # Event Actions to Delete a Session

    if event == "Delete":
        selectedSessionId = ("".join(values["session_list"])).split(": ")[0]
        outputPath = ""
        if len(sessionsList) is not 0:
            for session in sessionsList:
                if session["id"] is selectedSessionId:
                    outputPath = path.join(
                        "output", stringToList(session["configList"])[5])
                    if path.exists(outputPath) is True:
                        remove(outputPath)
                    sessionsList = removeSession(
                        sessionsList, selectedSessionId)
                    configList[5] = ""
                    saveSessions(sessionsList)
                    sessionsList = loadSessions()
                    setSessionsValues(formatSessionsValues(sessionsList))
                    setConfigValues(configList, pwadList)
