import logging

indexerLogFile = 'indexer.log'
indexerlogFormat = '%(asctime)s - %(levelname)s - %(message)s'
indexerLogLevel = logging.WARNING
indexWorkerNumber = 4

indexFolders = ['D:\\Repository\\R_2_10_0\\doc\\examples']
solrURL = 'http://localhost:8983/solr/myworkspace'
