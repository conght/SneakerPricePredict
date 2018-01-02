# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


df = pd.read_csv("../../spure.csv")

#print(df.head())
#print(df.tail())
#print(df.index)
ticker = df["Ticker"].drop_duplicates()

for i in df.loc[:,["Ticker"]].drop_duplicates().loc[:,"Ticker"]:
	print(i)
