import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import openpyxl
import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path

#############################################################################
# Import data
#############################################################################
spot = pd.read_excel('SPOT_data.xlsx', engine='openpyxl')
NDBC = pd.read_csv('NDBC2.csv')
NDBC = NDBC.iloc[1: , :] #get rid of first row (this row only contains header units)

###############################################################################
# Extract time, signifcant wave height, mean period, and peak direction from dataframe
###############################################################################
spot_wave = spot[['Date/Time', 'Significant Wave Height (m)',
	 'Mean Period (s)', 'Peak Direction (deg)']]

NDBC_wave = NDBC[['#YY', 'MM', 'DD', 'hh', 'mm', 'WVHT', 'APD', 'MWD']]

################################################################################
# Convert data to match w.r.s.t date and time
#	* Dates are from 4/05/21 - 12/31/2021
#	* NDBC data is only valid for each 40min of an hour 
#		- 7 of these pts are invalid too and were filled via interpolation
#	* Spotter data is measured each 20min and 50min of every hour
#		- spotter data was interpolated to 40min of each hour
################################################################################

#convert dates to type datetime
spot_wave = spot_wave.assign(Dates = pd.to_datetime(spot_wave['Date/Time']))
spot_wave.Dates = spot_wave.Dates.apply(lambda t: t.replace(second=0))
spot_wave.drop('Date/Time', axis = 1, inplace=True)

NDBC_wave['Dates'] = NDBC_wave['#YY'].astype(str) +'-' \
	+ NDBC_wave['MM'].astype(str) + '-' \
	+ NDBC_wave['DD'].astype(str) + ' ' \
	+ NDBC_wave['hh'].astype(str) +':'  \
	+ NDBC_wave['mm'].astype(str) + ":00"

NDBC_wave['Dates'] = pd.to_datetime(NDBC_wave['Dates'])
NDBC_wave.drop('#YY', axis = 1, inplace=True)
NDBC_wave.drop('MM', axis = 1, inplace=True)
NDBC_wave.drop('DD',  axis = 1, inplace=True)
NDBC_wave.drop('hh', axis = 1, inplace=True)
NDBC_wave.drop('mm', axis = 1, inplace=True)

#align dataframes to same days
NDBC_wave = NDBC_wave.loc[(NDBC_wave.Dates.dt.date > pd.to_datetime('2021-04-05'))
	& (NDBC_wave.Dates.dt.date <= pd.to_datetime('2021-12-31'))]

spot_wave = spot_wave.loc[(spot_wave.Dates.dt.date > pd.to_datetime('2021-04-05'))
	& (spot_wave.Dates.dt.date <= pd.to_datetime('2021-12-31'))]

#cast columns as type float and make Dates column the index
NDBC_wave = NDBC_wave.astype({'WVHT': 'float', 'APD':'float', 'MWD':'float'})
NDBC_wave = NDBC_wave.set_index('Dates')

spot_wave = spot_wave.astype({'Significant Wave Height (m)' : 'float',
	 'Mean Period (s)': 'float', 'Peak Direction (deg)' : 'float'})
spot_wave = spot_wave.set_index('Dates')

#align dataframe to the same minute
spot_forty = spot_wave.resample('10T').asfreq()
spot_forty = spot_forty.interpolate(method = 'linear')
spot_forty = spot_forty.loc[(spot_forty.index.minute == 40)]

NDBC_wave = NDBC_wave.loc[(NDBC_wave.index.minute == 40)] #NDBC only has valid data at each 40min 
NDBC_wave = NDBC_wave.merge(spot_forty, how = 'right', right_index = True, left_index = True)
NDBC_wave.drop(['Significant Wave Height (m)', 'Mean Period (s)', 'Peak Direction (deg)'], \
	axis = 1, inplace=True)

#Interpolate missing values 
NDBC_wave['WVHT'] = NDBC_wave['WVHT'].apply(lambda x: np.NaN if x >= 99 else x)
NDBC_wave = NDBC_wave.interpolate(method = 'linear')

NDBC_wave['APD'] = NDBC_wave['APD'].apply(lambda x: np.NaN if x >= 99 else x)
NDBC_wave = NDBC_wave.interpolate(method = 'linear')

NDBC_wave['MWD'] = NDBC_wave['MWD'].apply(lambda x: np.NaN if x >= 999 else x)
NDBC_wave = NDBC_wave.interpolate(method = 'linear')

###############################################################################
# Export cleaned dataframes as .csv
###############################################################################

NDBC_wave.to_csv('NDBC_Cleaned.csv')
spot_forty.to_csv('Spotter_Cleaned.csv')
