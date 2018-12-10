import sys
import InduceC45
import Classify 
import random
import RandomForest


def readTrainingFile(fileName):
   file = open(fileName, "r")
   lines = file.readlines()
   columnNames = lines[0]
   domainSizes = lines[1]
   classLabel = lines[2]
   dataRows = []
   for line in lines[3:]:
      dataRows.append(line)
   file.close()
   return columnNames, domainSizes, classLabel, dataRows  

def randomData(dataRows, n, dataRowsLength):
   j = int(float(dataRowsLength) / n)
   listOfData = []
   for i in range(j):
      if(len(dataRows) > 0):
         rand = random.choice(dataRows)
         listOfData.append(rand)
         dataRows.remove(rand)
   return listOfData, dataRows

def outputRandomDataRowToCSVFileAsHoldout(fileName, columnNames, domainSizes, classLabel, holdoutDataRows):
   f = open(fileName, "w")
   f.write(columnNames)
   f.write(domainSizes)
   f.write(classLabel)
   for holdoutDataRow in holdoutDataRows:
      f.write(holdoutDataRow)
   f.close()

def outputRandomDataRowsToCSVFile(fileName, columnNames, domainSizes, classLabel, listOfRandomDataRows, holdoutRows):
   f = open(fileName, "w")
   f.write(columnNames)
   f.write(domainSizes)
   f.write(classLabel)
   for randomDataRows in listOfRandomDataRows:
      if randomDataRows != holdoutRows:
         for randomDataRow in randomDataRows:
            f.write(randomDataRow)
   f.close()

TEMPORARY_HOLDOUT_CSV_FILE_NAME = "validationsHoldoutTemporaryCSV.csv"
TEMPORARY_CSV_FILE_NAME = "validationsTemporaryCSV.csv"
def performValidation(columnNames, domainSizes, classLabel, dataRows, n, domainXMLFileName, restrictionsFileName, useRandomForest=False):
   totalAccuracy = 0.0
   totalCorrectlyClassifiedRecords = 0.0
   totalClassifiedRecords = 0.0
   listOfRandomDataRows = []
   totalNumberOfTruePositivesForObama = 0
   totalNumberOfTrueNegativesForObama = 0
   totalNumberOfFalsePositivesForObama = 0
   totalNumberOfFalseNegativesForObama = 0
   dataRowsLength = len(dataRows)
   folds = None
   listOfDictOfConfusionMatrices = []
   randomForestAccuracy = None
   if n == -1:
      folds = len(dataRows)
   else:
      folds = n
   for i in range(folds):
      listOfData, dataRows = randomData(dataRows, folds, dataRowsLength)
      listOfRandomDataRows.append(listOfData)
   for randomDataRows in listOfRandomDataRows:
      outputRandomDataRowToCSVFileAsHoldout(TEMPORARY_HOLDOUT_CSV_FILE_NAME, columnNames, domainSizes, classLabel, randomDataRows)
      outputRandomDataRowsToCSVFile(TEMPORARY_CSV_FILE_NAME, columnNames, domainSizes, classLabel, listOfRandomDataRows, randomDataRows)
      if useRandomForest == True:
         accuracy, dictOfConfusionMatrices = RandomForest.runRandomForest(5, 40, 5, TEMPORARY_CSV_FILE_NAME, domainXMLFileName)
         totalAccuracy += accuracy
         listOfDictOfConfusionMatrices.append(dictOfConfusionMatrices)
      else:
         InduceC45.runInduceC45(domainXMLFileName, TEMPORARY_CSV_FILE_NAME, restrictionsFileName)
         accuracy, noOfRecordsClassified, noOfRecordsCorrectlyClassified, noOfRecordsIncorrectlyClassified, errorRate, numberOfTruePositivesForObama, numberOfTrueNegativesForObama, numberOfFalsePositivesForObama, numberOfFalseNegativesForObama = Classify.runClassify(TEMPORARY_CSV_FILE_NAME, TEMPORARY_CSV_FILE_NAME.split(".csv")[0] + "Tree.xml", "output.txt")
         totalAccuracy += accuracy
         totalCorrectlyClassifiedRecords += noOfRecordsCorrectlyClassified
         totalClassifiedRecords += noOfRecordsClassified
         totalNumberOfTruePositivesForObama += numberOfTruePositivesForObama
         totalNumberOfTrueNegativesForObama += numberOfTrueNegativesForObama
         totalNumberOfFalsePositivesForObama += numberOfFalsePositivesForObama
         totalNumberOfFalseNegativesForObama += numberOfFalseNegativesForObama
   if useRandomForest == True:
      print "-----------------"
      for index, dictOfConfusionMatrices in enumerate(listOfDictOfConfusionMatrices):
         print "For run number " + str(index)
         for categoryName, confusionMatrix in dictOfConfusionMatrices.iteritems():
            print "Confusion Matrix for " + categoryName
            print "True Positives: " + str(confusionMatrix["TP"])
            print "True Negatives: " + str(confusionMatrix["TN"])
            print "False Positives: " + str(confusionMatrix["FP"])
            print "False Negatives: " + str(confusionMatrix["FN"])
            print "\n"
      print "Average accuracy : " + str(float(totalAccuracy) / folds)
      print "-----------------"
   else:
      precision = float(totalNumberOfTruePositivesForObama)/(totalNumberOfTruePositivesForObama + totalNumberOfFalsePositivesForObama)
      recall = float(totalNumberOfTruePositivesForObama)/(totalNumberOfTruePositivesForObama + totalNumberOfFalseNegativesForObama)
      pf = float(totalNumberOfFalsePositivesForObama)/(totalNumberOfFalsePositivesForObama + totalNumberOfTrueNegativesForObama)
      fMeasure = ((2.0 * precision * recall)/(precision + recall))
      print "-----------------"
      # print "Confusion Matrix: "
      # print "True Positives: " + str(totalNumberOfTruePositivesForObama)
      # print "True Negatives: " + str(totalNumberOfTrueNegativesForObama)
      # print "False Positives: " + str(totalNumberOfFalsePositivesForObama)
      # print "False Negatives: " + str(totalNumberOfFalseNegativesForObama)
      # print "\n" 
      # print "Precision : " + str(precision)
      # print "Recall : " + str(recall)
      # print "PF     : " + str(pf)
      # print "F-Measure : " + str(fMeasure)
      print "Average Accuracy : " + str(float(totalAccuracy) / folds)
      print "Overall Accuracy : " + str(float(totalCorrectlyClassifiedRecords)/ totalClassifiedRecords)
      print "-----------------"

def runEvaluate(trainingSetFileName, domainXMLFileName, n, restrictionsFileName, useRandomForest):
   columnNames, domainSizes, classLabel, dataRows = readTrainingFile(trainingSetFileName)
   performValidation(columnNames, domainSizes, classLabel, dataRows, n, domainXMLFileName, restrictionsFileName, useRandomForest)


