# coding: utf-8
import os
import glob
import codecs
import xlwt # Excel library from http://www.python-excel.org/
from optparse import OptionParser
import xml.dom.minidom

def getOptions():
	parser = OptionParser()
	parser.add_option("-d", "--directory", help="Android project root directory.", metavar="FILE")
	parser.add_option("-o", "--output", help="Output excel file.")
	return parser.parse_args()

def getNodeValue(node):
	value = ''
	if node.firstChild:
		value = node.firstChild.toxml()
		node.removeChild(node.firstChild)

	return value

def getNodeKey(node):	
	nodeinscript = node.attributes['name'].value
	return nodeinscript
	
def getPluralNodeKey(node):
	nodeinscript = node.attributes['quantity'].value
	return nodeinscript

def getNodeValueByKey(nodes, key):
	value = ''
	for node in nodes:
		if getNodeKey(node) == key:
			while node.hasChildNodes():
				value = value + getNodeValue(node)
			return value
	return ''
	
def getPluralNodeValueByKey(nodesPlural, key):
	value = ''
	for node in nodesPlural:
		if getPluralNodeKey(node) == key:
			while node.hasChildNodes():
				value = value + getNodeValue(node)
				nodesPlural.remove(node)
			return value
	return ''

def getNodeList(xmlFile):
	xmldoc = xml.dom.minidom.parse(xmlFile)
	xmlitem = xmldoc.getElementsByTagName('string')
	return  xmlitem 
	
def getNodeListPlural(xmlFile):
	xmldoc = xml.dom.minidom.parse(xmlFile)
	xmlitemplural = xmldoc.getElementsByTagName('plurals')
	return xmlitemplural
	
def getNodeListPluralQuantity(xmlFile):
	xmldoc = xml.dom.minidom.parse(xmlFile)
	xmlitemplural = xmldoc.getElementsByTagName('item')
	return xmlitemplural

def initWorkBook():
	return xlwt.Workbook(encoding='utf-8')

def addSheet(book, name):
	return book.add_sheet(name, cell_overwrite_ok=True)

def saveWorkBook(book, fileName):
	book.save(fileName)

def writeMasterKeys(sheet, nodes, nodesPlural):
	sheet.write(0, 0, 'keys')
	row = 1
	for node in nodes:
		sheet.write(row, 0, getNodeKey(node))
		row += 1
	for node in nodesPlural:
		sheet.write(row, 0, getPluralNodeKey(node))
		row += 1
		
def rewritePluralKeys(sheet, nodes, nodesPlural):
	sheet.write(0, 0, 'keys')
	row = 1
	for node in nodes:
		sheet.write(row, 0, getNodeKey(node))
		row += 1
	for node in nodesPlural:
		pluralname = getNodeKey(node)
		keyone = 'plural:' + pluralname + ':one'
		keyother = 'plural:' + pluralname + ':other'
		sheet.write(row, 0, keyone)
		row += 1
		sheet.write(row, 0, keyother)
		row += 1

def writeMasterValues(sheet, nodes, nodesPlural):
	row = 1
	value = ''
	for node in nodes:		
		while node.hasChildNodes():
			value = value + getNodeValue(node)
		sheet.write(row, 1, value)
		value = ''
		row += 1
	for node in nodesPlural:
		while node.hasChildNodes():
			value = value + getNodeValue(node)
		sheet.write(row, 1, value)
		value = ''
		row += 1

def writeValues(sheet, masterNodeList, masterNodeListPlural, nodes, nodesPlural, col):
	row = 1
	for node in masterNodeList:
		key = getNodeKey(node)
		value = getNodeValueByKey(nodes, key)
		sheet.write(row, col, value)
		row += 1
	for node in masterNodeListPlural:
		key = getPluralNodeKey(node)
		value = getPluralNodeValueByKey(nodesPlural, key)
		sheet.write(row, col, value)		
		row += 1

def writeNodesToColumn(sheet, masterNodeList, masterNodeListPlural, nodes, nodesPlural, langCode, col):
	sheet.write(0, col, langCode)
	writeValues(sheet, masterNodeList, masterNodeListPlural, nodes, nodesPlural, col)

def writeMasterNodeList(sheet, nodes, nodesPlural):
	writeMasterKeys(sheet, nodes, nodesPlural)
	writeMasterValues(sheet, nodes, nodesPlural)

def getStringsXmlFiles(directory, xmlFileName):
	return glob.glob(os.path.join(options.directory, 'res/values-*/' + xmlFileName))


def getMasterNodeList(directory): 
	xmlFile = glob.glob(os.path.join(options.directory, 'res/values/strings.xml'))[0]
	xmlstringlist = getNodeList(xmlFile)
	xmlstringlist.append(getNodeListPlural(xmlFile)) 
	return getNodeList(xmlFile)

def getLangCode(xmlFile):
	(head, tail) = os.path.split(xmlFile)
	(head, tail) = os.path.split(head)
	return tail.replace('values-', '')
	
def getFileName(xmlFile):
	(head, tail) = os.path.split(xmlFile)
	return tail
	
def getNameForSheet(xmlFile):
	(head, tail) = os.path.split(xmlFile)
	return tail.replace('strings_', '')
	
def getAllStringFilesInDefaultFolder(directory):
	xmlFiles = glob.glob(os.path.join(options.directory, 'res/values/strings*.xml'))	
	return xmlFiles	

if __name__ == '__main__':
	(options, args) = getOptions()
	#Create excel book
	book = initWorkBook()
	#Find all string*.xml in default values directory
	xmlFiles = getAllStringFilesInDefaultFolder(options.directory);
	
	for xmlFile in xmlFiles:
		print xmlFile
			
		#Create a sheet for each string file found in default values directoy		
		sheetName = getNameForSheet(xmlFile)
		sheet = addSheet(book, sheetName)
		
		#Write keys and values from xml default file and write then to sheet
		masterNodeList = getNodeList(xmlFile)
		masterNodeListPlural = getNodeListPlural(xmlFile)
		masterNodeListPluralQuantity = getNodeListPluralQuantity(xmlFile)
		writeMasterNodeList(sheet, masterNodeList, masterNodeListPluralQuantity)
		i=2
		#Search for the other languages xml files
		for xmlLangFile in getStringsXmlFiles(options.directory, getFileName(xmlFile)):
			print xmlLangFile			
			langCode = getLangCode(xmlLangFile)
			nodes = getNodeList(xmlLangFile)
			nodesPlural = getNodeListPluralQuantity(xmlLangFile)			
			writeNodesToColumn(sheet, masterNodeList, masterNodeListPluralQuantity, nodes, nodesPlural, langCode, i)
			i += 1
		rewritePluralKeys(sheet, masterNodeList, masterNodeListPlural)
	saveWorkBook(book, options.output)		
	