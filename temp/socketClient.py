from socket import *
from datetime import datetime
import pickle
import pandas as pd
import time
import os.path
from os import path
import numpy as np
import csv
import sys
import os
def socketClient(data, table,count):
    datatable =  readTableOrCreateFile(data,table,count);
    try:    
        jsondatatbale = {
            "datafrom" : table,
            "data": datatable,
            "count":count
        }
        if(data.split(",")[0] == table):
            return count;
        databyte = pickle.dumps(jsondatatbale)
        serverName = data.split(",")[2].split(":")[0];
        serverPort = int(data.split(",")[2].split(":")[1]);
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        clientSocket.send(databyte)
        modifiedSentence = clientSocket.recv(1024)
        if(modifiedSentence == None):
            return count;

        clientSocket.close()
        return count;
    except ConnectionRefusedError:
        EditTableDisconnect(datatable,data, table, 9999, count);
        return count;
        # print(f'Connot Connect {data.split(",")[1]}:{data.split(",")[2]}')      


def readTableOrCreateFile(data,table, count):
    try:

        if(data.split(',')[1] != "-"):
            if(path.isfile(f'./table/{table}.csv') != False):
                with open(f'./table/{table}.csv', 'r', ) as f:
                    datalist = list(csv.reader(f))
                    if(len(datalist) == 0):
                        datalist = [[data.split(',')[1], "-", 1, count]]
                        my_df = pd.DataFrame(datalist)
                        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                    WriteTable(datalist, data, table, 1,count);

            if(path.isfile(f'./table/{table}.csv') != True):
                with open(f'./table/{table}.csv', 'w+', ) as f:
                    datalist = list(csv.reader(f))
                    if(len(datalist) == 0):
                        datalist = [[data.split(',')[1], "-", 1, count]]
                        my_df = pd.DataFrame(datalist)
                        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                    WriteTable(datalist, data, table, 1, count);   
        if(path.isfile(f'./table/{table}.csv') != False):  
            f = open(f"./table/{table}.csv", "r", )
            line = list(csv.reader(f))
            npline = np.array(line);
            max = 0;
            for j in npline:
                if(max <= int(j[3])):
                    max = int(j[3]);

            newline=[];
            count = 0;
            for j in npline:
                if(max < int(j[3])):
                    line.pop(count)
                    count = count+1
            return line;
        return []
    except:
        print(f"Error read table ")    
        return [];  

def WriteTable(datatable, columeconnect, table, cost, count):
    #datatable คือ table ใน router
    #columeconnect คือ colume ปัจจุบัน
    #table คือชื่อ Routers หรือชื่อตาราง
    try:
        if(len(datatable) == 0):
            return;
        if(count> 1):

            if(path.isfile(f'./table/{table}.csv') != False):
                with open(f'./table/{table}.csv', 'r', ) as f:
                    datalist = list(csv.reader(f))
                    mytable= np.array(datalist)
                    row_mytable, c_mytable= mytable.shape;
                    routermytable = mytable[0:row_mytable,1:2];
                    if(columeconnect[0] != table):
                        position_datarow = np.argwhere(routermytable== columeconnect[0]);
                        if(len(position_datarow) == 0):
                            return;
                        mytable = np.delete(mytable,position_datarow[0][0], 0)
                        mytable[:, 3] =  count;
                        np.unique(datalist, axis=0)
                        # print(datalist);
                        # uniques = np.unique(new_array)  
                        # print(uniques);
                        datanumpi =np.append(datalist, np.array(mytable),axis = 0);
                        print(datanumpi);
                        my_df = pd.DataFrame(datanumpi)
                        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                        # print(mytable[position_datarow[0][0]]);
                        # print(datatable.split(','));
                        # print(datatable.split(',')[0]);


        x = np.array(datatable)
        r, c= x.shape;
        datarouter = x[0:r,0:1];
        subnet = columeconnect.split(",")[1];
        position_datarow = np.argwhere(datarouter== subnet);
        if(len(position_datarow) == 0 and subnet != "-"):
            datanumpi = np.append(x, np.array([[subnet,"-",cost, count]]),axis = 0);
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
        f = open(f"./profile/{sys.argv[1]}.txt", "r")
        line = f.readlines();
     
       
        with open(f'./table/{table}.csv', 'w+', ) as f:
                datalist = list(csv.reader(f))
                datalist_ = [[line[1].split(',')[1], "-", 1, 1]]
                my_df = pd.DataFrame(datalist_)
                my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
     
        if(path.isfile(f'./table/{table}.csv') != False):  
            f = open(f"./table/{table}.csv", "r", )
            line = list(csv.reader(f))
            return line;
    except:
        print(f"Error read table ")      




def EditTableDisconnect(datatable, columeconnect, table, cost, count):
    #datatable คือ table ใน router
    #columeconnect คือ colume ปัจจุบัน
    #table คือชื่อ Routers หรือชื่อตาราง
    try:
        print("");
        if(len(datatable) == 0):
            return;

        if(count> 1):
           
            if(path.isfile(f'./table/{table}.csv') != False):
                with open(f'./table/{table}.csv', 'r', ) as f:
                    datalist = list(csv.reader(f))
                    mytable= np.array(datalist)
                    row_mytable, c_mytable= mytable.shape;
                    routermytable = mytable[0:row_mytable,1:2];
                    if(columeconnect[0] != table):
                        position_datarow = np.argwhere(routermytable== columeconnect[0]);
                        if(len(position_datarow) == 0):
                            return;
                        mytable = np.delete(mytable,position_datarow[0][0], 0)
                        mytable[:, 3] =  count;
                        # print(datalist);
                        # print(mytable);
                        new_array = [tuple(row) for row in mytable]
                        uniques = np.unique(new_array,axis=0)
                        print(uniques);
                        datanumpi =np.append(datalist, np.array(uniques),axis = 0);
                        
                        my_df = pd.DataFrame(datanumpi)
                        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                        # print(mytable[position_datarow[0][0]]);
                        # print(datatable.split(','));
                        # print(datatable.split(',')[0]);


        x = np.array(datatable)
        r, c= x.shape;
        datarouter = x[0:r,0:1];
        subnet = columeconnect.split(",")[1];
        position_datarow = np.argwhere(datarouter== subnet);
        if(len(position_datarow) == 0 and subnet != "-"):
            datanumpi = np.append(x, np.array([[subnet,"-",cost, count]]),axis = 0);
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