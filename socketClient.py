from socket import *
from datetime import datetime
import pickle

import time
import os.path
from os import path
import numpy as np
import csv
import pandas as pd
def socketClient(data, table):
    try:

        datatable =  readTableOrCreateFile(table);
        jsondatatbale = {
            "datafrom" : table,
            "data": datatable
        }
        databyte = pickle.dumps(jsondatatbale)
        # databyte = bytes(f"{len(databyte):<{HEADERSIZE}}", 'utf-8')+databyte
        serverName = data.split(",")[1];
        serverPort = int(data.split(",")[2]);
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        clientSocket.send(databyte)
        modifiedSentence = clientSocket.recv(1024)
        # print(modifiedSentence);
        # modifiedSentence = pickle.loads(modifiedSentence)
        # print(modifiedSentence);
        clientSocket.close()
    except ConnectionRefusedError:
        WriteTable(datatable,data, table, 9999);
        # print(f'Connot Connect {data.split(",")[1]}:{data.split(",")[2]}')      


def readTableOrCreateFile(table):
    try:
        if(path.isfile(f'./table/{table}.csv') != True):
            with open(f'./table/{table}.csv', 'w', ) as f:
                writer = csv.writer(f)
                writer.writerow([table,0])
        f = open(f"./table/{table}.csv", "r", )
        line = list(csv.reader(f))
        return line;
    except:
        print(f"Error read table ")      

def WriteTable(datatable, columeconnect, table, cost):
    #datatable คือ table ใน router
    #columeconnect คือ colume ปัจจุบัน
    #table คือชื่อ Routers หรือชื่อตาราง
    try:
        x = np.array(datatable)
        # print(datatable)
        r, c= x.shape;

        datarouter = x[0:r,0:1];
        routername = columeconnect.split(",")[0];
        position_datarow = np.argwhere(datarouter== routername);
        if(len(position_datarow) == 0):
            datanumpi = np.append(x, np.array([[routername,cost]]),axis = 0);
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