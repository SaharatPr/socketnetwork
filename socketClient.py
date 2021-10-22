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
from processtable import *
from socketServer import *

def socketClient(data, table,count):
    datatable =  readTableOrCreateFile(data,table,count);
    try:    
        jsondatatbale = {
            "datafrom" : sys.argv[1],
            "data": datatable,
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

    except ConnectionRefusedError:
        EditTableDisconnect(datatable,data, table, 9999, count);
        return count;
        # print(f'Connot Connect {data.split(",")[1]}:{data.split(",")[2]}')      