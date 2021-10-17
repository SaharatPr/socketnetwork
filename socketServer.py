from socket import *
from time import time, sleep
import pickle
import numpy as np
import sys
import ast
import asyncio
from processtable import *
from socketClient import *
def socketServer(router,host,port):
    try:
        # print("Server");
        serverPort = int(port)
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1000)
        print(f'Router {router} started ...');
        CreateTableFirts(router);
        while 1:
            connectionSocket, addr = serverSocket.accept()
            sentence = connectionSocket.recv(4096)
            getDataFromClient(sentence);
            connectionSocket.send(sentence)
            connectionSocket.close();
    except NameError:
        print(NameError)

