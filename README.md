# Transdroider

A couple of **Python** scripts: 
i18n_excel_from_xml: creats an **MS Excel** book from every strings.xml file in your Android project. In case of having more than one strings file in your project they have to be named strings\*.xml for the script to recognize them. 
i18n_xml_from_excel: Creates all the res/values-xx structure and strings.xml (or strings\*.xml) files from an MS Excel book. For those not using **xliff** or **gettext**...

## Excel from XML (i18n_excel_from_xml.py)

Builds an MS Excel sheet with all the strings defined in every strings.xml file from an Android project separated in columns.

Excel created will contain as many sheets as strings\*.xml files there are in the project following the following structure

```text
------------------------------------------------
|  keys   |  lang_code_1  |  lang_code_2  |  ...
------------------------------------------------
|  key_1  |  translation  |  translation  |  ...
------------------------------------------------
|  key_2  |  translation  |  translation  |  ...
     .            .               .
     .            .               .
     .            .               .
```
An example Excel file could look like:

```text
---------------------------------------------------------
|     keys      |       en       |      es-rES     |  ...
---------------------------------------------------------
|  hello_world  |  Hello world!  |  ¡Hola, mundo!  |  ...
---------------------------------------------------------
|   good_bye    |    Good bye    |      Adiós      |  ...
        .                .                .
        .                .                .
        .                .                .
```

In case of having a plural of the form:

```text
<plurals name="example_day">
	<item quantity="one">1 day</item>
	<item quantity="other">%1$d days</item>
</plurals>
```
The script produces two rows in the sheet:

```text
--------------------------------------------------------------------
|         	keys			 |  lang_code_1  |  lang_code_2  |  ...
--------------------------------------------------------------------
|  plural:example_day:one    |  translation  |  translation  |  ...
--------------------------------------------------------------------
|  plural:example_day:other  |  translation  |  translation  |  ...
```
**NOTE:** The script only takes plurals that have items **one** and **other** 

### Usage

`python i18n_excel_from_xml.py -d <android_project_root_directory> -o <output_excel_file_name>`

## XML from Excel (i18n_xml_from_excel.py)

Create full directory structure (also lang code suffix) and localised strings.xml files (or strings*.xml files) for an Android project from an MS Excel file.

Excel file must contain as many sheets as strings\*.xml files you need per each language (each sheet also named strings\*.xml) with strings following the next structure:

```text
------------------------------------------------
|   keys  |  lang_code_1  |  lang_code_2  |  ...
------------------------------------------------
|  key_1  |  translation  |  translation  |  ...
------------------------------------------------
|  key_2  |  translation  |  translation  |  ...
     .            .               .
     .            .               .
     .            .               .
```	 
In the case of having a plural:

```text
--------------------------------------------------------------------
|         	keys			|  lang_code_1  |  lang_code_2  |  ...
--------------------------------------------------------------------
|  plural:key_plural:one    |  translation  |  translation  |  ...
--------------------------------------------------------------------
|  plural:key_plural:other  |  translation  |  translation  |  ...
```
	 
An example Excel file could look like:
```text
----------------------------------------------------------------
|        keys      	  |       en       |      es-rES     |  ...
----------------------------------------------------------------
|     hello_world  	  |  Hello world!  |  ¡Hola, mundo!  |  ...
----------------------------------------------------------------
|      good_bye    	  |    Good bye    |      Adiós      |  ...
----------------------------------------------------------------
|   plural:days:one   |     1 day  	   |  	  1 día	     |  ...
----------------------------------------------------------------
|  plural:days:other  |   %1$d days    |    %1$d días    |  ...
        .                .                .
        .                .                .
        .                .                .
```
		
### Usage

'python i18n_xml_from_excel.py -f <input_excel_file> [-c]'

- option **-c**. If used, strings will be 'cleaned' before writing them to the XML file. See function getCleanString in code for further info.

## Dependencies

* Python 2.7.2 (older versions not tested)
* `xlwt` and `xlrd` from Excel library, found at http://www.python-excel.org/
* Modules used: `optparse`, `codecs`, `os`, `glob`, `xml.dom.minidom`

## Developed by

Miguel Barrios - mbarrben@gmail.com
Elena Martínez - emlmartlopez@gmail.com (last changes)

## License

```text
Copyright 2013 Miguel Barrios

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
