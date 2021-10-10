from socket import *
from datetime import datetime
import pickle
import pandas as pd
import time
import os.path
from os import path
import numpy as np
import csv
import os
def socketClient(data, table):
    datatable =  readTableOrCreateFile(data,table);
    try:    
        jsondatatbale = {
            "datafrom" : table,
            "data": datatable
        }
        if(data.split(",")[0] == table):
            return
        databyte = pickle.dumps(jsondatatbale)
        serverName = data.split(",")[2].split(":")[0];
        serverPort = int(data.split(",")[2].split(":")[1]);
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        clientSocket.send(databyte)
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
    except ConnectionRefusedError:
        WriteTable(datatable,data, table, 9999);
        # print(f'Connot Connect {data.split(",")[1]}:{data.split(",")[2]}')      


def readTableOrCreateFile(data,table):
    try:
        if(data.split(',')[1] != "-"):
            if(path.isfile(f'./table/{table}.csv') != False):
                with open(f'./table/{table}.csv', 'r', ) as f:
                    datalist = list(csv.reader(f))
                    if(len(datalist) == 0):
                        datalist = [[data.split(',')[1], "-", 1]]
                        my_df = pd.DataFrame(datalist)
                        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                    WriteTable(datalist, data, table, 1);

            if(path.isfile(f'./table/{table}.csv') != True):
                with open(f'./table/{table}.csv', 'w+', ) as f:
                    datalist = list(csv.reader(f))
                    if(len(datalist) == 0):
                        datalist = [[data.split(',')[1], "-", 1]]
                        my_df = pd.DataFrame(datalist)
                        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                    WriteTable(datalist, data, table, 1);   
        if(path.isfile(f'./table/{table}.csv') != False):  
            f = open(f"./table/{table}.csv", "r", )
            line = list(csv.reader(f))
            return line;
        return []
    except:
        print(f"Error read table ")      

def WriteTable(datatable, columeconnect, table, cost):
    #datatable คือ table ใน router
    #columeconnect คือ colume ปัจจุบัน
    #table คือชื่อ Routers หรือชื่อตาราง
    try:
        if(len(datatable) == 0):
            return
        x = np.array(datatable)
        r, c= x.shape;
        datarouter = x[0:r,0:1];
        subnet = columeconnect.split(",")[1];
        position_datarow = np.argwhere(datarouter== subnet);
        if(len(position_datarow) == 0 and subnet != "-"):
            datanumpi = np.append(x, np.array([[subnet,"-",cost]]),axis = 0);
            my_df = pd.DataFrame(datanumpi)
            my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
        
        # if(path.isfile(f'./table/{table}.csv') != True):
        #     print("XXXX");
        #     with open(f'./table/{table}.csv', 'x', ) as f:
        #         f.write(f'{columeconnect.split(",")[0]}, {cost}');
        #     return

        # with open(f'./table/{table}.csv','w', encoding='UTF8' ) as f:
        #     writer = csv.writer(f)
        #     writer.writerow(f'{columeconnect.split(",")[0]}, {cost}')

        # print();
        # print(np.searchsorted(datarouter, routername))
        # print(columeconnect.split(",")[0]);
        # for index in range(len(datatable)):
        #     if(columeconnect.split(",")[0] == datatable[index].split(",")[0]):
        #         print(f'{columeconnect.split(",")[0]} == {datatable[index].split(",")[0]}');
        #     else:
        #         # print(data[index].split(",")[0].index(columeconnect.split(",")[0]));
        #         # print(f'{data[index].split(",")[0]}');
    except NameError:
        print(NameError);
        print(f"Error update table ")    


def readTable(table):
    try:
        if(path.isfile(f'./table/{table}.csv') != False):  
            f = open(f"./table/{table}.csv", "r", )
            line = list(csv.reader(f))
            return line;
    except:
        print(f"Error read table ")      
