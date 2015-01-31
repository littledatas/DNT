import socket
import sys
import time
import math
import heapq
import threading

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
        sock.close()
    return string;

def subscribe():
    print "Hi\n"
    HOST, PORT = "codebb.cloudapp.net", 17429
    s = ""
    data= "dnt" + " " + "nishilsucks" + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            s = rline.strip()
            rline = sfile.readline()
    finally:
        sock.close()

    data = s.parse(" ")
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
    print mystocks
    

def init():
    raw_data = run("SECURITIES")
    global companies
    global mystocks
    data = raw_data.split(" ")
    i = 0
    tickerupdate = ""
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
    t.start()

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

    while True:
        time.sleep(1)
        updateCompanies()         
        for company in companies:
            bids, asks = update(company) # need to write bidding 
            if company.getbidTrend() > 0: # need to write getbidTrend 
                average_bid = 0
                for B,S in bids:
                    average_bid += float(B)/len(bids)
                buy(company.getName(),10,average_bid) # numbers of shares is 10 
                company.setbought(True)
            if company.getbought():
                sell(company.getName(),10,1.25*10) # need to write get shares and getBought
                   
            company.addbids(bids) # need to write addbidTrend 
            company.addasks(asks) # add ask trends 
            

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
    return float(run("MY_CASH"))


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


    def sellStocks(self, n):
        if n < self.shares:
            while n > 0:
                heapq.heappop(self.prices)
                n-=1
            return True
        else:
            return False
        
    def buyStocks(self, num, price):
        self.shares += num
        while num > 0:
            heapq.heappush(self.prices, price)
            num-=1
