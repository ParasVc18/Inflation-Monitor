import pandas as pd
import numpy as np
df = pd.read_csv("Developer/GautamInflation/foods/Gurugram/food/food.csv", error_bad_lines=False)
for index, row in df.iterrows():
    if (row['date']=="date"):
        row['date']=np.nan
df=df.dropna()
ddf= df[df["price"]!=0]
ddf['price']=pd.to_numeric(df['price'], errors='coerce')
grouped=ddf.groupby('date')
print(grouped['price'].mean())
print(grouped['price'].std())
