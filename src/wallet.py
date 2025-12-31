import httphandler

class Wallet:
    def __init__(self):
        j = httphandler.getWallet()
        self.availableFunds = j['usdc']
        shares = httphandler.getOrders()
        self.shares = {}
        for con in shares:
            self.shares[con['asset_id']] = con['size']