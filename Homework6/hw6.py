#Aaron Schlessman
#CS4630
#Homework6
#Hydrology

import datetime
import pandas
import numpy
import matplotlib.pyplot as plt 
from suds.client import Client
from IPython.display import display

#a lot of the data gathering is from the slides

StartDate, EndDate, mySiteCode = "3/5/2021 3/6/2021 04212100".split()
# StartDate, EndDate, mySiteCode = input("Enter Start Date, End Date and Site Code: ").split()

def reformatDateTime(date):
    month, day, year = date.split("/")
    newdate = datetime.date(int(year), int(month), int(day))
    return newdate

StartDate = reformatDateTime(StartDate)
EndDate = reformatDateTime(EndDate)
siteCode = "NWISUV:" + mySiteCode

wsdiURL = "http://hydroportal.cuahsi.org/nwisuv/cuahsi_1_1.asmx?WSDL"

NWIS = Client(wsdiURL).service

WaterTempC = "NWISUV:00010"
AirTempF = "NWISUV:00021"
WindSpeedMPH = "NWISUV:00035"
DischargeFPS3 = "NWISUV:00060"

WaterTempC_response = NWIS.GetValuesObject(siteCode, WaterTempC, StartDate, EndDate)
AirTempF_response = NWIS.GetValuesObject(siteCode, AirTempF, StartDate, EndDate)
WindSpeedMPH_response = NWIS.GetValuesObject(siteCode, WindSpeedMPH, StartDate, EndDate)
DischargeFPS3_response = NWIS.GetValuesObject(siteCode, DischargeFPS3, StartDate, EndDate)

def getData(response, vcode):
    df = pandas.DataFrame(columns = ['Date', 'Time', 'Value'])
    try:
        getattr(response.timeSeries[0].values[0], 'value')
    except AttributeError:
        print("No value: ", mySiteCode, ":", vcode)
    else:
        values = response.timeSeries[0].values[0].value
        myDataValues=[]
        times = []
        dates = []
        for x in values:
            myDataValues.append(float(x.value))
            dates.append(x._dateTime.date())
            times.append(x._dateTime.time())

        df = pandas.DataFrame({'Date': dates,'Time': times, 'Value': myDataValues})
        
    return(df)

def ConvertCtoF(DF_WaterTempC):
    DF_WaterTempF = DF_WaterTempC.copy()
    DF_WaterTempF['Value'] = DF_WaterTempF['Value']*9/5+32
    return(DF_WaterTempF)

DF_WaterTempC = getData(WaterTempC_response, WaterTempC)
DF_WaterTempF = ConvertCtoF(DF_WaterTempC)
DF_AirTempF = getData(AirTempF_response, AirTempF)
DF_WindSpeedMPH = getData(WindSpeedMPH_response, WindSpeedMPH)
DF_DischargeFPS3 = getData(DischargeFPS3_response, DischargeFPS3)

DF_WaterTempC['Value'] = DF_WaterTempC['Value'].astype(float)
DF_WaterTempF['Value'] = DF_WaterTempF['Value'].astype(float)
DF_AirTempF['Value'] = DF_AirTempF['Value'].astype(float)
DF_WindSpeedMPH['Value'] = DF_WindSpeedMPH['Value'].astype(float)
DF_DischargeFPS3['Value'] = DF_DischargeFPS3['Value'].astype(float)

DF_WaterTempC_DailyAvg = DF_WaterTempC['Value'].groupby(DF_WaterTempC['Date']).mean()
DF_WaterTempF_DailyAvg = DF_WaterTempF['Value'].groupby(DF_WaterTempF['Date']).mean()
DF_AirTempF_DailyAvg = DF_AirTempF['Value'].groupby(DF_AirTempF['Date']).mean()
DF_WindSpeedMPH_DailyAvg = DF_WindSpeedMPH['Value'].groupby(DF_WindSpeedMPH['Date']).mean()
DF_DischargeFPS3_DailyAvg = DF_DischargeFPS3['Value'].groupby(DF_DischargeFPS3['Date']).mean()

def getMeanMinMaxSD(DF, name):
    newDF = pandas.DataFrame({'Name': name, 'Min': DF['Value'].min(), 'Max': DF['Value'].max(), 'Mean': DF['Value'].mean(), 'S.D.': DF['Value'].std()}, index=[0])
    return(newDF)

DF_WaterTempC_full = getMeanMinMaxSD(DF_WaterTempC, 'Water Temp C')
DF_WaterTempF_full = getMeanMinMaxSD(DF_WaterTempF, 'Water Temp F')
DF_AirTempF_full = getMeanMinMaxSD(DF_AirTempF, 'Air Temp F')
DF_WindSpeedMPH_full = getMeanMinMaxSD(DF_WindSpeedMPH, 'Wind Speed MPH')
DF_DischargeFPS3_full = getMeanMinMaxSD(DF_DischargeFPS3, 'Discharge f/s^3')

merge1 = pandas.merge(DF_WaterTempC_DailyAvg, DF_WaterTempF_DailyAvg, left_on='Date', right_on='Date', how = 'left')
merge2 = pandas.merge(merge1, DF_AirTempF_DailyAvg, left_on='Date', right_on='Date', how = 'left')
merge3 = pandas.merge(merge2, DF_WindSpeedMPH_DailyAvg, left_on='Date', right_on='Date', how = 'left')
DF_Merged_Avg = pandas.merge(merge3, DF_DischargeFPS3_DailyAvg, left_on='Date', right_on='Date', how = 'left')
DF_Merged_Avg.columns = ['Water Temp C', 'Water Temp F', 'Air Temp F', 'Wind Speed MPH', 'Discharge f/s^3']
display("\nDaily Averages")
empty_columns = [x for x in DF_Merged_Avg.columns if DF_Merged_Avg[x].isnull().all()] #credit to https://www.jitsejan.com/find-and-delete-empty-columns-pandas-dataframe.html
DF_Merged_Avg.drop(empty_columns, axis=1, inplace=True)
display(DF_Merged_Avg)

DF_Merged = pandas.concat([DF_WaterTempC_full, DF_WaterTempF_full, DF_AirTempF_full, DF_WindSpeedMPH_full, DF_DischargeFPS3_full])
DF_Merged = DF_Merged.dropna()
DF_Merged.reset_index(drop=True, inplace=True)
display("\nFull Series attributes")
display(DF_Merged)

merge4 = pandas.merge(DF_WaterTempC, DF_WaterTempF, left_on=['Date','Time'], right_on=['Date','Time'], how = 'left')
merge5 = pandas.merge(merge4, DF_AirTempF, left_on=['Date','Time'], right_on=['Date','Time'], how = 'left')
merge6 = pandas.merge(merge5, DF_WindSpeedMPH, left_on=['Date','Time'], right_on=['Date','Time'], how = 'left')
DF_Merged_empty = pandas.merge(merge6, DF_DischargeFPS3, left_on=['Date','Time'], right_on=['Date','Time'], how = 'left')
DF_Merged_empty.columns = ['Date', 'Time', 'Water Temp C', 'Water Temp F', 'Air Temp F', 'Wind Speed MPH', 'Discharge f/s^3']

empty_columns = [x for x in DF_Merged_empty.columns if DF_Merged_empty[x].isnull().all()] #credit to https://www.jitsejan.com/find-and-delete-empty-columns-pandas-dataframe.html

display("\nMissing Data")

for x in empty_columns:
    display(x, " is Empty")

DF_Merged_empty.drop(empty_columns, axis=1, inplace=True)
DF_Merged_empty = DF_Merged_empty[DF_Merged_empty.isnull().any(axis=1)] #credit to https://stackoverflow.com/questions/43424199/display-rows-with-one-or-more-nan-values-in-pandas-dataframe

display(DF_Merged_empty.tail())

plotframe = DF_Merged_Avg.copy()
if 'Water Temp F' in plotframe : plotframe = plotframe.drop(columns = 'Water Temp F')
plotframe.plot(title = mySiteCode)
plt.show()