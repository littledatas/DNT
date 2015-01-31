import socket
import sys
import time
import math
import heapq

companies = []
mystocks = []

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
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data= "dnt" + " " + "nishilsucks" + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

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
            mystocks.append(Stocks(name))
            net = float(data[i+1])
            ratio = float(data[i+2])
            volatility = float(data[i+3])
            companies.append(Company(name, net, ratio, volatility))
        i+=4
   
def updateCompanies():
    global companies
    raw_data = run("SECURITIES")
    data = raw_data.split(" ")
    i = 0
    while i < len(data):
        if i == 0:
            i-=3
        else:
            companies[math.floor(i/4)].updateNet(float(data[i+1]))
            companies[math.floor(i/4)].updateRatio(float(data[i+2]))
            companies[math.floor(i/4)].updateVolatility(float(data[i+3]))
        i+=4
    global mycompanies
    raw_data = run("MY_SECURITIES")
    data

def algo_1(): # ticker, shares, price 
    
    while True:
        time.sleep(1)
        for company in companies:
            bids, asks, shares,net = update(company) # need to write bidding 
            if company.getTrend() > 0: # need to write getTrend 
                average_bid = reduce(lambda x, y: x + y, bids) / len(bids)
                buy(company.getName(),average_bid,shares) 
            if company.bought > 0:
                sell(company.getName,1.25*company.getBought,shares) # need to write get shares and getBought
        
           
            
            company.addbidTrend(bids) # need to write addbidTrend 
            company.addaskTrend(asks) # add ask trends 
            company.addnetTrend(net) # add net Trend



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
    def __init__(self, n, ne, r, v):
        self.name = n
        self.net =  [ne]
        self.ratio = [r]
        self.volatility = [v]
        self.trend = [0]
        self.shares = [0]
        self.bought = [0]
    def getName(self):
        return self.name
    def getNet(self):
        return self.net
    def getRatio(self):
        return self.ratio
    def getVolatility(self):
        return self.volatility
    def __repr__(self):
        return "Ticker: "+self.name+" Net Value: "+str(self.net)+" Ratio: "+str(self.ratio)+" Volatility: "+str(self.volatility)
    def updateNet(self, ne):
        self.net.append(ne)
    def updateRatio(self, r):
        self.ratio.append(r)
    def updateVolatility(self, v):
        self.volatility.append(v)

class Stocks:
    name = ""
    number = 0
    heap = []
    def __init__(self, n):
        self.name = n
    def sellStocks(self, n):
        if n < number:
            while n > 0:
                heapq.heappop(heap)
                n-=1
        else:
            return False
    def sellStock(self):
        number -= 1
    def buyStocks(self, num, price):
        number += num
        while num > 0:
            heapq.heappush(price)
            num-=1
    
        
