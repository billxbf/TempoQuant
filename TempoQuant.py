import numpy as np
import yfinance as yf
import datetime as dt

class TempoQuant():
    def __init__(self):
        pass

    def getPrice(self, stock):
        try:
            price = yf.Ticker(stock).history(interval="1m", period="1d").iloc[-1]["Close"]
        except:
            price = -1
        return price 
    
    def getDayCandle(self,stock, y, m, d):
        df = yf.Ticker(stock).history(interval="1d", start=dt.datetime(y,m,d), end=dt.datetime(y,m,d+1))
        out = {'open':df.Open[0],
               'high':df.High[0],
               'low':df.Low[0],
               'close':df.Close[0],
               'vol':df.Volume[0]}
        return out
    
    def getDayCandleAfter(self,stock, y, m, d, interval):
        df = yf.Ticker(stock).history(interval="1d", start=dt.datetime(y,m,d))
        df = df[:interval+1]
        out = {'open': np.array(df.Open),
               'high':np.array(df.High),
               'low':np.array(df.Low),
               'close':np.array(df.Close),
               'vol':np.array(df.Volume)}
        return out

    def getDayCandleBefore(self,stock, y, m, d, interval):
        df = yf.Ticker(stock).history(interval="1d",end=dt.datetime(y,m,d+1))
        df = df[-(interval+1):]
        out = {'open': np.array(df.Open),
               'high':np.array(df.High),
               'low':np.array(df.Low),
               'close':np.array(df.Close),
               'vol':np.array(df.Volume)}
        return out

    def isYang(self, stock, y, m, d):
        candle = self.getDayCandle(stock, y, m, d)
        return candle['close'] > candle['open']
    
    def highVol(self, stock, y, m, d, significance = 1.0):
        his = self.getDayCandleBefore(stock, y, m, d, 5)
        vols = his['vol']
        bodies = np.abs(his['close']-his['open'])
        ma_vol = np.mean(vols[:-1])
        ma_body = np.mean(bodies[:-1])
        if vols[-1]>vols[-2] and vols[-1] > significance*ma_vol and bodies[-1] > significance*ma_body:
            return True
        return False
        