import black
import data

Max = '(HIGH)'
Min = '(LOW)'
End = 'over'
Above = 'Up'
Below = 'Down'

############## Class Contract ##################

class Contract:
    def __init__(self, conID, name, underlying, K, expiry):
        self.conID = conID
        self.name = name
        self.underlying = underlying
        self.K = K
        self.expiry = expiry
    def __repr__(self):
        return self.name + "\n"
    
    def calculate(self):
        spot = data.getSpot(self.underlying)
        
        K = self.K 

        tenor = black.get_tenor(self.expiry)

        r = 0.045

        sigma = data.getVol(self.underlying)/100

        if Max in self.name:
            if spot >= K:
                return .99
            
            return black.one_touch_barrier_call(spot, K, r, sigma, tenor)
        
        elif Min in self.name:
            if spot <= K:
                return .99
            
            return black.one_touch_barrier_put(spot, K, r, sigma, tenor)
        
        elif Below in self.name:
            return black.cash_or_nothing_call(spot, K, r, sigma, tenor, False)
        
        else:
            return black.cash_or_nothing_call(spot, K, r, sigma, tenor, True)

if __name__ == "__main__":
    print("Getting all contracts")
    con = Contract(21312312, "Gold Up", "Gold", data.get_close('Gold'), 1766458800.0)
    value = con.calculate()
    print(con.expiry)