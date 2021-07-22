import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#Import dataset for project
import requests

data=pd.read_csv("Financials (3).csv")
print(data.head())
print(data.describe())
#Check for duplicates
missing_values_count=data.isnull().sum()
print(missing_values_count)
#Only duplicates are in P/E and Price/Book columns.
#If duplicates were on Name column the duplicate would be dropped
print(data.shape)
data.drop_duplicates(subset="Name")
print(data.shape)
#I am not interested in the Market Cap and EBITDA columsn so these will be dropped
data.drop(['Market Cap', 'EBITDA'], axis=1, inplace=True)
print(data.shape)
#Can see now that columns have decreased from 14 to 12.
#I would like to see the comparative Euro price by using a function to translate the price from USD to Dollar using rate 0.85
def convert_to_euro(x):
    return x *0.85
#Add this as a new column to dataset
data['Price Euro']=data['Price'].map(convert_to_euro)
print(data.shape)
print(data.head)
#Column added to dataset
#Getting data ready for visualisations using sorting and setting index
data=data.set_index("Sector").sort_values("Sector")
print(data["Dividend Yield"])
print(data.columns.tolist())
#add column "52 week movement" to see how much the share price has moved during the year
data["52 Week Movement"]=(data["52 Week High"]-data["52 Week Low"])/data["52 Week Low"]
print(data.columns.tolist())
for index, row in data.iterrows():
    print(row['Name'],row['52 Week Movement'])
data_dvd_yield=data.groupby("Sector")["Dividend Yield"].mean()\
    .reset_index(name="Average Dividend Yield")
data_dvd_yield=data_dvd_yield.set_index("Sector")
print(data_dvd_yield.head(10))
fig,ax=plt.subplots()
ax.bar(data_dvd_yield.index, data_dvd_yield["Average Dividend Yield"])
ax.set_xticklabels(data_dvd_yield.index, rotation=90)
ax.set_ylabel("Average Dividend Yield")
ax.set_title('Average Dividend Yield by Sector')
plt.tight_layout()
plt.show()
#keep just the top ten dividend yield companies to compare stock prices to latest from Alpha Vantage
data_sorted=data.sort_values(["Dividend Yield"], ascending=False)
print(data_sorted[['Name','Dividend Yield']].head(10))
data_sorted_10=data_sorted[0:10]
print(data_sorted_10)
my_api_list=['CTL', 'KIM','IRM','F','SCG']
print(my_api_list)
import alpha_vantage
import json
API_URL="https://www.alphavantage.co/query"
symbols=my_api_list
print(symbols)
for symbol in symbols:
    data = {
        "function":"Global_Quote",
        "symbol": symbol,
        "apikey": "F8GHV69N64XWSFKT",
    }
    response = requests.get(API_URL, params=data)
    print(response.json())
#Create a new DataFrame which lists the top 5 companies and the Current Price as obtained from Alpha Vantage
data_api=[
    {"Symbol":"CTL", "AV Current Price":"12.85"},
    {"Symbol":"KIM", "AV Current Price":"21.25"},
    {"Symbol":"IRM", "AV Current Price":"43.89"},
    {"Symbol":"F", "AV Current Price":"14.19"},
    {"Symbol":"SCG", "AV Current Price":"47.78"}
]
data_api_new=pd.DataFrame(data_api)
print(data_api_new)
#Merge data_sorted_10 and data_api_new on Symbol
data_merged=data_sorted_10.merge(data_api_new, on="Symbol")
print(data_merged)
fig1,ax1=plt.subplots()
ax1.plot(data_merged["Name"], data_merged["Price"], color='blue')
ax1.set_xticklabels(data_merged["Name"], rotation=90)
ax1.set_ylabel('Original Price', color='blue')
ax1.tick_params('y', colors='blue')
ax1.set_title('Comparison of Current Price (per AV) vs. Original Price (per Dataset')
ax2=ax1.twinx()
ax2.plot(data_merged["Name"], data_merged["AV Current Price"], color='red')
ax2.set_ylabel('AV Current Price', color ='red')
ax2.tick_params('y', colors='red')
plt.tight_layout()
plt.show()

