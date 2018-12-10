
def addCountInDictionaryForKey(dictionary, key):
   if key not in dictionary:
      dictionary[key] = 1
   else:
      dictionary[key] += 1


def getMostAppearingValueInList(inputList):
   valueToNumberOfOccurencesDict = {} #maps value => numberOfOccurences
   for value in inputList:
      addCountInDictionaryForKey(valueToNumberOfOccurencesDict, value)
   mostFrequentValue = None
   mostFrequentValueNumberOfOccurences = None
   for value, numberOfOccurences in valueToNumberOfOccurencesDict.items():
      if mostFrequentValue == None or numberOfOccurences > mostFrequentValueNumberOfOccurences:
         mostFrequentValue = value
         mostFrequentValueNumberOfOccurences = numberOfOccurences
   return mostFrequentValue

def appendToListIfNotInList(listObject, element):
   if element not in listObject:
      listObject.append(element)