import sys
import algo
import wallet
import httphandler
import order
from threading import Thread
import objectcache
import time

algo_threads = []

def startDaAlgo():
    global algo_threads
    oil_end = algo.Algo(
            objectcache.CachedDict().Traded['Oil']['End'],
             5,
            .10,
            300,
            "OilEnd")
    oil_max = algo.Algo(
            objectcache.CachedDict().Traded['Oil']['Max'],
             5,
            .10,
            300,
            "OilMax")
    oil_min = algo.Algo(
            objectcache.CachedDict().Traded['Oil']['Min'],
             5,
            .10,
            300,
            "OilMin")
    thread_oil = Thread(target = oil_end.algo, args= [] )
    thread_oil.daemon = True
    thread_oil.start()
    time.sleep(20)
    thread_oil2 = Thread(target= oil_max.algo, args = [] )
    thread_oil2.daemon = True
    thread_oil2.start()
    time.sleep(20)
    thread_oil3 = Thread(target=oil_min.algo, args = [] )
    thread_oil3.daemon = True
    thread_oil3.start()


if __name__ == "__main__":
    startDaAlgo()

    while(1):
        time.sleep(1)