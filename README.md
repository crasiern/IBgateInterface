# IBGateInterface\*
For purposes of automating collection of equity price data via IB Gateway

\* Program needs a new name

## Dataformat:

[ticker_symbol],[last_update_date]\
[date],[open]\*,[high]\*,[low]\*,[close]\*,[volume],[average]\
[repeat above until first trade date]

\* data is adjusted for splits and dividends 

## Usage:
Code will produce files in three seperate locations: The first will be the csv files in the "save_path" directory [see below], where the historic prices of each equity is saved in the form of [ticker]_prices.csv. The second will be at the "ticker_list_path" directory, company_tickers.csv, which is the csv version of the SEC's company_tickers.json found [here](https://www.sec.gov/file/company-tickers). This file is important because the program loads the tickers from it to query price histories. As of yet, there is no way to select indiviudal or desired groups of securities, it is all or nothing based on this file. My recommendation is to follow the format in the csv and edit the file yourself if you only care about a small handful of securities. Be mindful of the commas and the header. The final file is found at the "log_error_path" directory. There, "errors.log" logs every error the program encounters, along with a timestamp and the corresponding error produced. This log can be used to deduce what went wrong with the program, and is espcially useful in determining which, if any, securities were skipped in the updating process. 

## Error Codes:
100 -> Internal Error

200 -> Server/File Error
    101 = csvSaveFilePath is not valid

300 -> IB Gateway Error
    301 = ConnectionError
    302 = TimeoutError
    303 = no header time

## Config:
This program uses a "config.toml" file to properly configue settings and file paths. Please ensure that directory paths end with '/'. Nothing in the code will enforce this rule, it will just break. 

### Structure of config.toml:

[directory_paths]
save_path = 
ticker_list_path = 
log_error_path = 

[file_names]
ticker_file = "company_tickers.csv"
log_file = "errors.log"

[misc]
cutOffDays = 

## TODO:
- Rename files and repo to something more appropriete
- Debug issues found in errors.log
- log more specific errors and events (like start, stop, and cancelled(?))
- find ways to update individual or groups of securities
- use async functions to load multiple tickers at a time 
- implement a progress bar type system in console
- at present, program is quite slow. Back of math calculations predict that it would take a full work week of ~37 hours to load price data for every single ticker listed.

## Dependencies
Program uses a c module I built called smart_update from ticker_loader. This module handles the management of the company_tickers.csv file. To use, visit github repo [here](https://github.com/crasiern/ticker_loader).

