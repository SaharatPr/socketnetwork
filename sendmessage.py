import csv
from os import path
import os.path
import pickle
from socket import *

def sendMessage():
    try:
        router = input('Enter source router EX. A : ')
        file_exists = os.path.exists('table/'+router+'.csv')
        if(file_exists == False): 
            print("Not find router");
            return;
        file_exists = os.path.exists('profile/'+router+'.txt')
        if(file_exists == False): 
            print("Not find router");
            return;
        ip = input('Enter destination ip Ex. 192.168.1.0/24 : ')
        data = readdatatable('./table/'+router+'.csv');
        if(len(data) == 0):
            print("404 page error");
            return;
        findsubnet = False
        for datatable in data:
            if(datatable[0] == ip):
                findsubnet = True
        
        if(findsubnet == False):
            print("404 page error");
            return;
        data = readdatatable('./profile/'+router+'.txt');
        clientSendmessag(data[1][2],router,ip )
    except NameError:
        print(NameError);
        print("Error somthing");

def readdatatable(router):
    try:
        if(path.isfile(f'{router}') != False):  
            f = open(f"{router}", "r", )
            line = list(csv.reader(f))
            return line;
        return []
    except:
        print(f"Error read table ")    
        return [];  
# //192.168.2.0/24
def clientSendmessag(ipconnect, router, destination ):
    try:
        jsondatatbale = {
            "datafrom" : router,
            "data": "hello",
            "type":"message",
            "destination":destination,
        }
        databyte = pickle.dumps(jsondatatbale)
        serverName = ipconnect.split(":")[0];
        serverPort = int(ipconnect.split(":")[1]);
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        clientSocket.send(databyte)
        modifiedSentence = clientSocket.recv(1024)
    except:
        print("AAAA");
    print(ipconnect)


def processClinetSendmessage(message,data, router):
    try:
        print(message["destination"]);
        for dataintable in data:
            if(dataintable[0] == message["destination"] and dataintable[1] == '-'):
                print("Message arrived");
                return;
            elif (dataintable[0] == message["destination"]):
                print("Send message to next router");
                ipconnect = dataintable;
        newdatatableprofile = readdatatable('./profile/'+router+'.txt');

        for x in newdatatableprofile:
            if(x[0] == ipconnect[1]):
                ipconnect = x[2]
                break;

        clientSendmessag(ipconnect, router, message["destination"]);
    except NameError:
        print(NameError);
        print(f"Error get table")
if __name__ == '__main__':
    sendMessage();