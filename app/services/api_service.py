from ..models import Sectors, StockPrice, Symbols
from ..models import StockInfo
from datetime import datetime
import sys
import yfinance as yf


class exec_api:
    def exec_basic_info_api(self):
        symbols = Symbols.objects.all().values_list('symbol', flat=True)
        sectors = Sectors.objects.all().values('sector_id', 'sector_name_en')
        sector_dic = {}
        for sector in sectors:
            sector_dic[sector['sector_id']] = sector['sector_name_en']

        text = ''
        for symbol in symbols:
            text = text + symbol + ','
        
        try:
            tickers = yf.Tickers(text)
            for symbol in symbols:

                if (StockInfo.objects.filter(symbol=symbol).exists()):
                    print(symbol + 'はすでに登録されています')
                    continue
                
                try:
                    ticker = getattr(tickers.tickers, symbol).info
                    print('APIから' + ticker['symbol'] + '取得確認')
                    # sector_dicのvalueからkey(sector_id)を取得
                    sector_id = 0
                    if (ticker['sector'] in sector_dic.values()):
                        sector_id = [k for k, v in sector_dic.items() if v == ticker['sector']][0]
                    
                    stock_info = StockInfo(
                        short_name=ticker['shortName'] if 'shortName' in ticker else 'None',
                        long_name=ticker['longName'] if 'longName' in ticker else 'None',
                        symbol=symbol,
                        sector=ticker['sector'] if 'sector' in ticker else 'None',
                        full_tiime_employees=ticker['fullTimeEmployees'] if 'fullTimeEmployees' in ticker else 0,
                        long_bussiness_summary=ticker['longBusinessSummary'] if 'longBusinessSummary' in ticker else 'None',
                        city=ticker['city'] if 'city' in ticker else 'None',
                        phone=ticker['phone'] if 'phone' in ticker else 'None',
                        state=ticker['state'] if 'state' in ticker else 'None',
                        country=ticker['country'] if 'country' in ticker else 'None',
                        web_site=ticker['website'] if 'website' in ticker else 'None',
                        logo_url=ticker['logo_url'] if 'logo_url' in ticker else 'None',
                        industry=ticker['industry'] if 'industry' in ticker else 'None',
                        currency=ticker['currency'] if 'currency' in ticker else 'None',
                        exchange_time_zone=ticker['exchangeTimezoneShortName'] if 'exchangeTimezoneShortName' in ticker else 'None',
                        quote_type=ticker['quoteType'] if 'quoteType' in ticker else 'None',
                        market=ticker['market'] if 'market' in ticker else 'None',
                        sector_id=sector_id
                    )

                    try:
                        stock_info.save()
                        print(ticker['symbol'] + 'DB登録成功')
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                    continue        
        except Exception as e:
            print(e)

    def exec_daily_price_api(self):
        value = ('stock_info_id', 'symbol')
        target_stocks = StockInfo.objects.all().values(*value)

        text = ''
        for stock in target_stocks:
            text = text + stock['symbol'] + ','

        try:
            tickers = yf.Tickers(text)
            for stock in target_stocks:
                
                stock_price = StockPrice.objects.filter(stock_info_id=stock['stock_info_id'])
                dic = list(stock_price.values())
                if (stock_price.exists() and dic[0]['updated_at'].strftime('%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d')):
                    print(stock['symbol'] + 'はすでに本日の更新があるのでスキップ')
                    continue

                try:
                    ticker = getattr(tickers.tickers, stock['symbol']).info
                    # 最も最近の集計の終値を取得
                    close = getattr(tickers.tickers, stock['symbol']).history(period="min")['Close'].values.tolist()[0]
                    print('APIから' + stock['symbol'] + '取得確認')
                except Exception as e:
                    print(e)
                    continue

                try:
                    StockPrice.objects.update_or_create(
                        stock_info_id=stock['stock_info_id'],
                        defaults={
                            'close' : close if close is not None else 0,
                            'previous_close' : ticker['previousClose'] if 'previousClose' in ticker and ticker['previousClose'] is not None else 0,
                            'open' : ticker['open'] if 'open' in ticker and ticker['open'] is not None else 0,
                            'day_low' : ticker['dayLow'] if 'dayLow' in ticker and ticker['dayLow'] is not None else 0,
                            'day_high' : ticker['dayHigh'] if 'dayHigh' in ticker and ticker['dayHigh'] is not None else 0,
                            'day_diff' : 0,
                            'volume' : ticker['volume'] if 'volume' in ticker and ticker['volume'] is not None else 0,
                            'ask' : ticker['ask'] if 'ask' in ticker and ticker['ask'] is not None else 0,
                            'bid' : ticker['bid'] if 'bid' in ticker and ticker['bid'] is not None else 0,
                            'two_hundred_day_average' : ticker['twoHundredDayAverage'] if 'twoHundredDayAverage' in ticker and ticker['twoHundredDayAverage'] is not None else 0,
                            'fifty_day_average' : ticker['fiftyDayAverage'] if 'fiftyDayAverage' in ticker and ticker['fiftyDayAverage'] is not None else 0,
                            'average_volume_10days' : ticker['averageVolume10days'] if 'averageVolume10days' in ticker and ticker['averageVolume10days'] is not None else 0,
                            'average_volume' : ticker['averageVolume'] if 'averageVolume' in ticker and ticker['averageVolume'] is not None else 0,
                            'price_to_sales_trailling_12months' : ticker['priceToSalesTrailing12Months'] if 'priceToSalesTrailing12Months' in ticker and ticker['priceToSalesTrailing12Months'] is not None else 0,
                            'enterprise_value' : ticker['enterpriseValue'] if 'enterpriseValue' in ticker and ticker['enterpriseValue'] is not None else 0,
                            'enterprise_to_revenue' : ticker['enterpriseToRevenue'] if 'enterpriseToRevenue' in ticker and ticker['enterpriseToRevenue'] is not None else 0,
                            'enterprise_to_ebitda' : ticker['enterpriseToEbitda'] if 'enterpriseToEbitda' in ticker and ticker['enterpriseToEbitda'] is not None else 0,
                            'number_52week_change' : ticker['52WeekChange'] if '52WeekChange' in ticker and ticker['52WeekChange'] is not None else 0,
                            'last_fiscal_year_end' : ticker['lastFiscalYearEnd'] if 'lastFiscalYearEnd' in ticker and ticker['lastFiscalYearEnd'] is not None else 0,
                            'net_income_to_common' : ticker['netIncomeToCommon'] if 'netIncomeToCommon' in ticker and ticker['netIncomeToCommon'] is not None else 0,
                            'most_recent_quarter' : ticker['mostRecentQuarter'] if 'mostRecentQuarter' in ticker and ticker['mostRecentQuarter'] is not None else 0,
                        }
                    )
                    print(stock['symbol'] + 'DB登録成功')
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
