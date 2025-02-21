import numpy as np
import pandas as pd

#normalized data: start from '100'
def normalize_data(dati):
    return 100 * dati.dropna() / dati.dropna().iloc[0]

#rolling returns with sliding window
def roll_returns(ptf,years, dati, tickers, weights):
    components = dati[tickers].dropna()
    performance = (components.shift(-12*years)/components)**(1/years)-1
    performance_idx = pd.DataFrame( np.dot(performance,weights), index=performance.index, columns=["ptf"] )
    ptf["ptf"] = performance_idx.dropna()
    return (ptf["ptf"])

#sharpe ratio
def sharpe_ratio( avg_ret, free_rate, std ):
    return round(  (( avg_ret  -  free_rate ) / std )*100  ,3)

