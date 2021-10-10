from socket import *
from time import time, sleep
import pickle
import numpy as np
import sys
import ast
from socketClient import *
def socketServer(router,port):
    try:
        serverPort = port
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1000)
        print(f'Router {router[0]} started ...');
        while 1:
            connectionSocket, addr = serverSocket.accept()
            sentence = connectionSocket.recv(1024)
            getDataFromClient(sentence, "S");
            # capitalizedSentence = sentence.upper()
            connectionSocket.send(sentence)
        # connectionSocket.close();
    except NameError:
        print(NameError)

def getDataFromClient(data, fromrouter):
    try:
        datajson = pickle.loads(data);
        updateTable(datajson)
    # modifiedSentence = pickle.loads(ast.literal_eval(data))
    except NameError:
        print(NameError);
        print(f"Error get table")

def updateTable(data):
    # print(data["data"]);
    table = sys.argv[1];
    datatable = readTableOrCreateFile(table);
    mytable= np.array(datatable)
    neartable = np.array(data["data"]);
    row_mytable, c_mytable= mytable.shape;
    position_datarow = np.argwhere(mytable== data["datafrom"]);
    for i in mytable:
        for j in neartable:
            if(i[0] == j[0]):
                position_datarow = np.argwhere(mytable== j[0]);
                print( mytable[position_datarow[0]]);
                mytable[position_datarow][1] = 1;
                # print(position_datarow[0][0])

 
        # print(x[0])
    # if(len(position_datarow) == 0):
        # datanumpi = np.append(mytable, np.array([[routername,1]]),axis = 0);
        # my_df = pd.DataFrame(datanumpi)
        # my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 