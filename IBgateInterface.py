from ib_async import *
from pathlib import Path
import datetime as dt
import logging

class interface:
    def __init__(self, filePath, cutOffDays):
        self.is_functional = True
        util.logToConsole(logging.CRITICAL)
        self.current_date = dt.datetime.now()
        self.__file_appendix = "_prices.csv"
        self.__cutOffDays = cutOffDays

        self.ib = IB()
        self.ib_error_code = self.__intialize_ib_gateway()
        if not self.ib_error_code == 0:
            self.is_functional = False

        self.csvSaveFilePath = filePath
        self.file_error_code = self.__validate_file_path(filePath)
        if not self.file_error_code == 0:
            self.is_functional = False

    def __intialize_ib_gateway(self) -> int:
        try:
            self.ib.connect('127.0.0.1', 4001, clientId=1)
            return 0
        except ConnectionError:
            return 301
        except TimeoutError:
            return 302
    
    def __validate_file_path(self, filePath) -> int:
        path = Path(filePath)
        if not path.exists():
            return 101
        return 0

    def sync(self, ticker_symbol) -> int:
        price_file = self.__get_price_file_path(ticker_symbol)
        status = self.__validate_file_path(price_file)
        if not status == 0:
            status = self.__parse_api_data_to_csv(ticker_symbol)
            return status

        if self.__does_file_need_update(ticker_symbol):
            status = self.__parse_api_data_to_csv(ticker_symbol)
            return status
        # does not need update
        return 0

    def __does_file_need_update(self, ticker_symbol) -> bool:
        with open(self.__get_price_file_path(ticker_symbol), 'r') as f:
            headerDate = f.readline().rstrip('\r\n').split(',')[1]
            last_update = dt.datetime.strptime(headerDate, "%m/%d/%Y")
            date_cutoff = self.current_date - dt.timedelta(days=self.__cutOffDays)
            if last_update < date_cutoff:
                return True
            return False

    def __get_price_file_path(self, ticker_symbol) -> str:
        return f'{self.csvSaveFilePath}{ticker_symbol}{self.__file_appendix}'

    def __addFileHeader(self, ticker_symbol):
        stringDate = self.current_date.strftime("%m/%d/%Y")
        with open(self.__get_price_file_path(ticker_symbol), 'w') as f: 
            f.write(f"{ticker_symbol},{stringDate}\n")

    def __parse_api_data_to_csv(self, ticker_symbol):
        stock = Stock(ticker_symbol, 'SMART', 'USD')
        head_time = self.ib.reqHeadTimeStamp(stock, whatToShow='ADJUSTED_LAST', useRTH=False)
        if not head_time:
            return 303
        target_year = head_time.year

        # error check for valid reqHeadTimeStamp first
        self.__addFileHeader(ticker_symbol)

        year_incrments = 10
        index_year = int(self.current_date.year)
        index_month = int(self.current_date.month)
        index_day = int(self.current_date.day)
        index_date = dt.date(index_year, index_month, index_day)

        while True:
            if index_date.year < target_year:
                break
            tenYearChunck = self.ib.reqHistoricalData(
                stock, endDateTime=index_date, 
                durationStr='10 Y',
                barSizeSetting='1 day', 
                whatToShow='TRADES', 
                useRTH=False
            )

            self.__write_chunk_to_csv(tenYearChunck, ticker_symbol)
            index_date = index_date.replace(year=index_date.year - year_incrments)

        return 0

    def __write_chunk_to_csv(self, tenYearChunck, ticker_symbol):
      with open(self.__get_price_file_path(ticker_symbol), 'a') as f: 
        for i in range(len(tenYearChunck) - 1, 0, -1):
            f.write(f"{tenYearChunck[i].date},{tenYearChunck[i].open},{tenYearChunck[i].high},{tenYearChunck[i].low},{tenYearChunck[i].close},{tenYearChunck[i].volume},{tenYearChunck[i].average}\n")
