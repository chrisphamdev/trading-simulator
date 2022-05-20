import yfinance as yf


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper()

    def current_price(self):
        stock_info = yf.Ticker(self.symbol).info
        market_price = stock_info['regularMarketPrice']
        return market_price

    def get_full_name(self):
        company_name = yf.Ticker(self.symbol).info['longName']
        return company_name

    def __str__(self):
        return '{} {}'.format(self.company_name, self.symbol)
    
    def __repr__(self):
        return self.__str__()
