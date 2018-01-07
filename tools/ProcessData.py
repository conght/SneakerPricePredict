# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime

def parseDate(x):
	return datetime.strptime(x, '%A, %B %d, %Y')

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

AJ5_Need_Replace_Ticker = []
AM1_Need_Replace_Ticker = []

df_tmp = df[~ df.Ticker.isin(tickers)]
for index, row in df_tmp.iterrows():
	if row["Ticker"].split("-")[0] == "AJ5":
		#AJ5_Need_Replace_Ticker.append(row["Ticker"])
		df[index,"Ticker"] = "AJ5-MTSLV16"
	elif row["Ticker"].split("-")[0] == "AM1":
		#AM1_Need_Replace_Ticker.append(row["Ticker"])
		df[index,"Ticker"] = "AM1-RYL17"

df['c'] = df['a'].map(lambda x: x+1)
#for i in AJ5_Need_Replace_Ticker:
#	df.replace(i, "AJ5-MTSLV16")

#for i in AM1_Need_Replace_Ticker:
#	df.replace(i, "AM1-RYL17")

print(df[~ df.Ticker.isin(tickers)])

#extracte date
date = []
for i in df.loc[:,["Date"]].drop_duplicates().loc[:,"Date"]:
	date.append(i)

for i in date:
	#print(df[df.Date == i])
	pass


