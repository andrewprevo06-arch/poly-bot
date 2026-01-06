import curses
from curses import wrapper
import time
import data
import threading
import objectcache
import httphandler

gold_p = 0
silver_p = 0
oil_p = 0
max_y = 0
max_x = 0

STATE = 's'
INSTRUMENT = None
ATTRIBUTE = None

def print_footer(stdscr, message):
    global max_y, max_x
    
    max_msg_len = max_x - 2
    if len(message) > max_msg_len:
        message = message[:max_msg_len - 3] + "..."
    
    try:
        stdscr.move(max_y - 1, 0)
        stdscr.clrtoeol()
        stdscr.addstr(max_y - 1, 0, message)
        stdscr.refresh()
    except curses.error:
        pass


def init(stdscr):
    global max_y, max_x
    max_y = stdscr.getmaxyx()[0]
    max_x = stdscr.getmaxyx()[1]
    
    print_footer(stdscr, 'Initializing contracts...')
    stdscr.refresh()
    objectcache.CachedDict()
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    print_footer(stdscr, "Ready! Press 'p' for prices, 'o' for orderbook, 'q' to quit")
    stdscr.refresh()


def display_price(stdscr):
    global gold_p, silver_p, oil_p
    
    while True:
        try:
            gold_p_n = data.getSpot('Gold')
            silver_p_n = data.getSpot('Silver')
            oil_p_n = data.getSpot('Oil')

            if gold_p_n > gold_p:
                stdscr.addstr(0, 0, f'Gold: {gold_p_n:.2f}', curses.color_pair(2))
            elif gold_p_n < gold_p:
                stdscr.addstr(0, 0, f'Gold: {gold_p_n:.2f}', curses.color_pair(1))
            
            if silver_p_n > silver_p:
                stdscr.addstr(0, 25, f'Silver: {silver_p_n:.2f}', curses.color_pair(2))
            elif silver_p_n < silver_p:
                stdscr.addstr(0, 25, f'Silver: {silver_p_n:.2f}', curses.color_pair(1))

            if oil_p_n > oil_p:
                stdscr.addstr(0, 50, f'Oil: {oil_p_n:.2f}', curses.color_pair(2))
            elif oil_p_n < oil_p:
                stdscr.addstr(0, 50, f'Oil: {oil_p_n:.2f}', curses.color_pair(1))
            
            stdscr.refresh()
            time.sleep(0.2)
            
            stdscr.addstr(0, 0, f'Gold: {gold_p_n:.2f}', curses.color_pair(0))
            stdscr.addstr(0, 25, f'Silver: {silver_p_n:.2f}', curses.color_pair(0))
            stdscr.addstr(0, 50, f'Oil: {oil_p_n:.2f}', curses.color_pair(0))
                
            gold_p = gold_p_n
            silver_p = silver_p_n
            oil_p = oil_p_n
            
            stdscr.refresh()
            time.sleep(2.0)
        except Exception as e:
            print_footer(stdscr, f'Price error: {str(e)[:30]}')


def display_orderbook(stdscr, instr, att):
    try:
        stdscr.move(2, 0)
        stdscr.clrtobot()
        
        contracts = objectcache.CachedDict().Traded[instr][att]
        
        if not contracts:
            stdscr.addstr(3, 0, f"No {instr} {att} contracts found")
            stdscr.refresh()
            return
        
        stdscr.addstr(2, 0, f"{instr} {att} Contracts:")
        
        i = 3
        for idx, c in enumerate(contracts[:9], 1):  
            display_text = f"{idx}. {c.name}"
            if len(display_text) > max_x - 2:
                display_text = display_text[:max_x - 5] + "..."
            stdscr.addstr(i, 0, display_text)
            i += 1
        
        stdscr.refresh()
    except Exception as e:
        print_footer(stdscr, f"Display error: {str(e)[:30]}")


def display_booknumber(stdscr, instr, att, n):
        contracts = objectcache.CachedDict().Traded[instr][att]
        
        if n < 1 or n > len(contracts):
            print_footer(stdscr, f"Contract #{n} out of range (1-{len(contracts)})")
            return
        
        c = contracts[n-1]
        
        stdscr.move(2, 0)
        stdscr.clrtobot()
        
        name = c.name[:max_x-2] if len(c.name) > max_x-2 else c.name
        stdscr.addstr(2, 0, name)
        stdscr.addstr(3, 0, "Loading orderbook...")
        stdscr.refresh()
        
        token_id = c.conID[0] if isinstance(c.conID, list) else c.conID
        j = httphandler.getOrderBook(token_id)
        
        stdscr.move(3, 0)
        stdscr.clrtoeol()
        
        
        stdscr.addstr(4, 2, "BID SIDE")
        stdscr.addstr(4, 30, "ASK SIDE")
        stdscr.addstr(5, 2, "Size")
        stdscr.addstr(5, 12, "Price")
        stdscr.addstr(5, 27, "Size")
        stdscr.addstr(5, 37, "Price")
        
        bids = j.get('bids', [])[:10]
        for i, bid in enumerate(bids):
            row = i + 7
            if row >= max_y - 2:
                break
            
            size = float(bid['size'])
            price = float(bid['price'])
            
            stdscr.addstr(row, 2, f"{size:>6.0f}")
            stdscr.addstr(row, 12, f"${price:.2f}")
        
        asks = j.get('asks', [])[:10]
        for i, ask in enumerate(asks):
            row = i + 7
            if row >= max_y - 2:
                break
            
            size = float(ask['size'])
            price = float(ask['price'])
            
            stdscr.addstr(row, 27, f"{size:>6.0f}")
            stdscr.addstr(row, 37, f"${price:.2f}")
        
        if bids and asks:
            spread = float(asks[0]['price']) - float(bids[0]['price'])
            stdscr.addstr(max_y - 3, 2, f"Spread: ${spread:.2f}")
        
        stdscr.refresh()
        



def event_key(stdscr):
    global STATE, INSTRUMENT, ATTRIBUTE
    
    while True:
        try:
            c = stdscr.getch()
            
            if c == ord('q'):
                STATE = 'q'
                
            elif c == ord('p'):
                STATE = 'p'
                price_thread = threading.Thread(target=display_price, args=(stdscr,), daemon=True)
                price_thread.start()
                
            elif c == ord('o'):
                STATE = 'o'
                print_footer(stdscr, '1.Gold End 2.Silver End 3.Gold Max 4.Silver Max 5.Oil Max 6.Gold Min 7.Silver Min')
                c = stdscr.getch()
                
                if c == ord('1'):
                    display_orderbook(stdscr, 'Gold', 'End')
                    INSTRUMENT = 'Gold'
                    ATTRIBUTE = 'End'
                elif c == ord('2'):
                    display_orderbook(stdscr, 'Silver', 'End')
                    INSTRUMENT = 'Silver'
                    ATTRIBUTE = 'End'
                elif c == ord('3'):
                    display_orderbook(stdscr, 'Gold', 'Max')
                    INSTRUMENT = 'Gold'
                    ATTRIBUTE = 'Max'
                elif c == ord('4'):
                    display_orderbook(stdscr, 'Silver', 'Max')
                    INSTRUMENT = 'Silver'
                    ATTRIBUTE = 'Max'
                elif c == ord('5'):
                    display_orderbook(stdscr, 'Oil', 'Max')
                    INSTRUMENT = 'Oil'
                    ATTRIBUTE = 'Max'
                elif c == ord('6'):
                    display_orderbook(stdscr, 'Gold', 'Min')
                    INSTRUMENT = 'Gold'
                    ATTRIBUTE = 'Min'
                elif c == ord('7'):
                    display_orderbook(stdscr, 'Silver', 'Min')
                    INSTRUMENT = 'Silver'
                    ATTRIBUTE = 'Min'
                elif c == ord('8'):
                    display_orderbook(stdscr, 'Oil', 'Min')
                else:
                    print_footer(stdscr, f"Invalid option: {chr(c) if 32 <= c < 127 else c}")
                    
                stdscr.refresh()
                
            elif c >= ord('1') and c <= ord('9'):
                if STATE == 'o':
                    if INSTRUMENT is None or ATTRIBUTE is None:
                        print_footer(stdscr, "Press 'o' then 1-7 to select contract type first!")
                    else:
                        display_booknumber(stdscr, INSTRUMENT, ATTRIBUTE, c - ord('1') + 1)
                        
            elif c == ord('w'):
                try:
                    wallet = httphandler.getWallet()
                    print_footer(stdscr, f"Balance: {wallet['usdc_formatted']}")
                except Exception as e:
                    print_footer(stdscr, f"Wallet error: {str(e)[:30]}")
                    
            elif 32 <= c < 127:
                print_footer(stdscr, f"Key '{chr(c)}' not used. Try: p, o, w, q")
                
        except curses.error:
            pass
        except Exception as e:
            try:
                print_footer(stdscr, f"ERR: {type(e).__name__}")
            except:
                pass

        
def main(stdscr):
    global STATE
    init(stdscr)
    stdscr.clear()
    
    key_thread = threading.Thread(target=event_key, args=(stdscr,), daemon=True)
    key_thread.start()
    
    while True:
        if STATE == 'q':
            break
        time.sleep(0.2)


if __name__ == '__main__':
    wrapper(main)