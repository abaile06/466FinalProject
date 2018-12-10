import math as mt
import random
from collections import Counter


def getKey(item):
   return item[0]

def computeSimilarity(elem, elem2):
   sim = 0.0
   for index,e in enumerate(elem):
      if e == elem2[index] and index != 0 and index != 1 and index != 16 and index != 17:
         if index != 10:    
            sim +=1
         elif index == 10 and Counter(e) == Counter(elem2[index]):
            sim +=1
   return sim/(len(elem) - 1)


def computeKNN(D, k, elem2, i2):
   KNearest = []
   for i,elem in enumerate(D):
      if i != i2:
         sim = computeSimilarity(elem, elem2)
         if len(KNearest) < k:
            KNearest.append((sim, elem))
         else:
            KNearest = sorted(KNearest, key=getKey)
            for i, j in enumerate(KNearest):
               if j[0] < sim:
                  KNearest[i] = (sim, elem)
                  break
   KNearest = sorted(KNearest, key=getKey)
   numm = 0.0
   for elem in KNearest:
      if elem[1][16] == 400:
         numm+=1
   item = 0
   if numm/len(KNearest) >= .5:
      item = 400
   
   if elem2[16] == 400 and item == 400:
      strin = ""
      for i in range(len(elem2) - 1):
         if i + 1 != 16:
            if type(elem2[i + 1]) is str:
               if elem2[i + 1] == "M":
                  strin = strin + "," + "0"
               elif elem2[i + 1] == "F":
                  strin = strin + "," + "1"
               else:
                  strinR = elem2[i+1].split()
                  strin = strin + "," + "\"" + ' '.join(strinR) + "\""
            else:
               strin = strin + ","  + str(elem2[i + 1]) 
         else:
            strin = strin + "," + "1"
      #print(strin)
      #print("True")
      return 1,1,0,0,0
   elif elem2[16] != 400 and item != 400:
      strin = ""
      for i in range(len(elem2) - 1):
         if i + 1 != 16:
            if type(elem2[i + 1]) is str:
               if elem2[i + 1] == "M":
                  strin = strin + "," + "0"
               elif elem2[i + 1] == "F":
                  strin = strin + "," + "1"
               else:
                  strinR = elem2[i+1].split()
                  strin = strin + "," + "\"" + ' '.join(strinR) + "\""
            else:
               strin = strin + "," + str(elem2[i + 1])
         else:
            strin = strin + "," + "1"
      #print(strin)
      #print("True")
      return 1,0,0,0,1

   elif elem2[16] == 400 and item != 400:
      strin = ""
      for i in range(len(elem2) - 1):
         if i + 1 != 16:
            if type(elem2[i + 1]) is str:
               if elem2[i + 1] == "M":
                  strin = strin + "," + "0"
               elif elem2[i + 1] == "F":
                  strin = strin + "," + "1"
               else:
                  strinR = elem2[i+1].split()
                  strin = strin + "," + "\"" + ' '.join(strinR) + "\""
            else:
               strin = strin + "," + str(elem2[i + 1])
         else: 
            strin = strin + "," + "-1"
      print(strin)
      return 0,0,0,1,0

   strin = ""
   for i in range(len(elem2) - 1):
      if i + 1 != 16:
         if type(elem2[i + 1]) is str:
            if elem2[i + 1] == "M":
               strin = strin + "," + "0"
            elif elem2[i + 1] == "F":
               strin = strin + "," + "1"
            else:
               strinR = elem2[i+1].split()
               strin = strin + "," + "\"" + ' '.join(strinR) + "\""
         else:
            strin = strin + "," + str(elem2[i + 1])
      else:
         strin = strin + "," + "-1"
   print(strin)
   #print("False")
   return 0,0,1,0,0

         


def runAnalysis(D, k, n):   
   acc = 0.0
   truePos = 0.0
   falsePos = 0.0
   falseNeg = 0.0
   trueNeg = 0.0
   for i in range(n):
   #for i,elem in enumerate(D):
      #print(elem)
      j = random.randint(0,19999)
      acc1, truePos1, falsePos1, falseNeg1, trueNeg1 = computeKNN(D, k, D[j], j)
      acc += acc1
      truePos += truePos1
      falsePos += falsePos1
      falseNeg += falseNeg1
      trueNeg += trueNeg1
   return float(acc)/n, truePos, falsePos, falseNeg, trueNeg

#runAnalysis()
