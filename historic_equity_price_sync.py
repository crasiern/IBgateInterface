from IBgateInterface import interface
import sys
import tomllib
from ticker_loader import smart_update
from datetime import datetime

def main():
    with open("config.toml", "rb") as config:
        settings = tomllib.load(config)

    logger = error_logger(f"{settings["directory_paths"]["log_error_path"]}{settings["file_names"]["log_file"]}")

    price_sync = interface(settings["directory_paths"]["save_path"], 30)
    if not price_sync.is_functional:
        logger.log_connection_error(price_sync.ib_error_code, price_sync.file_error_code)
        sys.exit(1)

    csv_dir = settings["directory_paths"]["ticker_list_path"]
    result_code = smart_update(csv_dir, settings["misc"]["cutOffDays"])
    if not result_code == 0:
        logger.log_file_error(csv_dir, result_code)
        sys.exit(1)

    ticker_list_file_path = f"{csv_dir}{settings["file_names"]["ticker_file"]}"

    with open(ticker_list_file_path, 'r') as f:
        f.readline() # skip header
        for company in f:
            company_ticker = company.rstrip('\r\n').split(',')[1]
            update_status = price_sync.sync(company_ticker)
            if not update_status == 0:
                logger.log_ticker_error(company_ticker, update_status)
           # break # break exists so entire list is not loaded

class error_logger:
    def __init__(self, file_path):
        self.file_path = file_path

    def __time_stamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_connection_error(self, ib_error, file_error):
        with open(self.file_path, 'a') as f:
            f.write(f"At {self.__time_stamp()}: Connection Error! IB Error: {ib_error}; File Error: {file_error}\n")

    def log_ticker_error(self, ticker, error):
        with open(self.file_path, 'a') as f:
            f.write(f"At {self.__time_stamp()}: {ticker} has error {error}\n")

    def log_file_error(self, file, error):
        with open(self.file_path, 'a') as f:
            f.write(f"At {self.__time_stamp()}: {file} has error {error}\n")

if __name__ == "__main__":
    main()