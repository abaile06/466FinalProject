import math
import utilities
import sys

def parseCSVFile(pathToCSVFile):
   f = open(pathToCSVFile, "r")
   lines = f.readlines()
   dataRows = []
   for dataLine in lines[3:]:
      tokens = dataLine.strip().split(",")
      dataRows.append(tokens)
   f.close()
   return dataRows

def getDistanceBetweenPoints(dataRows, i, j):
   distanceSum = 0.0
   #print(dataRows[i])
   #print(dataRows[j])
   for columnValue1, columnValue2 in zip(dataRows[i], dataRows[j]):
      try:
         floatValue1 = float(columnValue1)
         floatValue2 = float(columnValue2)
         subtractionValue = floatValue1 - floatValue2
         distanceSum += subtractionValue * subtractionValue
      except:
         if columnValue1 != columnValue2:
            distanceSum += 50.0
   return math.sqrt(distanceSum)

def getDistanceMatrix(dataRows):
   noOfRows = len(dataRows)
   distanceMatrix = [[None] * noOfRows for i in range(noOfRows)]
   for i in range(noOfRows):
      for j in range(i, noOfRows):
         if i != j:
            distance = getDistanceBetweenPoints(dataRows, i, j)
            distanceMatrix[i][j] = distance
            distanceMatrix[j][i] = distance
         else:
            distanceMatrix[i][j] = 0.0
   
   #for i in range(noOfRows):
   #   print(distanceMatrix[i])
   return distanceMatrix

def getKNearestNeighbors(pointId, distanceMatrix, k):
   distancesWithIndexList = []
   for index, distanceToOtherPoint in enumerate(distanceMatrix[pointId]):
      if index != pointId:
         distancesWithIndexList.append([index, distanceToOtherPoint])
   distancesWithIndexList.sort(key=lambda x: x[1])
   
   return distancesWithIndexList[:k]

def getPluralityClassLabel(kNearestNeighbors, dataRows):
   classLabelIndex = len(dataRows[0]) - 1
   classLabelToCountsDict = {} #maps class label string => count of class label
   for distanceWithIndex in kNearestNeighbors:
      pointId = distanceWithIndex[0]
      utilities.addCountInDictionaryForKey(classLabelToCountsDict, dataRows[pointId][classLabelIndex]) 

   pluralityClassLabel = None
   pluralityClassLabelCount = None
   for classLabel, classLabelCount in classLabelToCountsDict.items():
      if pluralityClassLabel == None or classLabelCount > pluralityClassLabelCount:
         pluralityClassLabel = classLabel
         pluralityClassLabelCount = classLabelCount
   return pluralityClassLabel

def runKNN(pathToCSVFile, k):
   dataRows = parseCSVFile(pathToCSVFile)
   distanceMatrix = getDistanceMatrix(dataRows)
   noOfRows = len(dataRows)
   numberOfCorrectlyClassifiedRows = 0
   for pointId, dataRow in enumerate(dataRows):
      kNearestNeighbors = getKNearestNeighbors(pointId, distanceMatrix, k) 
      #kNearestNeighbors 
      #will contain a list of [pointId, distance] sorted in ascending order for the k nearest neighbors and their distances
      predictedClassLabel = getPluralityClassLabel(kNearestNeighbors, dataRows)
      classLabelIndex = len(dataRows[0]) - 1
      actualClassLabel = dataRow[classLabelIndex]
      if predictedClassLabel == actualClassLabel:
         numberOfCorrectlyClassifiedRows += 1
      print("Point Id: " + str(pointId) + " Predicted class: " + predictedClassLabel \
               + " Actual class: " + actualClassLabel)
   print("------------------------")
   print("Accuracy for classifying all points: " + str(float(numberOfCorrectlyClassifiedRows)/noOfRows))
   print("------------------------")

pathToCSVFile = sys.argv[1]
k = int(sys.argv[2])
runKNN(pathToCSVFile, k)