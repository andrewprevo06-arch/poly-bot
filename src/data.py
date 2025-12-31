import yfinance as yf

gold_ticker = yf.Ticker("GC=F")
silver_ticker = yf.Ticker("SI=F")
oil_ticker = yf.Ticker("CL=F")
gvz_ticker = yf.Ticker("^GVZ")
vxslv_ticker = yf.Ticker("^VXSLV")
ovx_ticker = yf.Ticker("^OVX")


def get_gold():
    info = gold_ticker.info
    current_price = info['regularMarketPrice']
    return current_price

def get_silver():
    info = silver_ticker.info
    current_price = info['regularMarketPrice']
    return current_price

def getSpot(ul):
    if ul == "Gold":
        data = gold_ticker.info
        spot = data['regularMarketPrice']
        return spot
    elif ul == "Silver":
        data = silver_ticker.info
        spot = data['regularMarketPrice']
        return spot
    else:
        data = oil_ticker.info
        spot = data['regularMarketPrice']
        return spot

def getVol(ul):
    if ul == "Gold":
        vol = gvz_ticker.info
        return vol['regularMarketPrice'] 
    elif ul == "Silver":
        vol = vxslv_ticker.info
        return vol['regularMarketPrice'] 
    else:
        vol = ovx_ticker.info
        return vol['regularMarketPrice'] 





if __name__ == "__main__":

    print(f"Oil Spot: {getSpot('Oil')}")
    print(f"Oil Vol: {getVol('Oil')}\n")
    print(f"Gold Spot: {getSpot('Gold')}" )
    print(f"Gold Vol: {getVol('Gold')}\n")
    print(f"Silver Spot: {getSpot('Silver')}")
    print(f"Silver Vol: {getVol('Silver')}\n")
