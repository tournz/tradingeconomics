# Dependencies
import tradingeconomics as te
import pandas as pd
import matplotlib.pyplot as plt

# Constants
TE_API_KEY = 'h4kaciriziudhm8:bsx1onzl7qwee0z'
COUNTRIES = ['Mexico', 'Thailand', 'Sweden', 'New Zealand']
CURRENCY_PAIRS = {'Mexico': 'USD/MXN', 'Thailand': 'USD/THB', 'Sweden': 'USD/SEK', 'New Zealand': 'NZD/SEK'}
INDICATOR = 'currency'
START_DATE = '2010-08-31'
END_DATE = '2020-04-11'

# DF functions:
def simplify_df(input_df, columns, countries):
    return_df = input_df[columns]
    return_df = return_df[return_df['Country'].isin(countries)]
    return return_df

def base_100(input_df, columns):
    for x in columns:
        input_df[x] = input_df[x] * 100 / input_df[x].iloc[0]
    return input_df


# Get the info from Trading Economics:
te.login(TE_API_KEY)
te_data = te.getHistoricalData(country=COUNTRIES, indicator=INDICATOR, initDate=START_DATE, endDate=END_DATE, output_type='df')

# Simplify the dataframe:
simple_df = simplify_df(te_data, ['DateTime', 'Country', 'Value'], COUNTRIES)

print(simple_df)

# Separate into several dataframes:
Mexico = simple_df[simple_df['Country'] == 'Mexico']
Thailand = simple_df[simple_df['Country'] == 'Thailand']
Sweden = simple_df[simple_df['Country'] == 'Sweden']
New_Zealand = simple_df[simple_df['Country'] == 'New Zealand']

# Rename the Value column to the currency pair:
Mexico.rename(columns = {'Value': CURRENCY_PAIRS['Mexico']}, inplace = True)
Thailand.rename(columns = {'Value': CURRENCY_PAIRS['Thailand']}, inplace = True)
Sweden.rename(columns = {'Value': CURRENCY_PAIRS['Sweden']}, inplace = True)
New_Zealand.rename(columns = {'Value': CURRENCY_PAIRS['New Zealand']}, inplace = True)

# Merge the dataframes:
merged_df = pd.merge(Thailand, Mexico, on='DateTime', how='outer')
merged_df = pd.merge(merged_df, Sweden, on='DateTime', how='outer')
merged_df = pd.merge(merged_df, New_Zealand, on='DateTime', how='outer')

# Recalculate the numbers:
final_df = base_100(merged_df, [CURRENCY_PAIRS['Mexico'], CURRENCY_PAIRS['Thailand'], CURRENCY_PAIRS['Sweden'], CURRENCY_PAIRS['New Zealand']])


# Display the graph:
plt.plot(final_df['DateTime'], final_df[CURRENCY_PAIRS['Mexico']], label=CURRENCY_PAIRS['Mexico'])
plt.plot(final_df['DateTime'], final_df[CURRENCY_PAIRS['Thailand']], label=CURRENCY_PAIRS['Thailand'])
plt.plot(final_df['DateTime'], final_df[CURRENCY_PAIRS['Sweden']], label=CURRENCY_PAIRS['Sweden'])
plt.plot(final_df['DateTime'], final_df[CURRENCY_PAIRS['New Zealand']], label=CURRENCY_PAIRS['New Zealand'])
plt.xlabel("Date")  # add X-axis label
plt.xticks(ticks=none, labels=none)
plt.ylabel("Exchange rate - 100 basis")  # add Y-axis label
plt.title("Exchange rates of 4 currencies Vs the US dollar since 08/31/2010")  # add title
plt.legend()
plt.show()
