import os
import os.path
import time
import utils.updater
import myconfig
from progress.bar import Bar
import logging
import multiprocessing
import indexervisitor

def findTestCaseFile(path):
    for dirpath, dirs, files in os.walk(path):
        for file in files:
            fullName = os.path.join(dirpath, file)
            if os.path.splitext(fullName)[1] == '.tc':
                yield fullName

class Indexer(object):
    def __init__(self):
        self.indexerVisitor = indexervisitor.IndexerVisitor()
        self.solr = utils.updater.Updater()
        self.progresser = None

    def indexMyWorkspace(self, workspacePath):
        startTime = time.time()

        myFindTestCaseFile = findTestCaseFile(workspacePath)
        tcFiles = list(myFindTestCaseFile)
        print "Going to index {} test cases in folder {}".format(len(tcFiles), workspacePath)

        self.progresser = Bar('Indexing', max = len(tcFiles))
        for tcFile in tcFiles:
            try:
                self.indexOneTestCase(tcFile)
            except Exception, e:
                logging.error('Fail to index {}'.format(tcFile))
            finally:
                self.progresser.next()

        self.progresser.finish()
        print('Time used: {} seconds'.format(time.time() - startTime))

    def indexOneTestCase(self, testCaseFilePath):
        doc = self.indexerVisitor.generateIndexDocument(testCaseFilePath)
        self.solr.update([doc])

if __name__ == '__main__':
    logging.basicConfig(filename=myconfig.indexerLogFile, format=myconfig.indexerlogFormat, level=myconfig.indexerLogLevel)

    indexer = Indexer()
    for folder in myconfig.indexFolders:
        indexer.indexMyWorkspace(folder)
