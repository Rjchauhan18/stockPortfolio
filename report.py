import numpy as np
import pandas as pd
import yfinance as yf
import riskfolio as rp
import matplotlib.pyplot as plt

# yf.pdr_override()

# Date range

def download_report(tickers, start, end):
    
    tickers.sort()

    # Downloading the data
    data = yf.download(tickers, start = start, end = end)
    data = data.loc[:,('Adj Close', slice(None))]
    data.columns = tickers
    assets = data.pct_change().dropna()

    Y = assets

    # Creating the Portfolio Object
    port = rp.Portfolio(returns=Y)

    # To display dataframes values in percentage format
    pd.options.display.float_format = '{:.4%}'.format

    # Choose the risk measure
    rm = 'MV'  # Standard Deviation

    # Estimate inputs of the model (historical estimates)
    method_mu='hist' # Method to estimate expected returns based on historical data.
    method_cov='hist' # Method to estimate covariance matrix based on historical data.

    port.assets_stats(method_mu=method_mu, method_cov=method_cov)

    # Estimate the portfolio that maximizes the risk adjusted return ratio
    w = port.optimization(model='Classic', rm=rm, obj='Sharpe', rf=0.0, l=0, hist=True)


    ax = rp.jupyter_report(assets,
                        w,
                        rm='MV',
                        rf=0,
                        alpha=0.05,
                        height=6,
                        width=14,
                        others=0.05,
                        nrow=25)
    
    fig = ax.get_figure()
    
    return fig

    # ax.figure.savefig('stockPortfolio/output/efficient_frontier.png', dpi=300, bbox_inches='tight')

