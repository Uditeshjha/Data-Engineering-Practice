import pandas as pd
import numpy as np
from utils import load_data as ld
from utils import preprocessing as pp

df = ld.load_data('../data/raw/application_train.csv')
print(df.shape)

# Optimize numeric dtypes
optimized_df = pp.optimize_dataframe(df)
print(optimized_df.shape)  # Should print the shape of the optimized DataFrame

cleaned_df = pp.treat_nulls(optimized_df)
print(cleaned_df.shape)  

outliers = pp.find_outliers_iqr(cleaned_df,['AMT_INCOME_TOTAL'])
print(len(outliers))

#### visualizations
pp.visualize_dataset(df)