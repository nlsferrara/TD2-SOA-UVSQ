import xml.etree.ElementTree as ET
print(ET.parse('"demande_pret_Doe.xml"').getroot().tag)