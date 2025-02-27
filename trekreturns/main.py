import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px

#Import functions
from functions import normalize_data
from functions import roll_returns
from functions import sharpe_ratio

st.set_page_config(
    page_title="TrekReturns - For backtesting trends",
    layout="wide",
    initial_sidebar_state="auto",
)


st.title(":blue[_TrekReturns_] - Backtest tool for data-driven retail investor")
st.warning("*Disclaimer: This is not financial advice. All content on this application is information of a general nature and does not address the circumstances of anybody. Any reliance you place on such information is strictly at your own risk.*")
st.write("This tool is useful for examining how assets behaved in different periods.")
st.write("Here, we analyze the distribution rolling returns on a given time.")
st.write("Let's try to answer the final question: *:blue[_How would it have been if I had bought it a while ago?_]*")
st.text("")
# Input tickers, weights, years, and risk-free return
try:
    st.divider()
    st.subheader(":pushpin: Input data")
    st.html("""
                <p>Drop your favorite data. We will search it on <a href="https://finance.yahoo.com/lookup/">Yahoo Finance</a>  <p>
                <p>TIP: Search your ticker (also an index ticker) on Yhaoo Finance website before inserting here: some tickers require the exchange where they are traded!
                """)
    # Tickers Input
    tickers_input = st.text_input("Enter tickers (comma separated)", "AAPL, TSLA")
    tickers = [ticker.upper().strip() for ticker in tickers_input.split(",")]

    # Weights Input
    weights_input = st.text_input("Enter weights (comma separated)", "40, 60")
    try:
        weights = [(float(x.strip())/100) for x in weights_input.split(",")]
    except ValueError:
        st.error(":cry: Invalid weight format. Please enter numbers separated by commas.")
        st.stop()

    # Rolling Return Windows Size Input
    years_input = st.text_input("Enter the rolling return windows size", "8")
    try:
        if years_input is None or years_input == '':
            years_input = 1
        else:
            years_input = int(years_input)
        if years_input < 1 or years_input > 999:
            st.error("C'mon! Please enter a value between 1 and 999.")
            st.stop()
    except ValueError:
        st.error(":cry: Ouch! Invalid input. Please enter a valid number.")
        st.stop()

    # Risk-Free Return Input
    rf_input = st.text_input("Enter the risk-free return (%). We use it for Sharpe ratio", "2")
    try:
        if rf_input is None or rf_input.strip() == '':
            rf_input = 0.0
        else:
            rf_input = float(rf_input)
        if rf_input <= 0 or rf_input >= 100:
            st.error("C'mon!. Risk-free return must be between 0 and 100%.")
            st.stop()
    except ValueError:
        st.error(":cry: Invalid input for risk-free return. Please enter a valid number.")
        st.stop()

    # Validate Tickers
    valid_tickers = []
    for ticker in tickers:
        info = yf.Ticker(ticker).history(period="1mo")
        if not info.empty:
            valid_tickers.append(ticker)
        else:
            st.warning(f"⚠️ Ticker '{ticker}' not found or has no data. It will be ignored.")

    if not valid_tickers:
        st.error("❌ No valid tickers found. Please enter at least one valid ticker.")
        st.stop()

    # Validate Weights
    if len(weights) != len(valid_tickers):
        st.error("❌ Number of weights does not match the number of valid tickers. Please adjust.")
        st.stop()

    if sum(weights) != 1:
        st.error(f"❌ The sum of weights must be 100%. Current sum: {(round(sum(weights), 2)) * 100}%. Please adjust your weights.")
        st.stop()

except Exception as e:
    st.error(":scream: Unexpected exception...")
    #st.error(f"Error: {e}")
    st.stop()


try:
    st.divider()
    data = yf.download(valid_tickers, interval='1mo')["Close"]
    data = data.reindex(valid_tickers, axis=1)
    data.fillna(method="ffill", limit=1, inplace=True)
    st.success(f"Cool!:sunglasses: We got data from **{data.dropna().index[0].strftime("%Y-%m-%d")} to {data.dropna().index[-1].strftime("%Y-%m-%d")}** ")

except Exception as e:
    st.error(":scream: Failed retrieve tickers data...")
    #st.error(f"Error: {e}")
    st.stop()

## normalized data
try:
    st.subheader(":pushpin: Display price normalized data")
    data_normaliz = normalize_data(data)
    data_normaliz

    ## normalized data - chart
    st.write("Now... price chart! You can compare how assets were going through the years.")
    dn_chart=px.line(data_normaliz, title='Price normalization chart')
    dn_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified"
    )
    st.plotly_chart(dn_chart, use_container_width=True)
except Exception as e:
    st.error(":scream: Failed normalized data...")
    #st.error(f"Error: {e}")
    st.stop()

## rolling ret
try:
    portfolio=pd.DataFrame()
    #return each period
    portfolio=roll_returns(portfolio, years_input, data, tickers, weights)

    st.subheader(f":pushpin: Display portfolio :green[annualized return] over {years_input} years")
    st.write("A series of annualized returns by month: Imagine you bought on *start date* and sold on *end period date*, **which annualized return did you get?**")
    st.write("*the 'annualized returns' are already a % value*")
    start_dates = portfolio.index
    end_dates = start_dates + pd.DateOffset(years=years_input)
    returns = (portfolio*100)

    results = pd.DataFrame({
        #"start date": start_dates,
        "end period date": end_dates,
        "% annualized return over period ": returns
    })
    st.dataframe(results)

except Exception as e:
    st.error(":scream: Failed generate rolling returns on data...")
    #st.error(f"Error: {e}")
    st.stop()

## rolling ret - line chart
try:
    rr_chart=px.line(portfolio.dropna(), title="Rolling return chart")
    rr_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Return %",
        hovermode="x unified"
    )
    rr_chart.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
    rr_chart.layout.yaxis.tickformat = ',.0%'
    st.plotly_chart(rr_chart, use_container_width=True)
    
    st.write(f":face_with_monocle: How to read it: on X axis we have the date when we start investing, on Y axis we have the annualized return reached")


    #rolling ret - hist chart
    hist = px.histogram(portfolio.dropna(), 
        opacity=0.4, nbins=120, 
        title="Histogram of Portfolio Returns"
    )
    hist.update_layout(
        xaxis_title="Return",
        yaxis_title="# of times",
        hovermode="x unified"
    )
    hist.add_vline(x=0, line_dash="dash", line_color="red", line_width=2)
    hist.layout.xaxis.tickformat = ',.0%'
    st.plotly_chart(hist, use_container_width=True)

    st.write(f":face_with_monocle: How to read it: On the X axis we have the % return, on the Y axis we have the number of times it happened.")

except Exception as e:
    st.error(":scream: Failed create rolling charts...")
    #st.error(f"Error: {e}")
    st.stop()

## Portfolio Statistics
try:
    st.subheader(f":pushpin: Juicy portfolio statistics over {years_input} years")
    st.write(":yum: Some yummy statistics:")
    st.write("*the 'value' are already a % value*")
    #st.write(portfolio.dropna().describe())
    st.write(
        pd.DataFrame(
            [
                {"Data over period": "number of periods" , "value": portfolio.dropna().describe().iloc[0] },
                {"Data over period": "mean of return", "value": (portfolio.dropna().describe().iloc[1])*100 },
                {"Data over period": "median of return", "value": (portfolio.dropna().describe().iloc[5])*100 },
                {"Data over period": "standard deviation", "value": (portfolio.dropna().describe().iloc[2])*100 },
                {"Data over period": "Max return", "value": (portfolio.dropna().describe().iloc[7])*100 },
                {"Data over period": "Min return", "value": (portfolio.dropna().describe().iloc[3])*100 }
            ]
        )
    )
except Exception as e:
    st.error(":scream: Failed create portfolio statistics...")
    #st.error(f"Error: {e}")
    st.stop()

## Drawdown
try:
    st.subheader(":pushpin: :red[Drawdown] Statistics")
    st.write(":worried: The painful side...")
    st.write("*the 'value' are already a % value*")
    #round(portfolio.dropna().quantile([0.0,0.1])*100,2)
    st.write(
        pd.DataFrame(
            [
                {"Data over period": "max drawdown" , "value": ( round(portfolio.dropna().quantile(0.0)*100,2) ) },
                {"Data over period": "10% quantile", "value": round(portfolio.dropna().quantile(0.1)*100,2)  },
                {"Data over period": "mean return on 10% quantile", "value": round(portfolio.dropna()[portfolio.dropna()<=portfolio.dropna().quantile(0.1)].mean()*100,2)  },
                {"Data over period": "5% quantile", "value": round(portfolio.dropna().quantile(0.05)*100,2)  },
                {"Data over period": "mean return on 5% quantile", "value": round(portfolio.dropna()[portfolio.dropna()<=portfolio.dropna().quantile(0.05)].mean()*100,2)  }
            ]
        )
    )

    st.write(f":face_with_monocle: How to read it: we have the worst case (max drawdown), the return in 10% of worst cases (10% quantile), the return in 5% of worst cases (5% quantile) and the mean return in that case (mean return on quantile) ")
except Exception as e:
    st.error(":scream: Failed calculate drawdown statistics...")
    #st.error(f"Error: {e}")
    st.stop()

## sharpRatio
try:
    st.subheader(":pushpin: Sharpe Ratio")
    st.write(f"Sharpe Ratio over period with risk-free rate of: {rf_input}")

    st.write(f"sharpe ratio: **{ sharpe_ratio( portfolio.dropna().mean(), (rf_input/100) , portfolio.dropna().std() ) }**")


except Exception as e:
    st.error(":scream: Failed create Sharpe ratio...")
    #st.error(f"Error: {e}")
    st.stop()
