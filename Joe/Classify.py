import sys
import xml.etree.ElementTree

def parseXMLTreeFile(fileName):
   return xml.etree.ElementTree.parse(fileName).getroot()

def classifyDataRow(row, columnNames, T):
   if T.find("decision") != None:
      decisionNode = T.find("decision")
      return decisionNode.get("choice"), decisionNode.get("end")   
   else:
      node = T.find("node") 
      for index, columnName in enumerate(columnNames):
         if columnName == node.get("var"): 
            for edge in node:
               if ">=" in edge.get("var") or "<" in edge.get("var"):
                  greaterThanRule = True
                  if "<" in edge.get("var"): 
                     greaterThanRule = False
                  rowValue = row[index]
                  if greaterThanRule == True:
                     if rowValue >= float(edge.get("var").split(">= ")[1]):
                        return classifyDataRow(row, columnNames, edge)
                  else:
                     if rowValue < float(edge.get("var").split("< ")[1]):
                        return classifyDataRow(row, columnNames, edge)
              
               if edge.get("num") == str(row[index]):
                  return classifyDataRow(row, columnNames, edge)

def classifyCSVFile(fileName, T, outputFileName):
   csvFile = open(fileName, "r")
   outputFile = open(outputFileName, "w")
   hasClass = False
   csvFileLines = csvFile.readlines()
   columnNames = csvFileLines[0].strip().split(",")
   dataRows = []
   if len(csvFileLines[2].strip().split(",")) == 1:
      hasClass = True
   for line in csvFileLines[3:]:
      tokens = line.strip().split(",")
      if "." in tokens[0]:
         dataRows.append([float(x) for x in tokens])
      else:
         dataRows.append([int(x) for x in tokens])
   classifications = []
   noOfErrors = 0
   numberOfFalseNegativesForObama = 0
   numberOfFalsePositivesForObama = 0
   numberOfTruePositivesForObama = 0
   numberOfTrueNegativesForObama = 0
   for dataRow in dataRows:
      classification = classifyDataRow(dataRow, columnNames, T)
      if classification == None:
         classification = '1001-1200', '1'
      print "Row: " + str(dataRow) + " Prediction: " + str(classification)
      outputFile.write("Row: " + str(dataRow) + " Prediction: " + str(classification) + "\n")
      classifications.append(classification)
      #print classification
      #print dataRow
      if int(classification[1]) != dataRow[len(dataRow) - 1]:
         noOfErrors += 1
         actualValue = dataRow[len(dataRow) - 1]
         predictedValue = int(classification[1])
         if actualValue == 1:
            #1 is Obama
            #we are predicting negative here
            numberOfFalseNegativesForObama += 1
         else:
            numberOfFalsePositivesForObama += 1     
      else:
         actualValue = int(classification[1])
         if actualValue == 1:
            #1 is Obama
            numberOfTruePositivesForObama += 1
         else: 
            numberOfTrueNegativesForObama += 1
      
   if hasClass:
   	accuracy = (float(len(classifications) - noOfErrors))/len(classifications)
   	print "Total number of records classified: " + str(len(classifications))
   	print "Total number of records correctly classified: " + str(len(classifications) - noOfErrors)
   	print "Total number of records incorrectly classified: " + str(noOfErrors)
   	print "Classifier Accuracy: " + str(accuracy)
   	print "Classifier Error Rate: " + str(1 - accuracy)
   csvFile.close()
   outputFile.close()
   #returns accuracy, no of records classified, no of records correctly classified, no of records incorrectly classified, error rate
   return accuracy, len(classifications), (len(classifications) - noOfErrors), (noOfErrors), (1 - accuracy), numberOfTruePositivesForObama, numberOfTrueNegativesForObama, numberOfFalsePositivesForObama, numberOfFalseNegativesForObama



def runClassify(csvFileName, treeXMLFileName, outputFileName):
   T = parseXMLTreeFile(treeXMLFileName)
   accuracy, noOfRecordsClassified, noOfRecordsCorrectlyClassified, noOfRecordsIncorrectlyClassified, errorRate, numberOfTruePositivesForObama, numberOfTrueNegativesForObama, numberOfFalsePositivesForObama, numberOfFalseNegativesForObama = classifyCSVFile(csvFileName, T, outputFileName)
   return accuracy, noOfRecordsClassified, noOfRecordsCorrectlyClassified, noOfRecordsIncorrectlyClassified, errorRate, numberOfTruePositivesForObama, numberOfTrueNegativesForObama, numberOfFalsePositivesForObama, numberOfFalseNegativesForObama
