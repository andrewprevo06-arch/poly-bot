import json
import httphandler

class Order:
    def __init__(self, conID, side, quantity, price):
        self.conID = conID
        self.side = side
        self.quantity = quantity
        self.price = price
    def __repr__(self):
        pass



def order2str(listOfOrders):
    listOfJson = []
    for order in listOfOrders:
        json_obj = {'token_id': order.conID,
                    'side': order.side,
                    'size': order.quantity,
                    'price': order.price
                    }
        listOfJson.append(json_obj)
    json_str = json.dumps(listOfJson, indent=1, separators=(',',':') )
    return json_str

def cancel2str(listOfCancels):
    listOfJson = []
    for string in listOfCancels:
        json_obj = {'Id': string}
        listOfJson.append(json_obj)
        
    json_str = json.dumps(listOfJson, indent=1, separators=(',',':'))
    return json_str