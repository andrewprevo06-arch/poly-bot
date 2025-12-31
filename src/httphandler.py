from py_clob_client.clob_types import OrderArgs, OrderType, PostOrdersArgs
import creds
from creds import POLYMARKET_ADDRESS
from py_clob_client.order_builder.constants import BUY
import requests
from web3 import Web3
import time

contractsURL = "https://gamma-api.polymarket.com/series?limit=1000&slug=silver-si-above&slug=will-silver-si-hit&slug=what-will-gold-gc-hit&slug=gold-gc-above&slug=crude-oil-cl-above&slug=crude-oil-cl-hit"
eventURL = "https://gamma-api.polymarket.com/events/"
marketURL = "https://gamma-api.polymarket.com/markets/"
orderBookURL = "https://clob.polymarket.com/book?token_id="


# GET FUNCTIONS

def getOrders():
   client = creds.get_client()
   response = client.get_orders()
   return response

def getWallet():
    web3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))
    # USDC contract (native USDC on Polygon)
    USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    
    usdc_abi = [{
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }]
    
    usdc = web3.eth.contract(
        address=Web3.to_checksum_address(USDC_ADDRESS),
        abi=usdc_abi
    )
    usdc_balance = usdc.functions.balanceOf(
        Web3.to_checksum_address(POLYMARKET_ADDRESS)
    ).call()
    usdc_amount = usdc_balance / 1_000_000  # USDC has 6 decimals
    return {
        'address': POLYMARKET_ADDRESS,
        'Available Balance': float(usdc_amount),
        'usdc_formatted': f'${usdc_amount:.2f}',
    }


def getContracts(url):
   response = requests.get(url)
   j = response.json()
   return j
    
def getSeries():
   response = requests.get(contractsURL)
   j = response.json()
   return j 

def getEvent(eID):
   response = requests.get(eventURL + eID)
   j = response.json()
   return j 

def getMarket(mID):
   response = requests.get(marketURL + mID)
   j = response.json()
   return j 

def getOrderBook(tID):
   response = requests.get(orderBookURL + tID)
   j = response.json()
   return j 


# POST FUNCTIONS


def postAddOrders(orderList):
    if not orderList:
        return []
    
    client = creds.get_client()
    all_responses = []

    BATCH_SIZE = 15
    num_batches = (len(orderList) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(num_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(orderList))
        chunk = orderList[start_idx:end_idx]
        
        postOrderArgs = []
        for order in chunk:
            orderArgs = OrderArgs(
                price=order.price,
                size=order.quantity,
                side=BUY,
                token_id=order.conID
            )
            signedOrder = client.create_order(orderArgs)
            postOrderArgs.append(
                PostOrdersArgs(order=signedOrder, orderType=OrderType.GTC)
            )
        

        response = client.post_orders(postOrderArgs)  
        all_responses.append(response)
        
        if batch_num < num_batches - 1:
            time.sleep(0.5)

    return all_responses

def postCancelOrders(cancelList):
   client = creds.get_client()
   
   for oID in cancelList:
      response = client.cancel(order_id=oID)
   
   return response

