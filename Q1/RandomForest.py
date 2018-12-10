import sys
#import Validation
import InduceC45
import random
import utilities
import Classify

def readCsvFile(fileName):
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

def outputRandomDataRowsToCsvFile(fileName, columnNames, domainSizes, classLabel, randomDataRows):
   f = open(fileName, "w")
   f.write(columnNames)
   f.write(domainSizes)
   f.write(classLabel)
   for randomDataRow in randomDataRows:
      f.write(randomDataRow)
   f.close()

def getRandomDataRows(dataRows, numOfDataPoints_k):
   listOfData = []
   for i in range(numOfDataPoints_k):
      rand = random.choice(dataRows)
      listOfData.append(rand)
   return listOfData

def getClassLabelIndex(columnNames, classLabel):
   for index, columnName in enumerate(columnNames):
      if columnName.strip() == classLabel.strip():
         return index

def createRestrictionsFile(restrictionsFileName, numOfAttributes_m, columnNames, classLabel):
   restrictionsFile = open(restrictionsFileName, "w")
   hasIdColumn = False
   if columnNames[0] == "Id":
      hasIdColumn = True
   noOfColumns = len(columnNames)
   indexesToInclude = [getClassLabelIndex(columnNames, classLabel)]
   if numOfAttributes_m > noOfColumns:
      raise Exception('Num of attributes greater than number of attributes in data')
   if hasIdColumn == True and numOfAttributes_m > (noOfColumns - 1):
      raise Exception('Num of attributes greater than number of attributes in data')
   lowerLimit = 0
   if hasIdColumn == True:
      lowerLimit = 1
   for i in range(numOfAttributes_m):
      randomIndex = random.randint(lowerLimit, noOfColumns-1)
      while randomIndex in indexesToInclude:
         randomIndex = random.randint(lowerLimit, noOfColumns-1)
      indexesToInclude.append(randomIndex)
   vectorString = ""
   for i in range(0, noOfColumns):
      if i in indexesToInclude:
         vectorString += "1"
      elif i == 0 and hasIdColumn == True:
         vectorString += "1"
      else:
         vectorString += "0"
      
      if i < noOfColumns-1:
         vectorString += ","
   restrictionsFile.write(vectorString + "\n")
   restrictionsFile.close()

def getPluralityPrediction(predictionsFromAllTrees, indexOfDataRowToLookAt):
   if len(predictionsFromAllTrees) <= 0:
      raise Exception("len of predictionsFromAllTrees cannot be <= 0")
   predictionCounts = {}
   for predictionsFromTree in predictionsFromAllTrees:
       utilities.addCountInDictionaryForKey(predictionCounts, predictionsFromTree[indexOfDataRowToLookAt])
   maxPrediction = None
   maxPredictionCount = None
   for prediction, predictionCount in predictionCounts.iteritems():   
      if maxPrediction == None:
         maxPrediction = prediction
         maxPredictionCount = predictionCount
      elif predictionCount > maxPredictionCount:
         maxPrediction = prediction
         maxPredictionCount = predictionCount
   return maxPrediction

def randomForest(numOfAttributes_m, numOfDataPoints_k, numOfTrees_N, csvFilePath, domainFilePath):
   columnNames, domainSizes, classLabel, dataRows = readCsvFile(csvFilePath)
   classLabelIndex = getClassLabelIndex(columnNames.strip().split(","), classLabel)
   A, continuousVariablesDict = InduceC45.parseXML(domainFilePath)
   treeFileNames = []
   classifiedRowsFileNames = []
   print A["categories"][classLabel.strip()]
   dictOfConfusionMatrices = {}
   for categoryObject in A["categories"][classLabel.strip()]:
      dictOfConfusionMatrices[categoryObject["name"]] = {}
      dictOfConfusionMatrices[categoryObject["name"]]["TP"] = 0
      dictOfConfusionMatrices[categoryObject["name"]]["FP"] = 0
      dictOfConfusionMatrices[categoryObject["name"]]["TN"] = 0
      dictOfConfusionMatrices[categoryObject["name"]]["FN"] = 0
   for i in range(numOfTrees_N):
      randomDataRows = getRandomDataRows(dataRows, numOfDataPoints_k)
      randomDataRowsOutputCsvFileName = "temporaryRandomForest" + str(i) + ".csv"
      outputRandomDataRowsToCsvFile(randomDataRowsOutputCsvFileName, columnNames, domainSizes, classLabel, randomDataRows)
      treeFileNames.append("temporaryRandomForest" + str(i) + "Tree.xml") 
      restrictionsFileName = "temporaryRandomForestRestrictionsFile" + str(i) + ".csv"
      createRestrictionsFile(restrictionsFileName, numOfAttributes_m, columnNames.strip().split(','), classLabel)
      InduceC45.runInduceC45(domainFilePath, randomDataRowsOutputCsvFileName, restrictionsFileName)
   for i, treeFileName in enumerate(treeFileNames):
      classifiedRowsFileName = treeFileName.split(".xml")[0] + "Classified.txt"
      Classify.runClassify(csvFilePath, treeFileName, classifiedRowsFileName)
      classifiedRowsFileNames.append(classifiedRowsFileName)
   
   
   predictionsFromAllTrees = []
   for classifiedRowsFileName in classifiedRowsFileNames:
      predictionsFromCurrentTree = []
      classifiedRowsFile = open(classifiedRowsFileName, "r")
      lines = classifiedRowsFile.readlines()
      for line in lines:
         predictionsFromCurrentTree.append(int(line.strip().split("Prediction")[1].split(",")[1].split("\'")[1])) #get the prediction number
      classifiedRowsFile.close()
      predictionsFromAllTrees.append(predictionsFromCurrentTree)
   
   noOfErrors = 0
   noOfDataRows = len(dataRows)
   for index, dataRow in enumerate(dataRows):  
      pluralityPrediction = int(getPluralityPrediction(predictionsFromAllTrees, index))
      print "Row: " + str(dataRow.strip()) + "      Random Forest Prediction: " + str(pluralityPrediction)
      #if int(dataRow[classLabelIndex].strip()) != pluralityPrediction
      dataRowTokens = dataRow.strip().split(",")
      actualClassLabel = int(dataRowTokens[classLabelIndex])
      #print str(pluralityPrediction) + " " + str(actualClassLabel)
      if pluralityPrediction != actualClassLabel:
         actualClassLabelCategoryName = A["categories"][classLabel.strip()][actualClassLabel-1]["name"]
         predictedCategoryName = A["categories"][classLabel.strip()][pluralityPrediction-1]["name"]
         #wrong prediction, so add a false negative to actual class label and a false positive to the prediction
         dictOfConfusionMatrices[actualClassLabelCategoryName]["FN"] += 1
         dictOfConfusionMatrices[predictedCategoryName]["FP"] += 1
        
         #add true negative to everything else
         for categoryName, confusionMatrix in dictOfConfusionMatrices.iteritems():
            if categoryName != actualClassLabelCategoryName or categoryName != predictedCategoryName:
               confusionMatrix["TN"] += 1
         noOfErrors += 1
      else:
         actualClassLabelCategoryName = A["categories"][classLabel.strip()][actualClassLabel-1]["name"]
         dictOfConfusionMatrices[actualClassLabelCategoryName]["TP"] += 1
         
         #add true negative to everything else
         for categoryName, confusionMatrix in dictOfConfusionMatrices.iteritems():
            if categoryName != actualClassLabelCategoryName:
               confusionMatrix["TN"] += 1
         
   accuracy = (float(noOfDataRows - noOfErrors))/noOfDataRows
   print "Total number of records classified: " + str(noOfDataRows)
   print "Total number of records correctly classified: " + str(noOfDataRows - noOfErrors)
   print "Total number of records incorrectly classified: " + str(noOfErrors)
   print "Classifier Accuracy: " + str(accuracy)
   print "Classifier Error Rate: " + str(1 - accuracy) 
   return accuracy, dictOfConfusionMatrices

#if len(sys.argv) < 6:
#   print "Usage: python RandomForest.py numOfAttributes_m numOfDataPoints_k numOfTrees_N csvFilePath domainFilePath"
#   raise Exception('Invalid Program Inputs')

def runRandomForest(numOfAttributes_m, numOfDataPoints_k, numOfTrees_N, csvFilePath, domainFilePath):
   return randomForest(numOfAttributes_m, numOfDataPoints_k, numOfTrees_N, csvFilePath, domainFilePath)
