# IBScrapeSuite
For purposes of automating collection of equity price data via IB Gateway

# dataformat:
Uses CSV:
date | open | high | low | close | volume | average
data is adjusted for splits and dividends 
not entirely sure out of which exchange it is specifically from

## IKBR Limitations (note for self)
-Bars whose size is 30 seconds or less older than six months
-Expired futures data older than two years counting from the future's expiration date.
-Expired options, FOPs, warrants and structured products.
-End of Day (EOD) data for options, FOPs, warrants and structured products.
-Data for expired future spreads
-Data for securities which are no longer trading.
-Native historical data for combos. Historical data is not stored in the IB database separately for combos.; combo historical data in TWS or the API is the sum of data from the legs.
-Historical data for securities which move to a new exchange will often not be available prior to the time of the move.