from ib_async import *
import datetime as dt
import sys

"""
Responsibilities of this code

Handles the interactions with IB Gateway to fetch historic data
of a specifc contract. Also handles the timing?

TODO:
- Build aux program to handle authentication
- When run without arguments, have it run through a csv of tickers to load/update
- How aux program handle downloading tickers from sec into a csv for program to use
- use env to load file paths
- have file path direction
- Save when updated 
- Create header file for this function
- have ability to look up when last updated
- when running a second time, copy file contents, add up till last update point and repaste old contents
"""
def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} [ticker] [--options]")
        sys.exit(1)

    stockTicker = sys.argv[1]
    options = sys.argv[2]

    if not (options[0] == "-") or not (options[1] == "-"):
        print(f"Usage: python3 {sys.argv[0]} [ticker] [--options]")
        sys.exit(1)

    current_date = dt.datetime.now()
    # check for ticker here, if ticker hasn't been update since last month -- update, unless force update
    returnMaxStockChart(stockTicker)

# get stock prices as far back as possible
# adjusted for dividends and stock splits
def returnMaxStockChart(ticker):
    ib = IB()
    try:
        ib.connect('127.0.0.1', 4001, clientId=1)
    except ConnectionError:
        print("IB Gateway not functioning")
        sys.exit(1)
    except TimeoutError:
            print("Timed Out")
            sys.exit(2)

    stock = Stock(ticker, 'SMART', 'USD')
    current_date = dt.datetime.now()
    target_year = ib.reqHeadTimeStamp(stock, whatToShow='ADJUSTED_LAST', useRTH=False).year

    year_incrments = 10
    index_year = int(current_date.year)
    index_date = dt.date(index_year, 1, 1)

    while True:
        if index_date.year < target_year:
                    break
        tenYearChunck = ib.reqHistoricalData(
            stock, endDateTime=index_date, 
            durationStr='10 Y',
            barSizeSetting='1 day', 
            whatToShow='TRADES', 
            useRTH=False
        )
        chunkToCSV(tenYearChunck, ticker)
        index_date = index_date.replace(year=index_date.year - year_incrments)

# probably should make with filepath in mind
def chunkToCSV(tenYearChunck, ticker):
      with open(f"{ticker}.csv", 'a') as f: 
        for i in range(len(tenYearChunck) - 1, 0, -1):
            f.write(f"{tenYearChunck[i].date},{tenYearChunck[i].open},{tenYearChunck[i].high},{tenYearChunck[i].low},{tenYearChunck[i].close},{tenYearChunck[i].volume},{tenYearChunck[i].average}\n")

if __name__ == "__main__":
    main()