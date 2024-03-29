# XMLindent is credited to Erick M. Sprengel from Stack Overflow
import xml.etree.ElementTree as ET

# Indentate the Element Tree for Easier Reading


def XMLindent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            XMLindent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# Create the XML Structure given a pair of lists of available settings and pwads, and return the completed Element Tree


def buildConfig(configList, pwadList):
    config = ET.Element("config")
    oblige = ET.SubElement(config, "oblige")
    oblige.text = configList[0]
    obligeConfig = ET.SubElement(config, "oblige_config")
    obligeConfig.text = configList[1]
    sourcePort = ET.SubElement(config, "source_port")
    sourcePort.text = configList[2]
    iwad = ET.SubElement(config, "iwad")
    iwad.text = configList[3]
    pwads = ET.SubElement(config, "pwads")
    if len(pwadList) is not 0:
        pwadCount = 0
        for pwad in pwadList:
            pwadCount += 1
            pwadElement = ET.SubElement(pwads, "pwad"+str(pwadCount))
            pwadElement.text = pwad
    arguments = ET.SubElement(config, "arguments")
    arguments.text = configList[4]
    output = ET.SubElement(config, "output")
    output.text = configList[5]
    return config

# Write the XML to file system given an Element Tree and file name


def writeConfigXML(elem, name):
    XMLindent(elem)
    tree = ET.ElementTree(elem)
    if name.endswith(".xml") is False:
        name = name+".xml"
    tree.write(name, encoding="utf-8", xml_declaration=True)

# Read an XML from file system given a file name and return a pair of lists of file paths for each available setting and PWADs


def readConfigXML(name):
    if name.endswith(".xml") is False:
        name = name+".xml"
    tree = ET.parse(name)
    root = tree.getroot()
    xmlConfigList = [
        elem.text for elem in root if elem is not root and elem is not root.find('pwads')]
    print(xmlConfigList)
    pwadElement = root.find('pwads')
    xmlPwadList = [
        elem.text for elem in pwadElement if elem is not pwadElement]
    print(xmlPwadList)
    return xmlConfigList, xmlPwadList

# Create the Session XML Structure given a list of session dictionaries and return the completed Element Tree


def buildSession(sessionList):
    sessions = ET.Element("sessions")
    if len(sessionList) is not 0:
        sessionCount = 0
        for session in sessionList:
            sessionCount += 1
            sessionElement = ET.SubElement(
                sessions, "session"+str(sessionCount))
            sessionElement.attrib = session
    return sessions

# Write the Sessions XML to file system given an Element Tree


def writeSessionsXML(elem):
    XMLindent(elem)
    tree = ET.ElementTree(elem)
    tree.write("sessions.xml", encoding="utf-8", xml_declaration=True)

# Read a Session XML from file system given a file name and return a dictionary with the config of each session


def readSessionsXML():
    tree = ET.parse("sessions.xml")
    root = tree.getroot()
    xmlSessionsList = [
        elem.attrib for elem in root if elem is not root]
    print(xmlSessionsList)
    return xmlSessionsList
