from socket import *
from time import time, sleep
import pickle
import numpy as np
import sys
import ast
import asyncio
from socketClient import *
def socketServer(router,host,port):
    try:
        serverPort = int(port)
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1000)
        print(f'Router {router} started ...');
        while 1:
            connectionSocket, addr = serverSocket.accept()
            sentence = connectionSocket.recv(4096)
            getDataFromClient(sentence);
            connectionSocket.send(sentence)
    except NameError:
        print(NameError)

def getDataFromClient(data):
    try:

        datajson = pickle.loads(data);
        updateTable(datajson)
    # modifiedSentence = pickle.loads(ast.literal_eval(data))
    except NameError:
        print(NameError);
        print(f"Error get table")

def updateTable(data):
    try:
        
        if(len(data["data"]) == 0):
            return;
        table = sys.argv[1];
        datatable = readTable(table);
        mytable= np.array(datatable)
        neartable = np.array(data["data"]);
        row_mytable, c_mytable= mytable.shape;
        row_neartable, c_neartable= neartable.shape;
        
        subnetmyTable = mytable[0:row_mytable,0:1];
        
        subnetnearTable = neartable[0:row_neartable,0:1];
        position_datarow = np.argwhere(mytable== data["datafrom"]);
        
        for i in subnetnearTable:
            if(len(np.argwhere(subnetmyTable== i)) == 0 ):
               positionnear =  np.argwhere(neartable== i);
               subnet = neartable[positionnear[0][0]][positionnear[0][1]];
               fromrouter = neartable[positionnear[0][0]][1];
               if(fromrouter == '-'):
                   fromrouter = data["datafrom"]
               datanumpi= np.append(mytable, np.array([[subnet,fromrouter,int(neartable[positionnear[0][0]][2])+1, int(data["count"])+1]]),axis = 0);
               my_df = pd.DataFrame(datanumpi)
               my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
            print("-----------");
        return;
        # for i in subnetmyTable:
        #     for j in subnetnearTable:
        #         print(data["datafrom"]);
        #         # print(i);
        #         # print("==============");
        #         print(j);
        #         print("-----------");
        # return;
        for i in  mytable:
            for j in  neartable:
                if(i[0] == j[0]):
                    position_datarow_mytable = np.argwhere(mytable== j[0]);
                    row_mytable = position_datarow_mytable[0]
                    position_datarow_neartable = np.argwhere(neartable== i[0]);
                    row_neartable = position_datarow_neartable[0]
                    if(mytable[row_mytable[0]][1] > neartable[row_neartable[0]][1]):
                        print("XXXX");
                        mytable[row_mytable[0]][1] = int(neartable[row_neartable[0]][1])+1;
        my_df =pd.DataFrame(mytable)
        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                # print(position_datarow[0][0])
    except NameError:
        print(NameError);
        print(f"Error update table")
 
        # print(x[0])
    # if(len(position_datarow) == 0):
        # datanumpi = np.append(mytable, np.array([[routername,1]]),axis = 0);
        # my_df = pd.DataFrame(datanumpi)
        # my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 