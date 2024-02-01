import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
import os

def stationary_test(data, col, significance):
    result = adfuller(data[col])
    print(f'Test Statistics: {result[0]}')
    print(f'p-value: {result[1]}')
    print(f'cristical_values: {result[4]}')

    if result[1] > significance:
        print("Series is not stationary")
    else:
        print("Series is stationary")

###############################################################
# Import data
#   * Data is merged for granger test
##############################################################
spotter = pd.read_csv('Spotter_Cleaned.csv')
NDBC = pd.read_csv('NDBC_Cleaned.csv')

NDBC['Dates'] = pd.to_datetime(NDBC['Dates'])
spotter['Dates'] = pd.to_datetime(spotter['Dates'])

spotter = spotter.set_index('Dates')
NDBC = NDBC.set_index('Dates')

df = pd.merge(spotter, NDBC, left_index = True, right_index = True)
significance = 0.05
lag = 4
##################################################################
# Simple menu so I did not have to change function inputs and run
# the script for every test or alteration
##################################################################
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Menu Options")
    print("1) Stationary Test")
    print("2) Granger Causality Test")
    print("Type 'exit' to close script")
    user_text = input()
    
    if user_text == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Select data to test")
        print("SPOTTER BOUY OPTIONS")
        print("1) Significant Wave Height (m)")
        print("2) Mean Period (s)")
        print("3) Peak Direction (deg)")
        print("NDBC BOUY OPTIONS")
        print("4) WVHT")
        print("5) APD")
        print("6) MWD")
        print("Type 'main' to return to main menu or 'exit' to leave")
        user_text = input()

        if user_text == '1':
            stationary_test(spotter, 'Significant Wave Height (m)', significance)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == '2':
            stationary_test(spotter, 'Mean Period (s)', significance)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == '3':
            stationary_test(spotter, 'Peak Direction (deg)', significance)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == '4':
            stationary_test(NDBC, 'WVHT', significance)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == '5':
            stationary_test(NDBC, 'APD', significance)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == '6':
            stationary_test(NDBC, 'MWD', significance)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == 'exit':
            break
        elif user_text == 'main':
            continue
    elif user_text == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Select data to test")
        print("SPOTTER BOUY OPTIONS")
        print("1) Significant Wave Height (m)")
        print("2) Mean Period (s)")
        print("3) Peak Direction (deg)")
        print("Type 'main' to return to main menu or 'exit to leave")
        user_text = input()
        
        if user_text == '1':
            print("GRANGER WVHT VS SIGNIFICANT WAVE HEIGHT")
            grangercausalitytests(df[['WVHT', 'Significant Wave Height (m)']], maxlag=lag)
            print("GRANGER SIGNIFICANT WAVE HEIGHT VS WVHT")
            grangercausalitytests(df[['Significant Wave Height (m)','WVHT']], maxlag=lag)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == '2':
            print("GRANGER APD VS MEAN PERIOD")
            grangercausalitytests(df[['APD', 'Mean Period (s)']], maxlag=lag)
            print("GRANGER MEAN PERIOD VS APD")
            grangercausalitytests(df[['Mean Period (s)', 'APD']], maxlag=lag)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == '3':
            print("GRANGER MWD VS PEAK DIRECTION (DEG)")
            grangercausalitytests(df[['MWD', 'Peak Direction (deg)']], maxlag=lag)
            print("GRANGER PEAK DIRECTION (DEG) VS MWD")
            grangercausalitytests(df[['Peak Direction (deg)', 'MWD']], maxlag = lag)
            print("Hit enter to return to main menu")
            user_text = input()
        elif user_text == 'exit':
            break
        elif user_text == 'main':
            continue
    elif user_text.lower() == 'exit':
        break

