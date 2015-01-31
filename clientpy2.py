import socket
import sys
    
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
    data = raw_data.split(" ")
    i = 0
    tickerupdate = ""
    companies = [];
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
    print companies
class Company:
    name = ""
    net = 0.0
    ratio = 0.0
    volatility = 0.0
    def __init__(self, n, ne, r, v):
        self.name = n
        self.net = ne
        self.ratio = r
        self.volatility = v
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


    
