import xml.etree.ElementTree
import xml.etree.cElementTree as ET
import utilities
import math
import sys

def parseXML(fileName):
   data = {
      "variables": {},
      "categories": {}
   }
   xmlTree = xml.etree.ElementTree.parse(fileName).getroot()
   isInVariableNest = False
   isInCategoryNest = False
   continuousVariables = {}
   currentVariableGroups = []
   currentVariableName = None
   currentCategoryChoices = []
   currentCategoryName = None
   for elem in xmlTree.iter():
      if isInVariableNest == False and isInCategoryNest == False:
         if elem.tag == "variable":
            isInVariableNest = True
            data["variables"][elem.get("name")] = []
            currentVariableName = elem.get("name")
            if "continuous" in elem.attrib:
               continuousVariables[elem.get("name")] = True
            else:
               continuousVariables[elem.get("name")] = False
         elif elem.tag == "Category":
            isInCategoryNest = True
            data["categories"][elem.get("name")] = []
            currentCategoryName = elem.get("name")
      elif isInVariableNest:
         if elem.tag != "group":
            data["variables"][currentVariableName] = currentVariableGroups
            currentVariableGroups = []
            isInVariableNest = False
            if elem.tag == "Category":
               isInCategoryNest = True
               data["categories"][elem.get("name")] = []
               currentCategoryName = elem.get("name")
            elif elem.tag == "variable":
               isInVariableNest = True
               data["variables"][elem.get("name")] = []
               currentVariableName = elem.get("name")
               if "continuous" in elem.attrib:
                  continuousVariables[elem.get("name")] = True
               else:
                  continuousVariables[elem.get("name")] = False
         elif elem.tag == "group":
            currentVariableGroups.append({ "name": elem.get("name"), "p": elem.get("p") })
      elif isInCategoryNest:
         if elem.tag != "choice":
            data["categories"][currentCategoryName] = currentCategoryChoices
            currentCategoryChoices = []
            isInCategoryNest = False
            if elem.tag == "variable":
               isInVariableNest = True
               data["variables"][elem.get("name")] = []
               currentVariableName = elem.get("name")
               if "continuous" in elem.attrib:
                  continuousVariables[elem.get("name")] = True
               else:
                  continuousVariables[elem.get("name")] = False
            elif elem.tag == "Category":
               isInCategoryNest = True
               data["categories"][elem.get("name")] = []
               currentCategoryName = elem.get("name")
         elif elem.tag == "choice":
            currentCategoryChoices.append({ "name": elem.get("name"), "type": elem.get("type") })
    #At this point, either isInCategoryNestor isInVariableNest would be true, so deal 
    #with it
   if isInVariableNest:
      data["variables"][currentVariableName] = currentVariableGroups
   elif isInCategoryNest:
      data["categories"][currentCategoryName] = currentCategoryChoices

   '''print "--------Variables--------"
   for variableName, groups in data["variables"].iteritems():
      print variableName
      for group in groups:
         print group
   print "--------Categories--------"
   for categoryName, choices in data["categories"].iteritems():
      print categoryName
      for choice in choices:
         print choice'''

   return data, continuousVariables

def parseData(filePath):
   file = open(filePath, "r")
   lines = file.readlines()
   D = []
   domainSizes = []
   D.append(lines[0].strip().split(","))
   categoricalVariableIndex = None
   for index, columnName in enumerate(D[0]):
      if columnName == lines[2].strip():
         categoricalVariableIndex = index
         break

   domainSizesTempArr = lines[1].strip().split(",")
   domainSizes = [int(x) for x in domainSizesTempArr]
   for line in lines[3:]:
      tokens = line.split(",")
      integerArray = [float(x) for x in tokens]
      D.append(integerArray)
   file.close()
   '''print D'''
   return categoricalVariableIndex, D, domainSizes

def isDatasetPure(D, categoricalVariableIndex):
   if len(D[1:]) <= 0:
      return False, None
   var = None
   isPure = True
   for row in D[1:]:
      if var == None:
         var = row[categoricalVariableIndex]
      elif row[categoricalVariableIndex] != var :
         isPure = False
         break
   return isPure, var

#def getAttributeNameFromIndex(A, index):
#   return A["variables"][index]

def findMostFrequentLabel(D, categoricalVariableIndex):
   labels = {}
   for row in D[1:]:
      utilities.addCountInDictionaryForKey(labels, row[categoricalVariableIndex])
   mostFrequentLabel = None
   mostFrequentLabelCount = None
   for label, labelCount in labels.iteritems():
      if mostFrequentLabel == None:
         mostFrequentLabel = label
         mostFrequentLabelCount = labelCount
      elif labelCount > mostFrequentLabelCount:
         mostFrequentLabel = label
         mostFrequentLabelCount = labelCount
   return mostFrequentLabel

def entropy(D, categoricalVariableIndex):
   categoricalVariables = {}
   totalCount = len(D[1:])
   sumOfEntropy = 0.0
   for row in D[1:]:
      utilities.addCountInDictionaryForKey(categoricalVariables, row[categoricalVariableIndex])
   for categoricalValue, count in categoricalVariables.iteritems():
      probability = float(count)/totalCount
      sumOfEntropy += probability * math.log(probability)
   return sumOfEntropy * -1

def entropyASubIContinuousBinarySplit(A, D, ASubI, categoricalVariableIndex, splitValue):
   aSubIIndexForD = None
   for index, attribute in enumerate(D[0]):
      if attribute == ASubI:
         aSubIIndexForD = index
   sumOfEntropyASubI = 0.0
   for i in range(2):
      DSubJ = []
      for d in D[1:]:
         if i == 0:
            if d[aSubIIndexForD] >= splitValue:
               DSubJ.append(d)
         else:
            if d[aSubIIndexForD] < splitValue:
               DSubJ.append(d)
      sumOfEntropyASubI += (float(len(DSubJ))/len(D)) * entropy(DSubJ, categoricalVariableIndex)
   return sumOfEntropyASubI

'''
   Inputs:
      ASubI: a string indicating the current attribute being looked at
'''
def entropyASubI(A, D, ASubI, categoricalVariableIndex):
   aSubIIndexForD = None
   for index, attribute in enumerate(D[0]):
      if attribute == ASubI:
         aSubIIndexForD = index
   sumOfEntropyASubI = 0.0
   for currentAttributeIndex, attributeGroup in enumerate(A["variables"][ASubI]):
      DSubJ = []
      '''
      print "---------------"
      print currentAttributeIndex
      print attributeGroup
      print "----" + str(A["variables"][ASubI])
      '''
      for d in D[1:]:
         #print d[aSubIIndexForD]
         #if d[aSubIIndexForD] == currentAttributeIndex + 1:
         #   DSubJ.append(d)
         
         #if float datatype
         if "." in attributeGroup["name"]:
            if float(d[aSubIIndexForD]) == float(attributeGroup["name"]):
               DSubJ.append(d)
         elif d[aSubIIndexForD] == currentAttributeIndex + 1:
            DSubJ.append(d)
      
      sumOfEntropyASubI += (float(len(DSubJ))/len(D)) * entropy(DSubJ, categoricalVariableIndex)
   return sumOfEntropyASubI

def getAttributeIndexFromAttributeName(name, D):
   for index, attribute in enumerate(D[0]):
      if name == attribute:
         return index

def isAttributeRestricted(attributeName, restrictionsVector, D, A, categoricalVariableIndex):
   return restrictionsVector[getAttributeIndexFromAttributeName(attributeName, D)] == 0

def findBestSplit(A, D, p0, attribute, categoricalVariableIndex):
   counts = {}
   gains = {}
   entropies = {}
   attributeIndex = getAttributeIndexFromAttributeName(attribute, D)
   for d in D[1:]:
      utilities.addCountInDictionaryForKey(counts, d[attributeIndex])
   for attributeValue, count in counts.iteritems():
      entropies[attributeValue] = entropyASubIContinuousBinarySplit(A, D, attribute, categoricalVariableIndex, attributeValue)
      gains[attributeValue] = p0 - entropies[attributeValue]
   bestGain = 0.0
   bestAttributeValue = None
   for attributeValue, gain in gains.iteritems():
      if bestAttributeValue == None:
         bestAttributeValue = attributeValue
         bestGain = gain
      else:
         if gain > bestGain:
            bestAttributeValue = attributeValue
            bestGain = gain
   return bestAttributeValue, entropies[bestAttributeValue]
   

def selectSplittingAttribute(A, D, continuousVariablesDict, threshold, categoricalVariableIndex, restrictionsVector):
   p0 = entropy(D, categoricalVariableIndex)
   gain = []
   p = {}
   splitValues = {}
   for attribute in A["variables"]:
      #if attribute is continuous
      if continuousVariablesDict[attribute] == True:
         bestSplitAttributeValue, entropyOfBestSplitAttributeValue = findBestSplit(A, D, p0, attribute, categoricalVariableIndex)
         p[attribute] = entropyOfBestSplitAttributeValue
         splitValues[attribute] = bestSplitAttributeValue
         gain.append([attribute, (p0 - p[attribute])])
      else:
         p[attribute] = entropyASubI(A, D, attribute, categoricalVariableIndex)
         splitValues[attribute] = None
         gain.append([attribute , (p0 - p[attribute])])
   maxGain = -1
   attrib = ""
   for gains in gain: 
      if gains[1] > maxGain:
         maxGain = gains[1]
         attrib = gains[0]
   if maxGain > threshold:
      return attrib, splitValues[attrib]
   else:
      return None, None

def c45(A, D, continuousVariablesDict, categoricalVariableIndex, domainSizes, T, threshold, restrictionsVector):
   isPure, classLabel = isDatasetPure(D, categoricalVariableIndex)
   if isPure:
      classLabel = int(classLabel)
      node = {
         "label": str(classLabel),
         "decisionName" : A["categories"][D[0][categoricalVariableIndex]][classLabel-1],
         "leafNode" : True
      }
      return node
   elif len(A["variables"]) == 0:
      classLabel = findMostFrequentLabel(D,categoricalVariableIndex)
      decisionName = None
      #if no class label found, just select first decision
      if classLabel == None:
         decisionName = A["categories"][D[0][categoricalVariableIndex]][0]
         #if index is 0, class label is 1
         classLabel = 1
      else:
         classLabel = int(classLabel)
         decisionName = A["categories"][D[0][categoricalVariableIndex]][classLabel-1]
      node = {
         "label": str(classLabel),
         "decisionName" : decisionName,
         "leafNode" : True
      }
      return node
   else:
      aSubG, splitAttributeValue = selectSplittingAttribute(A, D, continuousVariablesDict, threshold, categoricalVariableIndex, restrictionsVector)
      aSubGIndex = getAttributeIndexFromAttributeName(aSubG, D)
      if aSubG == None:
         classLabel = findMostFrequentLabel(D, categoricalVariableIndex)
         decisionName = None
         if classLabel == None:
            decisionName = A["categories"][D[0][categoricalVariableIndex]][0]
            #if index is 0, class label is 1
            classLabel = 1
         else:
            classLabel = int(classLabel)
            decisionName = A["categories"][D[0][categoricalVariableIndex]][classLabel-1]
         node = {
            "label" : str(classLabel), 
            "decisionName" : decisionName,
            "leafNode" : True
         }
         return node
      else:
         node = {
            "label" : str(aSubG),
            "leafNode" : False,
            "edges" : []
         }
        
         #if variable is continuous, we don't want to remove the attribute from the attribute list
         if continuousVariablesDict[aSubG] == True:
            for i in range(2):
               Dv = []
               Dv.append(D[0]) #append header names to Dv 
               for d in D[1:]:
                  if i == 0:
                     if d[aSubGIndex] >= splitAttributeValue:
                        Dv.append(d)
                  else:
                     if d[aSubGIndex] < splitAttributeValue:
                        Dv.append(d)
               if len(Dv) > 1: #1 instead of 0 because there will always be header array 
                   #if the len of Dv is same as D then we can't split anymore otherwise we will result in infinite loop since we use the same D over and over again so just return this node
                   if len(Dv) == len(D):
                      #this part is the same code as the elif(len(A["variables"]) == 0)
                      classLabel = findMostFrequentLabel(D,categoricalVariableIndex)
                      decisionName = None
                      #if no class label found, just select first decision
                      if classLabel == None:
                         decisionName = A["categories"][D[0][categoricalVariableIndex]][0]
                         #if index is 0, class label is 1
                         classLabel = 1
                      else:
                         classLabel = int(classLabel)
                         decisionName = A["categories"][D[0][categoricalVariableIndex]][classLabel-1]
                      node = {
                         "label": str(classLabel),
                         "decisionName" : decisionName,
                         "leafNode" : True
                      }
                      return node                  

                   attributeName = ""
                   if i == 0:
                      attributeName = ">= " + str(splitAttributeValue)
                   else:
                      attributeName = "< " + str(splitAttributeValue)
                   node["edges"].append({ "edgeLabel" : attributeName,  "node" : c45(A, Dv, continuousVariablesDict, categoricalVariableIndex, domainSizes, T, threshold, restrictionsVector) }) 
               else:
                  classLabel = 1
                  decisionName = A["categories"][D[0][categoricalVariableIndex]][classLabel-1]
                  decisionNode = {
                     "label" : str(classLabel), 
                     "decisionName" : decisionName,
                      "leafNode" : True
                  }
                  node["edges"].append({ "edgeLabel" : attribute["name"],  "node" : decisionNode })
         else:
            for index, attribute in enumerate(A["variables"][aSubG]):
               Dv = []
               Dv.append(D[0])
               for row in D[1:]:
                  if row[aSubGIndex] == index+1:
                     Dv.append(row)
               if len(Dv) > 1: #1 instead of 0 because there will always be header array 
                  trimmedA = dict(A)
                  if aSubG in trimmedA["variables"]:
                     del trimmedA["variables"][aSubG]
                     
                  node["edges"].append({ "edgeLabel" : attribute["name"],  "node" : c45(trimmedA, Dv, continuousVariablesDict, categoricalVariableIndex, domainSizes, T, threshold, restrictionsVector) })
               else:
                  classLabel = 1
                  decisionName = A["categories"][D[0][categoricalVariableIndex]][classLabel-1]
                  decisionNode = {
                     "label" : str(classLabel), 
                     "decisionName" : decisionName,
                      "leafNode" : True
                  }
                  node["edges"].append({ "edgeLabel" : attribute["name"],  "node" : decisionNode })
         return node
      
def inOrderTraversalOfTree(T):
   print "Label: " + str(T["label"])
   if "edges" in T.keys(): 
      for edge in T["edges"]:
         print "Edge Label: " + str(edge["edgeLabel"])  
         inOrderTraversalOfTree(edge["node"])

def xmlPrintTreeRecursiveHelper(nodeObject, rootNodeElement):
   if "edges" in nodeObject.keys():
      for index, edge in enumerate(nodeObject["edges"]):
         edgeElement = ET.SubElement(rootNodeElement, "edge", var=edge["edgeLabel"], num=str(index+1))
         if edge["node"]["leafNode"] == True:
            edgeNodeElement = ET.SubElement(edgeElement, "decision", end=str(edge["node"]["label"]), choice=str(edge["node"]["decisionName"]["name"]))
         else:
            edgeNodeElement = ET.SubElement(edgeElement, "node", var=str(edge["node"]["label"]))
         xmlPrintTreeRecursiveHelper(edge["node"], edgeNodeElement)


def xmlPrintTree(T, outputFileName):
   treeElement = ET.Element("Tree", name="Lab2")
   rootNodeElement = ET.SubElement(treeElement, "node", var=T["label"])
   tree = ET.ElementTree(treeElement)
   #if root node has edges
   if "edges" in T.keys():
      for index, edge in enumerate(T["edges"]):
         edgeElement = ET.SubElement(rootNodeElement, "edge", var=edge["edgeLabel"], num=str(index+1))
         if edge["node"]["leafNode"] == True:
            edgeNodeElement = ET.SubElement(edgeElement, "decision", end=str(edge["node"]["label"]), choice=str(edge["node"]["decisionName"]["name"]))
         else:
            edgeNodeElement = ET.SubElement(edgeElement, "node", var=str(edge["node"]["label"]))
         xmlPrintTreeRecursiveHelper(edge["node"], edgeNodeElement)
   tree.write(outputFileName)

def getAttributeRestrictions(fileName):
   attributeRestrictionsFile = open(fileName, "r")
   restrictionsVector = attributeRestrictionsFile.readlines()
   restrictionsVector = [int(x) for x in restrictionsVector[0].strip().split(",")]
   attributeRestrictionsFile.close()
   return restrictionsVector

def printXmlFileToStdout(fileName):
   file = open(fileName, "r")
   for line in file.readlines():
      print line
   file.close()

def applyRestrictions(restrictionsVector, A, D):
   for index, restrictOrNot in enumerate(restrictionsVector):
      if restrictOrNot == 0:
         columnName = D[0][index]
         del A["variables"][columnName]


def runInduceC45(xmlFileName, csvFileName, restrictionsFileName):
   A, continuousVariablesDict = parseXML(xmlFileName)
   T = None
   #print A
   categoricalVariableIndex, D, domainSizes = parseData(csvFileName)
   restrictionsVector = None
   if restrictionsFileName != None:
      restrictionsVector = getAttributeRestrictions(restrictionsFileName)
   if restrictionsVector != None:
      applyRestrictions(restrictionsVector, A, D)
   T = c45(A, D, continuousVariablesDict, categoricalVariableIndex, domainSizes, T, 0.05, restrictionsVector)
   #inOrderTraversalOfTree(T)
   outputFileName = csvFileName.split(".csv")[0] + "Tree.xml"
   xmlPrintTree(T, outputFileName)
   printXmlFileToStdout(outputFileName)
   return outputFileName
