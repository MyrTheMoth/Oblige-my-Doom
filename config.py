# XMLindent is credited to Erick M. Sprengel from Stack Overflow
import xml.etree.ElementTree as ET


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


def buildConfig(configList, pwadList, argumentString):
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
    arguments.text = argumentString
    return config


def writeXML(elem, name):
    XMLindent(elem)
    tree = ET.ElementTree(elem)
    if name.endswith(".xml") is False:
        name = name+".xml"
    tree.write(name, encoding="utf-8", xml_declaration=True)


def readXML(name):
    if name.endswith(".xml") is False:
        name = name+".xml"
    tree = ET.parse(name)
    root = tree.getroot()
    xmlConfigTextList = [
        elem.text for elem in root if elem is not root and elem is not root.find('pwads')]
    print(xmlConfigTextList)
    pwadElement = root.find('pwads')
    xmlPwadTextList = [
        elem.text for elem in pwadElement if elem is not pwadElement]
    print(xmlPwadTextList)
    return xmlConfigTextList, xmlPwadTextList
