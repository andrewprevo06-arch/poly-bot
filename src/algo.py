import contract
import httphandler
import time
import math
import order
import threading


class Algo:
    def __init__(self, conList, pLimit, spread, timer, name):
        self.conList = conList
        self.pLimit = pLimit
        self.spread = spread
        self.timer = timer
        self.name = name
        self.running = True
        self.timestamp = time.localtime()
    def __repr__(self):
        return '<Algo Object: ' + self.name + '>'
    
    def start(self):
        self.running = True
        self.algo()
    def stop(self):
        self.running = False
    def setTimer(self, timer):
        self.timer = timer
    def setLimit(self, limit):
        self.pLimit = limit
    def setSpread(self, spread):
        self.spread = spread

    def algo(self):
        i = 1
        while True:
            try:
                self.timestamp = time.localtime()
                orderList = []
                cancelList = []
                jList = httphandler.getOrders()
                for con in self.conList:
                    print(con.name)
                    oldBuy = None
                    oldSell = None
                    for j in jList:
                        if j['asset_id'] == con.conID[0] or j['asset_id'] == con.conID[1]:
                            if j['outcome'] == 'YES':
                                oldBuy = j
                            if j['outcome'] == 'NO':
                                oldSell = j
                    value = con.calculate()   
                    buy = (math.floor(value * 100) / 100) - self.spread
                    sell = 1 - ((math.floor(value * 100) / 100) + self.spread)

                    if oldBuy == None and oldSell == None:
                        bidAmt = self.pLimit
                        askAmt = self.pLimit
                    elif oldBuy == None:
                        bidAmt = self.pLimit
                        askAmt = oldSell['original_size'] - oldSell['size_matched']
                    elif oldSell == None:
                        bidAmt = oldBuy['original_size'] - oldBuy['size_matched']
                        askAmt = self.pLimit
                    else:
                        if oldBuy['original_size'] - oldBuy['size_matched'] >=  oldSell['original_size'] - oldSell['size_matched']:
                            bidAmt = self.pLimit
                            askAmt = self.pLimit - abs((oldBuy['original_size'] - oldBuy['size_matched']) - (oldSell['original_size'] - oldSell['size_matched']))
                        else:
                            bidAmt = self.pLimit - abs((oldBuy['original_size'] - oldBuy['size_matched']) - (oldSell['original_size'] - oldSell['size_matched']))
                            askAmt = self.pLimit
                    print("[VALUE]" + " " + str(value))   
                    print("[BID]" + " " + str(bidAmt) + " Price " + str(buy))

                    if (oldBuy == None or buy != oldBuy['price']) and buy > 0 and buy < 1:
                        if oldBuy != None:
                            cancelList.append(oldBuy['id'])
                        orderList.append(order.Order(con.conID[0], 'BUY', bidAmt, buy))
                    if (oldSell == None or sell != oldSell['price']) and sell > 0 and sell < 1:
                        if oldSell != None:
                            cancelList.append(oldSell['id'])
                        orderList.append(order.Order(con.conID[1], 'BUY', askAmt, sell))

                cancelstr = order.cancel2str(cancelList)
                print(cancelstr)
                orderstr = order.order2str(orderList)
                print(orderstr)
                print(time.localtime())
                if cancelList:
                    httphandler.postCancelOrders(cancelList)
                if orderList:
                    httphandler.postAddOrders(orderList)
            except Exception as e:
                print("==================================")
                print(e)
                print("==================================")
            
            time.sleep(self.timer)
            i = i + 1