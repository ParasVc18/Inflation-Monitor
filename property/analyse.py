import pandas as pd
import numpy as np
df = pd.read_csv("Developer/GautamInflation/property/Bangalore/prices.csv", error_bad_lines=False)
def convertible(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False
for index, row in df.iterrows():
    if (row['psf']=="None"):
        row['psf']=np.nan
    elif (row['psf']=="psf"):
        row['psf']=np.nan
row['psf']=float(row['psf'])
if convertible(row['price']):
    row['price']=float(row['price'])
    else:
        row['price']=np.nan
df.dropna()
df['psf']=pd.to_numeric(df['psf'], errors='coerce')
df['price']=pd.to_numeric(df['price'], errors='coerce')
grouped=df.groupby('date')
grouped['psf'].median()
grouped['psf'].std()
grouped['price'].median()
grouped['price'].std()
