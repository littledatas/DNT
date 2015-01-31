import socket
import sys
import time
import math
import heapq
import threading
import random 
companies = []

def run(*commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data= "dnt" + " " + "nishilsucks" + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    string = ""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            string += rline.strip()
            rline = sfile.readline()
    finally:
        #sock.sendall()
        sock.close()
        
    return string;

def subscribe():
    print "Hi\n"
    HOST, PORT = "codebb.cloudapp.net", 17429
    s = ""
    data= "dnt" + " " + "nishilsucks" + "\nSUBSCRIBE\n" + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            s = rline.strip()
            rline = sfile.readline()
            data = s.split(" ")
            action = data[0]
            ticker = data[1]
            price = data[2]
            shares = data[3]
            for stock in companies:
                if stock.getName == ticker:
                    if action == "BUY":
                        stock.buyStocks(shares, price)
                    else:
                        stock.sellStocks(shares)
    finally:
        #sock.sendall()
        sock.close()



def init():
    raw_data = run("SECURITIES")
    global companies
    global mystocks
    data = raw_data.split(" ")
    i = 0
    tickerupdate = ""
    print 'Data', data
    while i < len(data):
        if i == 0:
            i-=3
        else:
            name = data[i]
            net = float(data[i+1])
            ratio = float(data[i+2])
            volatility = float(data[i+3])
            companies.append(Company(name, net, ratio, volatility))
        i+=4
    t = threading.Thread(target=subscribe)
    try:
        t.start()
    except (KeyboardInterrupt, SystemExit):
        print "Check this motha"
        run("CLOSE_CONNECTION")
        cleanup_stop_thread();
       # run("CLOSE_CONNECTION")
        sys.exit()
    
def updateCompanies():
    global companies
    raw_data = run("SECURITIES")
    data = raw_data.split(" ")
    i = 0
    while i < len(data):
        if i == 0:
            i-=3
        else:
            companies[int(math.floor(i/4))].updateNet(float(data[i+1]))
            companies[int(math.floor(i/4))].updateRatio(float(data[i+2]))
            companies[int(math.floor(i/4))].updateVolatility(float(data[i+3]))
        i+=4
    global mycompanies
    raw_data = run("MY_SECURITIES")
    data

def algo_1(): # ticker, shares, price 
    init()
    timep = 0
    while True:
        timep += .01
        updateCompanies()        
        for company in companies:
            bids, asks = update(company) # need to write bidding 
                
            shares = 20*heatfunction(timep)
            if type(doshares(company)) is not None:
                shares = math.max(int(doshares(company),heatfunction(timep)))*40
            average_bid = 0
            for B,S in bids:
                average_bid += float(B)/len(bids)
            buy(company.getName(),shares,average_bid) # numbers of shares is 10 
            company.setbought(True)
            if company.getshares() > 0 or random.random() > 0:
                print 'testing'
                average_bid = 0
                for B,S in bids:
                    average_bid += float(B)/len(bids)

                sell(company.getName(),int(company.getshares()*.8),average_bid*.15)
                   
            company.addbids(bids) # need to write addbidTrend 
            company.addasks(asks) # add ask trends 

def heatfunction(x):
    x *=-1
    return math.e**x


def doshares(company):
    bids = company.getbids()
    if len(bids) > 4:
        bids1 = bids[:int(len(bids)/4)]
        bids2 = bids[int(len(bids)/4)+1:int(len(bids)/2)]
        bids3 = bids[int(len(bids)/2)+1:int(3*len(bids)/4)]
        bids4 = bids[int(3*len(bids)/4)+1:int(len(bids))-1]
        avgbid1 = avgbid(bids1)
        abgbid2 = avgbid(bids2)
        avgbid3 = avgbid(bids3)
        avgbid4 = avgbid(bids4)
        avg5 = 0
        if len(bids4) > 4:
            last = bids[len(bids)-1]
            l = bids[len(bids)-2]
            Bla = []
            Bl = []
                       
            if isinstance(last,list) and isinstance(l,list):
                for B,S in last:
                    Bla.append(float(B))
                for B,S in l:
                    Bl.append(float(B))
                avg5 = max(Bla) - max(Bl)
        if avgbid4 == 0:
            avgbid4 = avg5*.657
        diff = (avg5-avgbid4)/(abs(avgbid4)+1)
        return .7+diff
    return .5


def avgbid(bids):
    ret = 0
    if isinstance(bids,list):
        for bid in bids:
            if isinstance(bid,int):
                return 43 
            Bi = []
            for B,S in bid:
                Bi.append(B)
            if isinstance(Bi,list):
                ret +=float(max(Bi))/len(bids)
            else:
                ret = int(random.random()*50)

    return ret


def update(company):
    name = company.getName()
    raw_data = run("ORDERS " + name)
    raw_data = raw_data.split(" ")
    raw_data.remove('SECURITY_ORDERS_OUT')
    bids = []
    asks = []
    for x in range(0,len(raw_data)):
        if x % 4 == 0:
            types = raw_data[x]            
            price = raw_data[x+2]
            shares = raw_data[x+3]
            if types == "BID":
                bids.append((price,shares))
            else:
                asks.append((price,shares))
    return bids,asks

def buy(ticker, shares, price):
    print run("BID "+ticker+" "+str(price)+" "+str(shares))
    

def sell(ticker, shares, price):
    print run("ASK "+ticker+" "+str(price)+" "+str(shares))

def cancelbuy(ticker):
    print run("CLEAR_BID "+ticker)

def cancelsell(ticket):
    print run("CLEAR_ASK "+ticker)

def getCash():
    data = run("MY_CASH").parse("  ")
    print(data[1])
    return float(data[1])


class Company:
    name = ""
    net = [] # net value 
    ratio = [] # 
    volatility = [] #
    bids = []
    shares = 0
    asks = []
    bought = False
    prices = []
    
    def __init__(self, n, ne, r, v):
        self.name = n
        self.net =  [ne]
        self.ratio = [r]
        self.volatility = [v]
        self.bids = [0]
        self.asks = [0]
        self.shares = 0
        self.prices = []
        self.bought = False
    def getName(self):
        return self.name
    def getNet(self):
        return self.net
    def getRatio(self):
        return self.ratio
    def getVolatility(self):
        return self.volatility
    def __repr__(self):
        return "Ticker: "+self.name+" Shares: "+number+" Net Value: "+str(self.net)+" Ratio: "+str(self.ratio)+" Volatility: "+str(self.volatility)
    def updateNet(self, ne):
        self.net.append(ne)
    def updateRatio(self, r):
        self.ratio.append(r)
    def updateVolatility(self, v):
        self.volatility.append(v)
    def getbidTrend(self):
        last = self.bids[len(self.bids)-1]
        l = self.bids[len(self.bids)-2]
        Bla = []
        Bl = []
       
        if isinstance(last,list) and isinstance(l,list):
            for B,S in last:
                Bla.append(float(B))
            for B,S in l:
                Bl.append(float(B))
            return max(Bla) - max(Bl)
        print self.bids
        
    def setbought(self,v):
        self.bought = v
    def getbought(self):
        return self.bought
    def addbids(self,b):
        self.bids.append(b)
    def addasks(self,a):
        self.asks.append(a)
    def getbids(self):
        return self.bids
    def getshares(self):
        return self.shares
    def sellStocks(self, n, price):
        if n < self.shares:
            #sell(self.getName(),n,price)
            while n > 0:
                heapq.heappop(self.prices)
                n-=1
            return True

        else:
            return False
        
    def buyStocks(self, num, price):
        #buy(self.getName(),num,price)
        self.shares += num
        while num > 0:
            heapq.heappush(self.prices, price)
            num-=1
