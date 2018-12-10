from analyzer import runAnalysis
import numpy as np
import pandas as pd

def run():
   D = pd.read_csv("Crime_Data_2010_2017.csv")
  #D = D.reset_index().values.ravel().view(dtype=[('DR Number',int), ('Date Reported', str), ('Date Occured', str), ('Time Occured', int), ('Area ID', int), ('Area Name', str), ('Reporting District', int), ('Crime Code', int), ('Crime Code Description', str), ('MO Codes', str), ('Victim Age', int), ('Victim Sex', str), ('Victim Descent', str), ('Premise Code', int), ('Premise Description', str), ('Weapon Used Code', int), ('Weapon Description', str), ('Status Code', str), ('Status Description', str), ('Crime Code 1', int), ('Crime Code 2', int), ('Crime Code 3', int), ('Crime Code 4', int), ('Address', str), ('Cross Street', str), ('Location', str)])
   D = np.array(D.to_records())
   D = D[0:20000]
   avg, truePos, falsePos, falseNeg, trueNeg = runAnalysis(D, 10, 1700)  
   print("Total Accuracy = {}".format(avg))
   print("Confusion Matrix:")
   print("{} {}".format(truePos, falsePos))
   print("{} {}".format(falseNeg, trueNeg))
run()

