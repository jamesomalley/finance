# -*- coding: utf-8 -*-
"""

Built using: 
https://www.machinelearningplus.com/machine-learning/portfolio-optimization-python-example/

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Load Data

df = pd.read_csv(r"XXXXXx")
df= pd.DataFrame(df, columns = ['XXXX', 'XXXX', 'XXXX'])

cov_matrix = df.pct_change().apply(lambda x: np.log(1+x)).cov()
corr_matrix = df.pct_change().apply(lambda x: np.log(1+x)).corr()

ind_er = df.pct_change(periods=503).mean()
ann_sd = df.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))


assets = pd.concat([ind_er, ann_sd], axis=1)
assets.columns = ['Returns','Volatility']
print(assets)

p_ret = []
p_vol = []
p_weights = []

num_assets=len(df.columns)
num_portfolios = 1000

for portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights = weights/np.sum(weights)
    p_weights.append(weights)
    returns = np.dot(weights, ind_er)
    
    p_ret.append(returns)
    var = cov_matrix.mul(weights, axis=0).mul(weights,axis=1).sum().sum()
    sd = np.sqrt(var)
    ann_sd = sd*np.sqrt(250)
    p_vol.append(ann_sd)

data = {'Returns':p_ret, 'Volatility':p_vol}

for counter, symbol in enumerate(df.columns.tolist()):
    data[symbol+'weight'] = [w[counter] for w in p_weights]

portfolios = pd.DataFrame(data)
rf = 0.01
optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]
print(optimal_risky_port)    

#Plot Optimal Portfolio
plt.subplots(figsize=(10,10))
plt.scatter(portfolios['Volatility'], portfolios['Returns'], marker='o', s=10, alpha=0.3)
plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)

