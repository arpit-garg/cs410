#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import numpy as np
import re
import pandas as pd
import csv
import json
from corpus.pubmed import getPubMedCorpus, getCitMetaGraphPmidIdMapping, readMetaFile
from toolkit import variables;


def computeTopicDetails(topicNumber, phiMatrix, idToPmid, metaFileDict):
    topicDocumentCitations = phiMatrix[topicNumber - 1, :]
    years = dict()
    milestonePapers = dict()
    for index in range(len(topicDocumentCitations)):
        phiVal = topicDocumentCitations[index]
        pubMedId = idToPmid[index]
        currentDocumentMetaData = metaFileDict[pubMedId]
        publishedYear = currentDocumentMetaData['year']
        if (publishedYear in years):
            years[publishedYear] += phiVal
        else:
            years[publishedYear] = phiVal

        milestonePapers[phiVal] = currentDocumentMetaData

    return years, milestonePapers


def writeTopicDetailsToJson(K, phiMatrix, idToPmid, metaFileDict):
    topicTemporalStrengthJson = []
    topicRelevantDocumentsJson = []

    for i in range(K):
        temporalStrength, relevantDocuments = computeTopicDetails(i, phiMatrix, idToPmid, metaFileDict)
        topicTemporalStrength = dict()
        topicTemporalStrength['timeline'] = sorted(temporalStrength.keys())
        topicTemporalStrength['temporalStrength'] = [temporalStrength[key] for key in topicTemporalStrength['timeline']]
        topicTemporalStrengthJson.append(topicTemporalStrength)

        topicRelevantDocuments = []
        for key in sorted(relevantDocuments.keys()):
            topicRelevantDocuments.append(relevantDocuments[key])
            if (len(topicRelevantDocuments) == 10):
                break

        topicRelevantDocumentsJson.append(topicRelevantDocuments)

    topicTemporalStrengthJson = json.dumps(topicTemporalStrengthJson)
    topicRelevantDocumentsJson = json.dumps(topicRelevantDocumentsJson)

    with open('topicTemporalStrength.json', 'w') as f1, open('topicRelevantDocuments.json', 'w') as f2:
        f1.write(topicTemporalStrengthJson)
        f2.write(topicRelevantDocumentsJson)


# Parse the generated LDA summary file and return the final theta(document_to_topic distribution) and phi(topic_to_document distribution) dstributions
def parseLdaFile(D, K, ldaSummaryFilePath):
    thetaMatrixFound = False
    phiMatrixFound = False
    # Matrix of document-topic distribution Theta
    thetaMatrix = np.empty(shape=(D, K))
    # Matrix of topic-document distribution Phi
    phiMatrix = np.empty(shape=(K, D))
    counta = 0
    countb = 0
    with open(ldaSummaryFilePath) as ldaFile:
        for line in ldaFile:
            try:
                if line.startswith('theta'):
                    thetaMatrixFound = True
                elif line.startswith('phi'):
                    thetaMatrixFound = False
                    phiMatrixFound = True
                elif line.startswith('topic_weight'):
                    phiMatrixFound = False
                elif thetaMatrixFound == True:
                    row = [float(val) for val in line.split(' ')]
                    thetaMatrix[counta] = row
                    counta = counta + 1
                elif phiMatrixFound == True:
                    row = [float(val) for val in line.split(' ')]
                    phiMatrix[countb] = row
                    countb = countb + 1
            except ValueError, e:
                print("error %s on line" % (e, counta))
                break

    return thetaMatrix, phiMatrix


def populateDependencyGraph(thetaMatrix, phiMatrix, threshold=0.04):
    weightedTopicDependencyGraph = np.dot(phiMatrix, thetaMatrix)
    topicDependencyGraph = np.empty(shape=(500, 500))
    count = 0
    for i in range(0, 500):
        for j in range(0, 500):
            if weightedTopicDependencyGraph[i][j] >= threshold:
                topicDependencyGraph[i][j] = 1
                count += 1
            else:
                topicDependencyGraph[i][j] = 0
    print('Total number of dependencies %d' % (count))
    return topicDependencyGraph


def writeGraphToJson(topicDependencyGraph, idToPmid, metaFileDict):
    topicDependencyDict = dict()
    timeSortedSummaryFile = '/Users/Garima/Documents/workspace/citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda_summary_timeSorted_shortSummary'
    with open(timeSortedSummaryFile) as f:
        for count, line in enumerate(f):
            topicDependencyDict[count] = line.split("\t")
            topicKeywords = topicDependencyDict[count][3]
            weight = topicDependencyDict[count][2].split()[0]
            year = topicDependencyDict[count][2].split()[1].split('(')[0]
            std = topicDependencyDict[count][2].split()[1].split('(')[1]
            topicDependencyDict[count][2] = weight
            topicDependencyDict[count][3] = year
            topicDependencyDict[count].append("https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation")
            topicDependencyDict[count].append(std)
            topicDependencyDict[count].append(topicKeywords)

    for i in range(0, len(topicDependencyDict)):
        topicDependencyDict[i][0] = re.sub('[\D+]', '', topicDependencyDict[i][0])
        topicDependencyDict[i][0] = int(topicDependencyDict[i][0])

        topicDependencyDict[i][1] = re.sub('[\D+]', '', topicDependencyDict[i][1])
        topicDependencyDict[i][1] = int(topicDependencyDict[i][1])

        topicDependencyDict[i][3] = re.sub('[a-zA-Z=]', '', topicDependencyDict[i][3])
        topicDependencyDict[i][3] = int(float(topicDependencyDict[i][3]))

        topicDependencyDict[i][4] = topicDependencyDict[i][4].strip(')')
        topicDependencyDict[i][5] = topicDependencyDict[i][5].strip('\n')

    df = pd.DataFrame.from_dict(topicDependencyDict, orient='index')
    df.columns = ['timeSort', 'topic', 'weight', 'year', 'topicMilestonePaperLink', 'std', 'topicTitle']
    # df.columns = ['timeSort', 'topic', 'year', 'topicMilestonePaperLink']

    influencedBy = {}
    for i in range(0, 500):
        currentInfluencedByList = []
        for j in range(0, 500):
            if topicDependencyGraph[i][j] == 1 and i != j:
                currentInfluencedByList.append(j)
        influencedBy[i] = currentInfluencedByList
    df['influencedBy'] = np.array
    for i in range(500):
        # df.loc[df.topic == i, 'influencedBy'] = influencedBy[i]
        df.set_value(df.topic[df.topic == i].index[0], 'influencedBy', influencedBy[i])

    # df['influencedBy'] = pd.Series(influencedBy)
    df = df.drop(['weight', 'std', 'topicTitle'], axis=1)
    # df.timeSort = df.timeSort.astype(np.int64)
    # df.topic = df.topic.astype(np.int64)
    # df.year = df.year.astype(np.int64)

    dfjson = df.to_json(orient="records")
    f = open("topics.json", "w")
    f.write(dfjson)
    f.close()


if __name__ == '__main__':
    pmd = getPubMedCorpus();
    (pmidToId, idToPmid) = getCitMetaGraphPmidIdMapping(pmd);
    D = len(pmidToId)
    K = 500
    # ldaSummaryFilePath = '/Users/arpitgarg/Documents/UIUC/MSIM/spring17/cs410/Project/sifaka.cs.uiuc.edu/~xwang95/citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda'
    ldaSummaryFilePath = '/Users/Garima/Documents/workspace/citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda'
    thetaMatrix, phiMatrix = parseLdaFile(D, K, ldaSummaryFilePath)

    metaDataFilePath = os.path.join(variables.DATA_DIR, 'PubMed/pubmed_metadata.txt');
    metaFileDict = readMetaFile(metaDataFilePath)
    # metaFileDict = readMetaFile(
        # "/Users/arpitgarg/Documents/UIUC/MSIM/spring17/cs410/Project/timan102.cs.illinois.edu/~xwang95/data/PubMed/pubmed_metadata.txt")

    # temporalStrength, relevantPapers = computeTopicDetails(8, phiMatrix, idToPmid, metaFileDict)
    # print(temporalStrength)

    topicDependencyGraph = populateDependencyGraph(thetaMatrix, phiMatrix)
    writeGraphToJson(topicDependencyGraph, idToPmid, metaFileDict)
    # writeTopicDetailsToJson(K, phiMatrix, idToPmid, metaFileDict)
