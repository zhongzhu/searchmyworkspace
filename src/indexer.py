import os
import os.path
import time

def findTestCaseFile(path):
    for dirpath, dirs, files in os.walk(path):
        for file in files:
            fullName = os.path.join(dirpath, file)
            if os.path.splitext(fullName)[1] == '.tc':
                yield fullName

class Indexer(object):
    def __init__(self):
        pass

    def indexMyWorkspace(self, workspacePath):
        startTime = time.time()
        myFindTestCaseFile = findTestCaseFile(workspacePath)
        tcFiles = list(myFindTestCaseFile)
        print time.time() - startTime, "seconds"
        print "found {} results".format(len(tcFiles))
        for tcFile in tcFiles:
            self.indexOneTestCase(tcFile)

    def indexOneTestCase(self, testCaseFilePath):
        print(testCaseFilePath)

if __name__ == '__main__':
    indexer = Indexer()
    indexer.indexMyWorkspace('D:\EasyTest\workspace')