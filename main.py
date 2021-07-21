import pandas as pd
import matplotlib.pyplot as plt
#Import dataset for project
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
data_sorted=data.sort_values(["Dividend Yield"], ascending=False)
print(data_sorted.head(10))
fig,ax=plt.subplots()
ax.bar(data_sorted.index, data_sorted["Dividend Yield"])
ax.set_xticklabels(data_sorted.index, rotation=90)
ax.set_ylabel("Dividend Yield")
ax.set_title('Dividend Yield by Sector')
plt.tight_layout()
plt.show()