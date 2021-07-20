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
#show bar chart of average dividend yield by sector
fig,ax=plt.subplots()
ax.bar(data.index, data["Dividend Yield"].mean())
for label in ax.get_xticklabels():
    label.set_ha("right")
    label.set_rotation(45)
plt.show()
