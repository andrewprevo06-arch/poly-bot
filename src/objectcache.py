import httphandler
import json
from datetime import datetime, timezone
import data
import contract
import math

class CachedJSON(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.JSeries = httphandler.getSeries()
            cls._instance.dict = {}
            eventlist = []
            cls._instance.marketList = []
        
            for series in cls._instance.JSeries:
                events = series.get('events', [])
                for event in events:
                    now = datetime.now(timezone.utc)
                    end = datetime.fromisoformat(event.get('endDate').replace('Z', '+00:00'))
                    if event['closed'] == False and now <= end:
                        eventlist.append(event['id'])
        
            for id in eventlist:
                event = httphandler.getEvent(id)
                markets = event.get('markets', [])

                for market_data in markets:
                    mID = market_data['id']
                    question = market_data.get('question', 'N/A') 
                
                    market = httphandler.getMarket(mID)
                
                    cls._instance.marketList.append(market)
                

                # print(f"ID: {mID}, Question: {question}")
        # print(cls.marketList)
        return cls._instance
            
   
class CachedDict():
    _instance = None

    def __new__(cls):
        if not cls._instance:
            
            cls._instance = super().__new__(cls)

            loc = CachedJSON().marketList

            Max = '(HIGH)'
            Min = '(LOW)'
            End = 'over'

            silverMax = []
            silverMin = []
            silverEnd = []
           
            goldMax = []
            goldMin = []
            goldEnd = []

            oilMax = []
            oilMin = []
            oilEnd = []

            silverList = {'Max' : silverMax, 'Min' : silverMin, 'End' : silverEnd }
            goldList = {'Max' : goldMax, 'Min' : goldMin, 'End': goldEnd }
            oilList = {'Max' : oilMax, 'Min' : oilMin, 'End': oilEnd }

            for con in loc:
                if 'Silver' in con['question']:
                    if Max in con['question']:
                        silverMax.append(dict2Contract(con))
                    elif Min in con['question']:
                        silverMin.append(dict2Contract(con))
                    elif End in con['question']:
                        silverEnd.append(dict2Contract(con))
                elif 'Gold' in con['question']:
                    if Max in con['question']:
                        goldMax.append(dict2Contract(con))
                    elif Min in con['question']:
                        goldMin.append(dict2Contract(con))
                    elif End in con['question']:
                        goldEnd.append(dict2Contract(con))
                elif 'Oil' in con['question']:
                    if Max in con['question']:
                        oilMax.append(dict2Contract(con))
                    elif Min in con['question']:
                        oilMin.append(dict2Contract(con))
                    elif End in con['question']:
                        oilEnd.append(dict2Contract(con))
                
            cls._instance.Traded = {'Silver' : silverList, 'Gold' : goldList, 'Oil': oilList}
            #cls._instance = super(CachedDict, cls).__new__(
             #                   cls)
        return cls._instance
        
def dict2Contract(d):
    conID = json.loads(d['clobTokenIds'])
    name = d['question']
    underlying = name.split()[1]
    K = float(d['question'].split('$')[1].split(' ')[0].replace(",", "")) # this might not work
    expiry = datetime.fromisoformat(d['endDate'].replace('Z', '+00:00')).timestamp()
    return contract.Contract(conID, name, underlying, K, expiry)
    
if __name__ == "__main__":
    
    priceMax = 1000000

    cache = CachedDict()
    oilMax = cache.Traded['Oil']['Max']
   
    for con in oilMax:
        value = con.calculate()
        spread = .02
        value_rounded = math.floor(value * 100) / 100
    
        yes_bid = value_rounded - spread  # Buy YES at discount
        yes_ask = value_rounded + spread  # Sell YES at premium
    
        no_bid = (1 - yes_ask)  # Buy NO at discount
        no_ask = (1 - yes_bid)  # Sell NO at premium
        print(f"{con}Value: {value}\nYes Buy: {yes_bid}\nNo Buy: {no_bid}")