<h1 align="center">
  <img
    alt="The TrekReturns logo;"
    height="250"
    src="./img/icon_bull.webp"
  >

  TrekReturns
</h1>
<p align="center"><em>ChatGPT done it's works with this image</em></p>

## Disclaimer
This is not financial advice. All content on this application is information of a general nature and does not address the circumstances of anybody. Any reliance you place on such information is strictly at your own risk.
## Table of Contents

- [What is it?](#what-is-it)

- [How can I run it?](#how-can-i-run-it)

- [How can I help?](#how-can-i-help)

## What is it?
**TrekReturns** is a web app useful for examining how assets behaved in different periods; 
Since we are investors over long time, this isn't a trading tool: we'll examine annualized returns over the rolling period.
Here you can simulate some backtest of your portfolio (or ideal portfolio!) and see how it's gone if you hold it for N years. (obviously, N is variable :smiley: )

<br><br>
You can discover:
- Annualized returns over rolling windows which you decide;
- Some charts about it;
- A few portfolio statistics like mean returns, median returns, standard deviation on the period, max and min return;
- A couple of statistics about the painful side... drawdown. We show max and min drawdown, 10% quartile 5% quartile and so on;
<br><br>
<center><sub><sup>
We use Yahoo Finance (https://finance.yahoo.com/) as a tickers database, but this project isn't part of Yahoo company.
We do not collect or store any data. We provide no guarantee, explicit or implicit, as to the accuracy of the results displayed, which are intended for educational and informational purposes only.
</sup></sub></center>
<br>

## How can i run it?
Go on [TrekReturns.streamlit.app](https://trekreturns.streamlit.app/) to use it online! Registration isn't needed.

(if the project is sleeping, wake it up!)

### run it locally
Clone the repo!

you must have [Docker](https://https://www.docker.com/) installed.
Build Docker image from Dockerfile
```shell
docker build -t TrekReturns .
```
then run the container (the image exposes port 8900)
```shell
docker run --rm -p 8080:8900 TrekReturns
```
Now you can reach it from your web browser on port `8080`


## How can I help?
Feel free to improve! Fork the repo and create a pull request to add some features.
<br>