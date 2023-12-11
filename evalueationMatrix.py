import pandas as pd

playersInfo = pd.read_csv('data/cleanCsvFiles/playersInfo.csv')
total_null_values = playersInfo.isnull().sum().sum()
total_values = playersInfo.size

print('Total number of null values:', total_null_values)
print('Total number of all values:', total_values)
print('Our model contains ', ((total_values - total_null_values) / total_values) * 100, '% of values and ',
      (total_null_values / total_values) * 100, '% are missing.')
