import sys
from datetime import datetime
import json
import utilities
import numpy as np


#---------------------------------
#python3 main.py  ./crimes-new-york-city/NYPD_Complaint_Data_Historic.csv 

#Uncomment this if you want to output a json file dump of dateString => noOfCrimes for that date

# pathToNYPDCrimeDataset = sys.argv[1] 
# f = open(pathToNYPDCrimeDataset, "r")
# firstLine = True
# headerLine = None
# currentDate = None
# dateToNoOfCrimesDict = {} #maps dateString => noOfCrimes
# for line in f:
#    if firstLine == True:
#       headerLine = line
#       firstLine = False
#    else:
#       tokens = line.split(",")
#       dateString = tokens[1].strip()
#       if "2015" not in dateString and "2014" not in dateString:
#          continue
#       try:
#          currentLineDate = datetime.strptime(dateString, "%m/%d/%Y").date()
#          utilities.addCountInDictionaryForKey(dateToNoOfCrimesDict, dateString)
#       except:
#          continue

# with open("./dateToNoOfCrimesDict.json", "w") as dateToNoOfCrimesDictFileHandler:
#    json.dump(dateToNoOfCrimesDict, dateToNoOfCrimesDictFileHandler)   
# f.close()
#---------------------------------


#1048576 lines
# with open("./dateToNoOfCrimesDict.json") as dateToNoOfCrimesDictFileHandler:
#    dateToNoOfCrimesDict = json.load(dateToNoOfCrimesDictFileHandler)
#    summation = 0
#    for key, value in dateToNoOfCrimesDict.items():
#       print(key + " " + str(value))
#       summation += value
#    print(summation)


#---------------------------------
#/Users/joewijoyo/anaconda3/bin/python3.7 main.py ./historical-hourly-weather-data/temperature.csv ./historical-hourly-weather-data/wind_speed.csv ./historical-hourly-weather-data/humidity.csv ./historical-hourly-weather-data/weather_description.csv historical-hourly-weather-data/pressure.csv historical-hourly-weather-data/wind_direction.csv 

#Uncomment this to get dateToWeatherDataDict outputted to the current directory as a json dump file

# WEATHER_DATASET_DATE_COLUMN_INDEX = 0
# WEATHER_DATASET_NEW_YORK_COLUMN_INDEX = 28

# def getWeatherDataFromWeatherCSVFile(pathToWeatherDataset, dateToWeatherDataDict, keyString):
#    firstLine = True
#    f = open(pathToWeatherDataset, "r")
#    for line in f:
#       if firstLine == True:
#          headerLine = line
#          firstLine = False
#          #print(headerLine.split(",")[WEATHER_DATASET_NEW_YORK_COLUMN_INDEX])
#       else:
#          tokens = line.split(",")
#          dateString = tokens[WEATHER_DATASET_DATE_COLUMN_INDEX].split(" ")[0]
#          if "2015" not in dateString and "2014" not in dateString:
#             continue
#          try:
#             currentLineDate = datetime.strptime(dateString, "%Y-%m-%d").date()
#             currentLineDate = datetime.strftime(currentLineDate, "%m/%d/%Y")
#             if currentLineDate not in dateToWeatherDataDict:
#                dateToWeatherDataDict[currentLineDate] = {
#                   "humidityValuesList" : [],
#                   "pressureValuesList" : [],
#                   "temperatureValuesList" : [],
#                   "weatherDescriptionValuesList" : [],
#                   "windDirectionValuesList" : [],
#                   "windSpeedValuesList" : []
#                }
#             appendValue = None
#             try:
#                appendValue = float(tokens[WEATHER_DATASET_NEW_YORK_COLUMN_INDEX])
#             except:
#                appendValue = tokens[WEATHER_DATASET_NEW_YORK_COLUMN_INDEX].strip()
#             if appendValue != "":
#                dateToWeatherDataDict[currentLineDate][keyString].append(appendValue)
     
#          except:
#             continue
          
#    f.close()

# dateToWeatherDataDict = {} 
# """
#    dateString => {
#       humidity:
#       pressure:
#       temperature:
#       weatherDescription:
#       windDirection:
#       windSpeed:
#    }
# """
# for pathToWeatherDataset in sys.argv[1:]:
#    keyString = None
#    if "temperature" in pathToWeatherDataset:
#       keyString = "temperatureValuesList"
#    elif "wind_speed" in pathToWeatherDataset:
#       keyString = "windSpeedValuesList"
#    elif "humidity" in pathToWeatherDataset:
#       keyString = "humidityValuesList"
#    elif "weather_description" in pathToWeatherDataset:
#       keyString = "weatherDescriptionValuesList"
#    elif "pressure" in pathToWeatherDataset:
#       keyString = "pressureValuesList"
#    else:
#       keyString = "windDirectionValuesList"
#    getWeatherDataFromWeatherCSVFile(pathToWeatherDataset, dateToWeatherDataDict, keyString)

# for dateString, weatherDataDict in dateToWeatherDataDict.items():
#    dateToWeatherDataDict[dateString]["humidity"] = np.mean(weatherDataDict["humidityValuesList"])
#    dateToWeatherDataDict[dateString]["temperature"] = np.mean(weatherDataDict["temperatureValuesList"])
#    dateToWeatherDataDict[dateString]["windSpeed"] = np.mean(weatherDataDict["windSpeedValuesList"])
#    dateToWeatherDataDict[dateString]["weatherDescription"] = utilities.getMostAppearingValueInList(weatherDataDict["weatherDescriptionValuesList"])
#    dateToWeatherDataDict[dateString]["pressure"] = np.mean(weatherDataDict["pressureValuesList"])
#    dateToWeatherDataDict[dateString]["windDirection"] = np.mean(weatherDataDict["windDirectionValuesList"])
#    del(weatherDataDict["humidityValuesList"])
#    del(weatherDataDict["temperatureValuesList"])
#    del(weatherDataDict["windSpeedValuesList"])
#    del(weatherDataDict["weatherDescriptionValuesList"])
#    del(weatherDataDict["pressureValuesList"])
#    del(weatherDataDict["windDirectionValuesList"])
#    print(weatherDataDict)

# with open("./dateToWeatherDataDict.json", "w") as dateToWeatherDataDictFileHandler:
#     json.dump(dateToWeatherDataDict, dateToWeatherDataDictFileHandler)   

#need to make a csv file where weather attributes are on the line and 
#---------------------------------

import xml.etree.ElementTree
import xml.etree.cElementTree as ET

dateToWeatherDataDict = {}
with open("./dateToWeatherDataDict.json") as dateToWeatherDataDictFileHandler:
   dateToWeatherDataDict = json.load(dateToWeatherDataDictFileHandler)

dateToNoOfCrimesDict = {}
with open("./dateToNoOfCrimesDict.json") as dateToNoOfCrimesDictFileHandler:
   dateToNoOfCrimesDict = json.load(dateToNoOfCrimesDictFileHandler)


allUniqueValuesDict = {
   "humidity" : [],
   "temperature" : [],
   "windSpeed" : [],
   "weatherDescription" : [],
   "pressure" : [],
   "windDirection" : [],
   "crimeRate" : [],
} #maps column => [unique values of column]
count = 0
noOfLessThanOrEqualTo800 = 0
noOf801To1000 = 0
noOf1001To1200 = 0
noOf1201To1400 = 0
noOfGreaterThan1400 = 0
for dateString, noOfCrimes in dateToNoOfCrimesDict.items(): 
   if dateString in dateToWeatherDataDict:
      weatherDataDict = dateToWeatherDataDict[dateString]
      crimeRateString = None
      if noOfCrimes <= 800:
         crimeRateString = "<=800"
         noOfLessThanOrEqualTo800 += 1
      elif noOfCrimes <= 1000:
         crimeRateString = "801-1000"
         noOf801To1000 += 1
      elif noOfCrimes <= 1200:
         crimeRateString = "1001-1200"
         noOf1001To1200 += 1
      elif noOfCrimes <= 1400:
         crimeRateString = "1201-1400"
         noOf1201To1400 += 1
      else:
         crimeRateString = ">1400"
         noOfGreaterThan1400 += 1
      if str(weatherDataDict["weatherDescription"]) not in allUniqueValuesDict["weatherDescription"]:
         allUniqueValuesDict["weatherDescription"].append(str(weatherDataDict["weatherDescription"]))
      if crimeRateString not in allUniqueValuesDict["crimeRate"]:
         allUniqueValuesDict["crimeRate"].append(crimeRateString)
      count += 1
print(count)
print("No of <=800: " + str(noOfLessThanOrEqualTo800))
print("No of 801-1000: " + str(noOf801To1000))
print("No of 1001-1200: " + str(noOf1001To1200))
print("No of 1201-1400: " + str(noOf1201To1400))
print("No of >1400: " + str(noOfGreaterThan1400))

# with open("./weatherDataAndNoOfCrimesData.csv", "w") as outputCSVFileHandler:
#    outputCSVFileHandler.write("humidity,temperature,windSpeed,weatherDescription,pressure,windDirection,crimeRate\n")
#    outputCSVFileHandler.write("1,1,1,1,1,1,1\n")
#    outputCSVFileHandler.write("crimeRate\n")
#    for dateString, noOfCrimes in dateToNoOfCrimesDict.items(): 
#       if dateString in dateToWeatherDataDict:
#          crimeRateString = None
#          if noOfCrimes <= 800:
#             crimeRateString = "<=800"
#          elif noOfCrimes <= 1000:
#             crimeRateString = "801-1000"
#          elif noOfCrimes <= 1200:
#             crimeRateString = "1001-1200"
#          elif noOfCrimes <= 1400:
#             crimeRateString = "1201-1400"
#          else:
#             crimeRateString = ">1400"
#          weatherDataDict = dateToWeatherDataDict[dateString]
#          writeString = str(weatherDataDict["humidity"]) + "," + str(weatherDataDict["temperature"]) + "," \
#                           + str(weatherDataDict["windSpeed"]) + "," + str(allUniqueValuesDict["weatherDescription"].index(weatherDataDict["weatherDescription"]) + 1) + "," \
#                           + str(weatherDataDict["pressure"]) + "," + str(weatherDataDict["windDirection"]) + "," \
#                           + str(allUniqueValuesDict["crimeRate"].index(crimeRateString) + 1) + "\n"
#          outputCSVFileHandler.write(writeString)
#          print(noOfCrimes)

#          if str(weatherDataDict["humidity"]) not in allUniqueValuesDict["humidity"]:
#             allUniqueValuesDict["humidity"].append(str(weatherDataDict["humidity"]))
#          if str(weatherDataDict["temperature"]) not in allUniqueValuesDict["temperature"]:
#             allUniqueValuesDict["temperature"].append(str(weatherDataDict["temperature"]))
#          if str(weatherDataDict["windSpeed"]) not in allUniqueValuesDict["windSpeed"]:
#             allUniqueValuesDict["windSpeed"].append(str(weatherDataDict["windSpeed"]))
#          # if str(weatherDataDict["weatherDescription"]) not in allUniqueValuesDict["weatherDescription"]:
#          #    allUniqueValuesDict["weatherDescription"].append(str(weatherDataDict["weatherDescription"]))
#          if str(weatherDataDict["pressure"]) not in allUniqueValuesDict["pressure"]:
#             allUniqueValuesDict["pressure"].append(str(weatherDataDict["pressure"]))
#          if str(weatherDataDict["windDirection"]) not in allUniqueValuesDict["windDirection"]:
#             allUniqueValuesDict["windDirection"].append(str(weatherDataDict["windDirection"]))
#          # if crimeRateString not in allUniqueValuesDict["crimeRate"]:
#          #    allUniqueValuesDict["crimeRate"].append(crimeRateString)
         
#          #outputCSVFileHandler.write("")


# #CODE BELOW TO CREATE XML DOMAIN FILE
# domainRootElement = ET.Element("domain")

# humidityElement = ET.SubElement(domainRootElement, "variable", name="humidity", continuous="true")
# for uniqueElement in allUniqueValuesDict["humidity"]:
#    ET.SubElement(humidityElement, "group", name=uniqueElement, p=".00")

# temperatureElement = ET.SubElement(domainRootElement, "variable", name="temperature", continuous="true")
# for uniqueElement in allUniqueValuesDict["temperature"]:
#    ET.SubElement(temperatureElement, "group", name=uniqueElement, p=".00")

# windSpeedElement = ET.SubElement(domainRootElement, "variable", name="windSpeed", continuous="true")
# for uniqueElement in allUniqueValuesDict["windSpeed"]:
#    ET.SubElement(windSpeedElement, "group", name=uniqueElement, p=".00")

# weatherDescriptionElement = ET.SubElement(domainRootElement, "variable", name="weatherDescription")
# for uniqueElement in allUniqueValuesDict["weatherDescription"]:
#    ET.SubElement(weatherDescriptionElement, "group", name=uniqueElement, p=".00")

# pressureElement = ET.SubElement(domainRootElement, "variable", name="pressure", continuous="true")
# for uniqueElement in allUniqueValuesDict["pressure"]:
#    ET.SubElement(pressureElement, "group", name=uniqueElement, p=".00")

# windDirectionElement = ET.SubElement(domainRootElement, "variable", name="windDirection", continuous="true")
# for uniqueElement in allUniqueValuesDict["windDirection"]:
#    ET.SubElement(windDirectionElement, "group", name=uniqueElement, p=".00")

# crimeRateElement = ET.SubElement(domainRootElement, "Category", name="crimeRate")
# for index, uniqueElement in enumerate(allUniqueValuesDict["crimeRate"]):
#    ET.SubElement(crimeRateElement, "choice", name=uniqueElement, type=str(index))

# ET.ElementTree(domainRootElement).write("weatherDataAndNoOfCrimesDataDomain.xml")
