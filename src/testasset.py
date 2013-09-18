from PySide import QtCore
from PySide import QtGui
from highlighter import TestCaseHighlighter

class TestAssetType(object):
    NONE = 0
    TESTCASE = 100
    SERVICE = 101
    LANGUAGE_REFERENCE = 102

class TestAsset(object):
    def __init__(self, fileLocation):
        self.fileLocation = fileLocation

    def getFileLocation(self):
        return self.fileLocation

    def getTestAssetType(self):
        return TestAssetType.NONE

    def getFileContent(self):
        pass

    def prepareContent(self):
        pass

    def setSyntaxHighlighter(self, document):
        pass        

class TestCase(TestAsset):
    def __init__(self, fileLocation):
        super(TestCase, self).__init__(fileLocation)

    def getTestAssetType(self):
        return TestAssetType.TESTCASE     

    def setSyntaxHighlighter(self, document):
        TestCaseHighlighter(document)          

    def getFileContent(self):
        return """
Testcase General Information
TC_ID tc001
QC_ID qc001
Title put title here
Author your name
Created 2011-03-01
Purpose Put the test case purpose here
Usage Put the test case usage here
function:: switch_case_default
  switch_case_default:description
    
  switch_case_default:arguments

  switch_case_default:variables
    int i
    string switchstr
    int switchi
    TMap map
    TArray arr
    string result
    string str
    TMap switchmap
    TArray switcharr
  switch_case_default:responseMapping

  switch_case_default:steps
    eval $i=1
    eval $str="string"
    eval $map["key"]="TMap"
    eval $arr<<"TArray"
    comment ****** switch int type variable ******
      eval $switchi=1
      switch $switchi
        case 0
          eval $result="0"
          break 
        case $i
          eval $result="1"
          break 
        case "str"
          eval $result="str"
          break 
        case $str
          eval $result="string"
          break 
        case $map["key"]
          eval $result="TMap"
          break 
        case $arr[0]
          eval $result="TArray"
          break 
        case start$i$str$map["key"]$arr[0]end
          eval $result="start1stringTMapTArrayend"
          break 
        default 
          eval $result+="default"
      print $result
      if $result!="1"
        failCase 
    comment ****** switch string type variable ******
      eval $switchstr="string"
      switch $switchstr
        case 0
          eval $result="0"
          break 
        case $i
          eval $result="1"
          break 
        case "str"
          eval $result="str"
          break 
        case $str
          eval $result="string"
          break 
        case $map["key"]
          eval $result="TMap"
          break 
        case $arr[0]
          eval $result="TArray"
          break 
        case start$i$str$map["key"]$arr[0]end
          eval $result="start1stringTMapTArrayend"
          break 
        default 
          eval $result+="default"
      print $result
      if $result!="string"
        failCase 
    comment ****** switch TMap type variable ******
      eval $switchmap["key"]="TMap"
      switch $switchmap["key"]
        case 0
          eval $result="0"
          break 
        case $i
          eval $result="1"
          break 
        case "str"
          eval $result="str"
          break 
        case $str
          eval $result="string"
          break 
        case $map["key"]
          eval $result="TMap"
          break 
        case $arr[0]
          eval $result="TArray"
          break 
        case start$i$str$map["key"]$arr[0]end
          eval $result="start1stringTMapTArrayend"
          break 
        default 
          eval $result+="default"
      print $result
      if $result!="TMap"
        failCase 
    comment ****** switch TArray type variable ******
      eval $switcharr<<"TArray"
      switch $switcharr[0]
        case 0
          eval $result="0"
          break 
        case $i
          eval $result="1"
          break 
        case "str"
          eval $result="str"
          break 
        case $str
          eval $result="string"
          break 
        case $map["key"]
          eval $result="TMap"
          break 
        case $arr[0]
          eval $result="TArray"
          break 
        case start$i$str$map["key"]$arr[0]end
          eval $result="start1stringTMapTArrayend"
          break 
        default 
          eval $result+="default"
      print $result
      if $result!="TArray"
        failCase 
    comment ****** switch mixture type variables ******
      switch start$switchi$switchstr$switchmap["key"]$switcharr[0]end
        case 0
          eval $result="0"
          break 
        case $i
          eval $result="1"
          break 
        case "str"
          eval $result="str"
          break 
        case $str
          eval $result="string"
          break 
        case $map["key"]
          eval $result="TMap"
          break 
        case $arr[0]
          eval $result="TArray"
          break 
        case start$i$str$map["key"]$arr[0]end
          eval $result="start1stringTMapTArrayend"
          break 
        default 
          eval $result+="default"
      print $result
      if $result!="start1stringTMapTArrayend"
        failCase 
    comment ****** switch with no break in cases ******
      switch start$switchi$switchstr$switchmap["key"]$switcharr[0]end
        case 0
          eval $result="0"
        case $i
          eval $result="1"
        case "str"
          eval $result="str"
        case $str
          eval $result="string"
        case $map["key"]
          eval $result="TMap"
        case $arr[0]
          eval $result="TArray"
        case start$i$str$map["key"]$arr[0]end
          eval $result="start1stringTMapTArrayend"
        default 
          eval $result+="default"
      print $result
      if $result!="start1stringTMapTArrayenddefault"
        failCase 
    comment ****** switch with some cases using one body ******
      switch start$switchi$switchstr$switchmap["key"]$switcharr[0]end
        case 0
        case $i
        case "str"
        case $str
        case $map["key"]
        case $arr[0]
        case start$i$str$map["key"]$arr[0]end
          eval $result="start1stringTMapTArrayend"
          break 
        default 
          eval $result+="default"
      print $result
      if $result!="start1stringTMapTArrayend"
        failCase        
        """                  