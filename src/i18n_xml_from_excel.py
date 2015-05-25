# coding: utf-8
import os
import codecs
import xlrd # Excel library from http://www.python-excel.org/
from optparse import OptionParser

def createAndInitXmlFile(languageCode, stringFileName):
	directory = 'res/values'
	
	if languageCode:
		directory = '%s-%s'%(directory, languageCode)

	if not os.path.exists(directory):
		os.makedirs(directory)
		
	print directory

	xmlFile = codecs.open(directory + '/strings_' + stringFileName, 'w+', encoding='utf-8')
	xmlFile.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n')
	xmlFile.write('<resources>\n')

	return xmlFile

def endAndCloseXmlFile(xmlFile):
	xmlFile.write('</resources>\n')
	xmlFile.close()

def getCleanString(input):
	input = input.replace('\ ', ' ')
	input = input.replace('...', '&#8230;')
	input = input.replace(u'…', '&#8230;')
	input = input.replace('"', '\"')
	input = ' '.join(input.split()) # replaces multiple spaces with a single space	
	# write here any usual replace that you need to perform	
	return input

def getXmlString(key, value):
	if key:
		return '<string name="%s">%s</string>\n'%(key, value)
	else:
		if value:
			print 'WARNING! EMPTY KEY WITH NOT EMPTY VALUE "%s". EXCEL CAN BE BAD FORMATTED'

		return ''
		
def getXmlPlural(key, value):
	valueone = ''
	valueother = ''
	keyplural = cellKey.split(':')
	if cellKey.endswith("one"):
		valueone = '<item quantity="one">%s</item>\n'%(cellValue)
		return '<plurals name="%s">\n'%(keyplural[1]) + valueone						
	if cellKey.endswith("other"):
		valueother = '<item quantity="other">%s</item>\n'%(cellValue)
		return valueother + '</plurals>\n'
	else:
		return ''			
			
def getCellTextValue(row, column):
	cellType = sheet.cell_type(row, column)
	cellValue = sheet.cell_value(row, column)
	
	if cellType in (2,3) and int(cellValue) == cellValue:
		cellValue = int(cellValue)

	return '%s'%(cellValue)

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-f", "--file", help="Input Excel file.", metavar="FILE")
	parser.add_option("-c", "--clean", help="Use this option to clean strings and leave XMLs Android Lint proof.", action="store_true", default=False)

	(options, args) = parser.parse_args()
	
	workbook = xlrd.open_workbook(options.file)
	sheetNames = workbook.sheet_names()
	
	for sheetName in sheetNames:
		sheet = workbook.sheet_by_name(sheetName)
	
		for column in range(1, sheet.ncols):
			xmlFile = createAndInitXmlFile(sheet.cell_value(0, column), sheetName)
			
			for row in range(1, sheet.nrows):
				cellValue = getCellTextValue(row, column)
				cellKey= sheet.cell_value(row, 0)
				if options.clean:
					cellValue = getCleanString(cellValue)					
				
				if cellKey.startswith("plural:"):
					xmlFile.write(getXmlPlural(cellKey, cellValue))					
				else:
					xmlFile.write(getXmlString(cellKey, cellValue))		
		
			endAndCloseXmlFile(xmlFile)
