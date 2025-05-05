import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = "iframe"

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))

#TSLA stock ticker
Tesla_ticker=yf.Ticker("TSLA")
tesla_data=Tesla_ticker.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

## Question 2: Use Webscraping to Extract Tesla Revenue Data
html_data=requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm").text
soup =BeautifulSoup(html_data,"html.parser")
tesla_revenue = pd.DataFrame(columns=["Year","Revenue"])
for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    year = col[0].text
    revenue = col[1].text
    tesla_revenue = pd.concat([tesla_revenue,pd.DataFrame({"Year":[year],"Revenue":[revenue]})])
tesla_revenue.head()

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',',"").str.replace('$','')
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail(5)

## Question GME: Use yfinance to Extract Stock Data
GME= yf.Ticker("GME")
gme_data=GME.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()

# Use Webscraping to Extract GME Revenue Data
html_data_2=requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html").text
soup = BeautifulSoup(html_data_2,"html.parser")
gme_revenue = pd.DataFrame(columns=["Year","Revenue"])
for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    year = col[0].text
    revenue = col[1].text
    gme_revenue = pd.concat([gme_revenue,pd.DataFrame({"Year":[year],"Revenue":[revenue]})])
gme_revenue.head()
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',',"").str.replace('$','')
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue.tail()

#plot tesla
tesla_revenue=tesla_revenue.rename(columns={'Year': 'Date'})
make_graph(tesla_data,tesla_revenue,'TSLA')
#plot GME
gme_revenue=gme_revenue.rename(columns={'Year': 'Date'})
make_graph(gme_data,gme_revenue,'GME')

