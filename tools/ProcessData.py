# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import sys
import csv

def parseDate(x):
	return datetime.strptime(x, '%A, %B %d, %Y')

def parseDate2(x):
	return datetime.strptime(x, '%A, %B %d, %Y').strftime('%Y%m%d')

def parseDate3(x):
	return x.strftime('%Y%m%d')

def replaceInvalidTicker(x):
	arr1 = x.split("-")
	if ("AJ5" == arr1[0] and x != "AJ5-MTSLV16"):
		x = "AJ5-MTSLV16"
		return x
	if ("AM1" == arr1[0] and x != "AM1-RYL17"):
		x = "AM1-RYL17"
		return x
	return x

def preProcess():
	#load original data
	df = pd.read_csv("../../spure.csv")

	#declare params
	colors = []
	sneaker = {}
	tickers = []
	tickers_dict = {}

	#extracte tickers
	for i in df.loc[:,["Ticker"]].drop_duplicates().loc[:,"Ticker"]:
		key = i.split("-")[0]
		value = i.split("-")[1]

		arr = sneaker.get(key, [])
		if value not in arr:
			arr.append(value)
		sneaker[key] = arr	

	sneaker['AJ5'] = sneaker['AJ5'][0:3]
	sneaker['AM1'] = sneaker['AM1'][0:1]

	#print(sneaker['AJ5'])
	#print(sneaker['AM1'])

	#generate the tickers dict
	for k,v in sneaker.items():
		for i in v:
			tickers.append(k+"-"+i)

	for i in range(len(tickers)):
		tickers_dict[tickers[i]] = i+1

	# AJ5_Need_Replace_Ticker = []
	# AM1_Need_Replace_Ticker = []

	# df_tmp = df[~ df.Ticker.isin(tickers)]
	# for index, row in df_tmp.iterrows():
	# 	if row["Ticker"].split("-")[0] == "AJ5":
	# 		AJ5_Need_Replace_Ticker.append(row["Ticker"])
	# 		#df[index,"Ticker"] = "AJ5-MTSLV16"
	# 	elif row["Ticker"].split("-")[0] == "AM1":
	# 		AM1_Need_Replace_Ticker.append(row["Ticker"])
	# 		#df[index,"Ticker"] = "AM1-RYL17"
	#for i in AJ5_Need_Replace_Ticker:
	#	df['Ticker'].replace(i, "AJ5-MTSLV16")

	#for i in AM1_Need_Replace_Ticker:
	#	df['Ticker'].replace(i, "AM1-RYL17")

	df["Ticker"] = df['Ticker'].map(replaceInvalidTicker)
	#print(df[~ df.Ticker.isin(tickers)])


	#extracte date
	date = []
	for i in df.loc[:,["Date"]].drop_duplicates().loc[:,"Date"]:
		date.append(i)

	tickers2dateMap = {}
	for index, row in df.iterrows():
		dateList = tickers2dateMap.get(row['Ticker'],[])
		if(len(dateList) == 0):
			dateList.append(parseDate(row['Date'])) # min
			dateList.append(parseDate(row['Date'])) # max
			tickers2dateMap[row['Ticker']] = dateList
			continue
		newDate = parseDate(row['Date'])
		if (newDate < dateList[0]):
			dateList[0] = newDate
		if (newDate > dateList[1]):
			dateList[1] = newDate
		tickers2dateMap[row['Ticker']] = dateList

	startTime = None
	endTime = None
	count = 0
	need_delete_tickers = []
	for i, v in tickers2dateMap.items():
		if v[0] >= datetime.strptime("2017-08-01", "%Y-%m-%d"):
			need_delete_tickers.append(i)
			continue
		if startTime == None:
			startTime = v[0]
			endTime = v[1]
			continue
		if (startTime < v[0]):
			startTime = v[0]
		if (endTime < v[1]):
			endTime = v[1]
		count = count + 1
	#print(len(df))
	df2 = df.drop(df[df.Ticker.isin(need_delete_tickers)].index.tolist())
	df2['Date'] = df2['Date'].map(parseDate2)

	tickers = df2.loc[:,["Ticker"]].drop_duplicates().loc[:,"Ticker"]

	SpureMap = {}
	Time = 155
	for ticker in tickers:
		local_size_list = [i for i in df2[df2.Ticker==ticker].loc[:,["Size"]].drop_duplicates().loc[:,"Size"]]
		for size in local_size_list:
			local_df = df2[(df2.Ticker==ticker)&(df2.Size==size)]
			for i in range(Time+1):
				currentDate = startTime + i * timedelta(days=1)
				key = ticker+"||"+size + "||" + parseDate3(currentDate)
				local_price = [p for p in local_df[local_df.Date==parseDate3(currentDate)].loc[:,["Sale Price"]].loc[:,"Sale Price"]]
				circletimes = 1000
				now = currentDate
				while (len(local_price) == 0 and circletimes > 0):
					currentDate = currentDate - timedelta(days=1)
					circletimes = circletimes - 1
					local_price = [p for p in local_df[local_df.Date==parseDate3(currentDate)].loc[:,["Sale Price"]].loc[:,"Sale Price"]]

				currentDate = now
				while (len(local_price) == 0 and currentDate <= endTime):
					currentDate = currentDate + timedelta(days=1)
					local_price = [p for p in local_df[local_df.Date==parseDate3(currentDate)].loc[:,["Sale Price"]].loc[:,"Sale Price"]] 
				
				#print([p for p in local_df[local_df.Date==parseDate3(currentDate)].loc[:,["Sale Price"]].loc[:,"Sale Price"]])
				print(key)
				sys.stdout.flush()
				total_price = 0
				for p in local_price:
					p = p.replace("$","").replace(",","")
					total_price = total_price + int(p)
				SpureMap[key] = total_price // len(local_price)

	for i, v in SpureMap.items():
		print(i+" "+str(v))
	#df2.to_csv('tmp.csv',columns=['Date','Time','Size','Sale Price', 'Ticker'],index=False)

	# tickers = list(set(df2.Ticker.tolist()))
	# a = df[df.Ticker.isin(tickers[0:1])].index.tolist()
	# local_size_list = []
	# local_date_list = []
	# for i in a:
	# 	local_size_list.append(str(df.loc[i,['Size']]))
	# 	local_date_list.append(str(df.loc[i,['Date']]))
	# local_size_list = list(set(local_size_list))
	# local_date_list = list(set(local_date_list))

def extractDateSet(startLine=0, endLine=0, inputFile="price", outFile="price.csv"):
	input_file = open("price")
	index = 0
	#writer = csv.writer(open(outFile, "w"))
	writer = open(outFile, "w")
	for line in input_file:
		index = index + 1
		if index >= startLine and index <= endLine:
			line = line.replace("\r","").replace("\n","")
			arr = line.split(" ")
			#row = []
			#row.append(arr[1])
			#writer.writerows(arr[1])
			writer.writelines(arr[1]+"\r\n")

def extractDateSet2(startLine=0, endLine=0, inputFile="price", outFile="price.csv"):
	input_file = open("price")
	index = 0
	priceMap = {}
	writer = open(outFile, "w")
	for line in input_file:
		index = index + 1
		if index >= startLine and index <= endLine:
			line = line.replace("\r","").replace("\n","")
			arr = line.split(" ")
			date = arr[0].split("||")[2]
			priceMap[date] = priceMap.get(date, 0) + int(arr[1]);
			#row = []
			#row.append(arr[1])
			#writer.writerows(arr[1])
			#writer.writelines(arr[1]+"\r\n")
	for i, v in priceMap.items():
		#print(i+" "+str(v//20))
		writer.writelines(str(v//20)+"\r\n")

extractDateSet2(endLine=3120, outFile="YZY350V2-RED-price.csv")

