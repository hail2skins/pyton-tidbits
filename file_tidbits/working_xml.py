import xml.etree.ElementTree as ET

def parse_xml_et(file):
    tree = ET.parse(file)
    root = tree.getroot()
    print("Domains for: " + root.attrib['name'])
    for child in root:
        print('\t' + child.attrib['name'], child.tag)
        
def add_xml_element_et(file, element, attrib, value):
    tree = ET.parse(file)
    root = tree.getroot()
    child = ET.Element(element)
    child.attrib[attrib] = value
    root.append('\t' + child)
    tree.write(file)
    
def change_xml_element_et(file, element, attrib, oldvalue, newvalue):
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root:
        if child.attrib[attrib] == oldvalue:
            child.attrib[attrib] = newvalue
            tree.write(file)
            return True
    return False
        
#parse_xml_et('./file_tidbits/files_to_read/ef_author.xml')
#add_xml_element_et('./file_tidbits/files_to_read/ef_author.xml', 'domain', 'name', 'Golang')
change_xml_element_et('./file_tidbits/files_to_read/ef_author.xml', 'domain', 'name', 'Golang', 'Go')
    
    