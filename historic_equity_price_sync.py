from IBgateInterface import interface
import sys
from ticker_loader import smart_update

"""
TODO:
- build pybind11 libraries for env parser
- implement the binded modules
- log errors at a file point
- unbreak loop
- run on server
"""

def main():
    # get file location for ticker_price.csvs --> from .env
    save_file_path = "X:/codeSpace/magi_project/IBgateInterface/"
    price_sync = interface(save_file_path, 30)
    if not price_sync.is_functional:
        print(f"IB Error: {price_sync.ib_error_code}")
        print(f"File Error: {price_sync.file_error_code}")
        sys.exit(1)

    # get file location of ticker list via env --> server error
    ticker_list_file_path = "X:/codeSpace/magi_project/IBgateInterface/company_tickers.csv"

    result_code = smart_update("X:/codeSpace/magi_project/IBgateInterface/", 25)
    if not result_code == 0:
        print(f"file not found: {result_code}")
        sys.exit(1)

    # for each ticker in ticker list, check if exists and if more than x days have passed via interface class --> server error
    # depending on output of above, use interface class to update ticker prices.csv --> IB Gateway error (ticker may not exist)
    with open(ticker_list_file_path, 'r') as f:
        f.readline() # skip header
        for company in f:
            company_ticker = company.rstrip('\r\n').split(',')[1]
            update_status = price_sync.sync(company_ticker)
            if not update_status == 0:
                print(f"{company_ticker}: {update_status}")
            break # break exists so entire list is not loaded

if __name__ == "__main__":
    main()