import numpy as np
import pandas as pd
import datetime as dt
import pickle as pk
import TempoQuant as TQ


def updateWatchList(significance=1.5, life=30):

    # 量涨缩踩信号识别
    y = dt.datetime.now().year
    m = dt.datetime.now().month
    d = dt.datetime.now().day
    
    with open("Nasdaq_main.pkl", "rb") as f:
        stock_list = pk.load(f)
        f.close()

    with open("signals.pkl", "rb") as f:
        watches = pk.load(f)
        f.close()

    tq = TQ.TempoQuant()
    #keep only low vol that's not expired
    expired = []
    for stock in watches:
        candle = tq.getDayCandle(stock, y, m, d)
        if candle["vol"] > watches[stock][0]:
            expired += [stock]
        elif (dt.datetime.now() - watches[stock][2]).days > life:
            expired += [stock]
    for stock in expired:
        watches.pop(stock)

    #update new signals
    for stock in stock_list:
        try:
            if tq.isYang(stock, y,m,d) and tq.highVol(stock,y,m,d,significance):
                #print(stock)
                candle = tq.getDayCandle(stock, y,m,d)
                warn = candle["low"]*0.8 + candle["high"]*0.2
                watches[stock] = (candle["vol"],candle["low"],dt.datetime.now())
        except:
            pass

    with open("signals.pkl","wb") as f:
        pk.dump(watches, f)
        f.close()

    return "Update Complete. {} stocks are now in watch list".format(len(watches))



def alert(tolerance=0.005):

    
    with open("signals.pkl", "rb") as f:
        watches = pk.load(f)
        f.close()

    tq = TQ.TempoQuant()
    alerted = []
    for stock in watches:
        try:
            if tq.getPrice(stock) <= watches[stock][1] * (1+tolerance):
                #Alert
                yield "[[Trade Alert]] {} reaches support level {} given {}% tolerance. Mind support downbreak with high volumn.".format(stock, np.round(watches[stock][1],2), tolerance)
                alerted += [stock]
        except:
            pass
    for s in alerted:
        watches.pop(s)
        with open("signals.pkl", "wb") as f:
            pk.dump(watches, f)
            f.close()
