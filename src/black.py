import math
import time
from scipy.stats import norm


days_year = 252 # or 252, 365
time_year = days_year * 24 * 60 * 60
time_year = float(time_year)

def get_tenor(time_close):
    return (time_close - time.time())/time_year

########################## Finance Stuff ##########################

def cash_or_nothing_call(S, K, r, sigma, tenor, isCall):
    # S: Asset Price
    # K: Strike Price
    # r: risk free rate (3.8 for treasuries)
    # sigma: annualized volatility
    # tenor: time to maturity in years

    d1 =(math.log(S / K) + (r + 0.5 * sigma * sigma) * tenor) / (sigma * math.sqrt(tenor))
    d2 = d1 - sigma * math.sqrt(tenor)
    if isCall:
        return math.pow(math.e, -r * tenor) * norm.cdf(d2)
    else:
        return math.pow(math.e, -r * tenor) * norm.cdf(-d2)


def one_touch_barrier_call(S, H, r, sigma, tenor):
    """
    Probability of touching barrier H from below
    Uses reflection principle with time dependence
    """
    if S >= H:
        return 1.0
    
    if tenor <= 0:
        return 0.0
    
    mu = r - 0.5 * sigma**2
    
    h = math.log(H / S)
    
    sigma_sqrt_t = sigma * math.sqrt(tenor)
    
    d1 = (h - mu * tenor) / sigma_sqrt_t
    d2 = (h + mu * tenor) / sigma_sqrt_t
    
    value = norm.cdf(-d1) + math.exp(2 * mu * h / (sigma**2)) * norm.cdf(-d2)
    
    return value


def one_touch_barrier_put(S, L, r, sigma, tenor):
    """
    Probability of touching barrier L from above
    Uses reflection principle with time dependence
    """
    if S <= L:
        return 1.0
    
    if tenor <= 0:
        return 0.0
    
    mu = r - 0.5 * sigma**2
    h = math.log(S / L)
    sigma_sqrt_t = sigma * math.sqrt(tenor)
    
    d1 = (h - mu * tenor) / sigma_sqrt_t
    d2 = (h + mu * tenor) / sigma_sqrt_t
    
    value = norm.cdf(-d1) + math.exp(2 * mu * h / (sigma**2)) * norm.cdf(-d2)
    
    return value

if __name__ == "__main__":
    priceMax = 1000000

    spread = 100000
    value = cash_or_nothing_call(6878, 6950, 4.5, 13.80 ,0.0027, True)
    print(value)
    buy = (int(math.floor(value * 100.0) / 100.0 * priceMax) - spread)/1000000
    sell =  (int(math.ceil(value * 100.0) / 100.0 * priceMax) + spread) /1000000
    print(buy)
    print(sell)