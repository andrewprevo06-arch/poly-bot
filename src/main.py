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
    gold_end = algo.Algo(
            objectcache.CachedDict().Traded['Gold']['End'],
             5,
            .10,
            300,
            "GoldEnd")
    gold_max = algo.Algo(
            objectcache.CachedDict().Traded['Gold']['Max'],
             5,
            .10,
            300,
            "GoldMax")
    gold_min = algo.Algo(
            objectcache.CachedDict().Traded['Gold']['Min'],
             5,
            .10,
            300,
            "GoldMin")
    silver_end = algo.Algo(
            objectcache.CachedDict().Traded['Silver']['End'],
             5,
            .10,
            300,
            "SilverEnd")
    silver_max = algo.Algo(
            objectcache.CachedDict().Traded['Silver']['Max'],
             5,
            .10,
            300,
            "SilverMax")
    silver_min = algo.Algo(
            objectcache.CachedDict().Traded['Silver']['Min'],
             5,
            .10,
            300,
            "SilverMin")
    thread_gold_end = Thread(target = gold_end.algo, args=[])
    thread_gold_max = Thread(target = gold_max.algo, args = [])
    thread_gold_min = Thread(target= gold_min.algo, args = [])
    thread_silver_end = Thread(target = silver_end.algo, args=[])
    thread_silver_max = Thread(target = silver_max.algo, args=[])
    thread_silver_min = Thread(target = silver_min.algo, args=[])
    thread_gold_end.daemon = True
    thread_gold_max.daemon = True
    thread_gold_min.daemon = True
    thread_silver_end.daemon = True
    thread_silver_max.daemon = True
    thread_silver_min.daemon = True
    thread_gold_end.start()
    time.sleep(10)
    thread_silver_end.start()
    time.sleep(10)
    thread_gold_max.start()
    time.sleep(10)
    thread_silver_max.start()
    time.sleep(10)
    thread_gold_min.start()
    time.sleep(10)
    thread_silver_min.start()

if __name__ == "__main__":
    startDaAlgo()
    while(1):
        time.sleep(1)