#!/usr/bin/python
'''
Created on Feb 15, 2013

@author: xwang95
'''
import sys;
import theme_discovery.citation_based_method;
import theme_discovery.content_based_method;
import toolkit.utility;
import toolkit.bcolor;

if __name__ == '__main__':
    if(len(sys.argv) > 1 and sys.argv[1] == '--citation_lda_summary'):
        theme_discovery.citation_based_method.pubmedCitationLdaSummary(sys.argv[2]);
    elif(len(sys.argv) > 1 and sys.argv[1] == '--citation_lda_short_summary'):
        theme_discovery.citation_based_method.pubmedCitationLdaShortSummary(sys.argv[2]);
    elif(len(sys.argv) > 1 and sys.argv[1] == '--citation_lda_run'):
        K = toolkit.utility.parseNumVal(sys.argv[2]);
        burninHr = toolkit.utility.parseNumVal(sys.argv[3]);
        sampliHr = toolkit.utility.parseNumVal(sys.argv[4]);
        theme_discovery.citation_based_method.pubmedCitationLdaRun(K, burninHr, sampliHr);
    elif(len(sys.argv) > 1 and sys.argv[1] == '--content_lda_run'):
        topicNum = toolkit.utility.parseNumVal(sys.argv[2]);
        burninHr = toolkit.utility.parseNumVal(sys.argv[3]);
        sampliHr = toolkit.utility.parseNumVal(sys.argv[4]);
        contentField = sys.argv[5].strip();
        theme_discovery.content_based_method.pubmedContentLdaRun(topicNum, burninHr, sampliHr, contentField=contentField);
    elif(len(sys.argv) > 1 and sys.argv[1] == '--content_lda_summary'):
        theme_discovery.content_based_method.pubmedContentLdaSummary(sys.argv[2]);
    elif(len(sys.argv) > 1 and sys.argv[1] == '--citation_lda_citation_matrix'):
        ldaFilePath = sys.argv[2].strip();
        theme_discovery.citation_based_method.pubmedCitationMatrix(ldaFilePath);
    elif(len(sys.argv) > 1 and sys.argv[1] == '--citation_lda_time_sorted_matrix'):
        citMatrixFilePath = sys.argv[2].strip();
        topicSummaryFilePath = sys.argv[3].strip();
        theme_discovery.citation_based_method.pubmedTimeSortedCitationMatrix(citMatrixFilePath, topicSummaryFilePath);
    elif(len(sys.argv) > 1 and sys.argv[1] == '--citation_lda_time_sorted_short_summary'):
        topicSummaryFilePath = sys.argv[2].strip();
        theme_discovery.citation_based_method.pubmedTimeSortedShortTopicSummary(topicSummaryFilePath);
    else:
        print('[run] argument error');
        print('[run] --usage:');
        print(toolkit.bcolor.toString("             [1]: --citation_lda_summary  [ldaFilePath]", 'warning'));
        print(toolkit.bcolor.toString("             [2]: --citation_lda_short_summary  [ldaFilePath]", 'warning'));
        print(toolkit.bcolor.toString("             [3]: --citation_lda_run  [topicNum]  [burninHr]  [sampliHr]", 'warning'));
        print(toolkit.bcolor.toString("             [4]: --content_lda_run  [topicNum]  [burninHr]  [sampliHr]  [contentField]", 'warning'));
        print(toolkit.bcolor.toString("             [5]: --citation_lda_citation_matrix  [ldaFilePath]", 'warning'));
        print(toolkit.bcolor.toString("             [6]: --citation_lda_time_sorted_matrix  [citMatrixFilePath]  [topicSummaryFilePath]", 'warning'));
        print(toolkit.bcolor.toString("             [7]: --citation_lda_time_sorted_short_summary  [topicSummaryFilePath]", 'warning'));
        print(toolkit.bcolor.toString("             [8]: --content_lda_summary  [ldaFilePath]", 'warning'));
