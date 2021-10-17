import csv
from os import path
import pickle
import sys
import numpy as np
import pandas as pd
# เราเตอร์เริ่มทำงาน สร้างtable
def CreateTableFirts(table):
    try:
        if(path.isfile(f'./table/{table}.csv') != True):
            with open(f"./profile/{sys.argv[1]}.txt", "r") as f:
                line = f.readlines();
                x = []
                for index in  range(1,len(line)):
                    temp =line[index].split(',')
                    if(temp[1] != '-'):
                                  #Sub ip, next routers, cost,count  
                        x.append([temp[1],'-',temp[3].strip()]);
                my_df = pd.DataFrame(x)
                my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
    except NameError:
        print(f"Error CreateTableFirts table ")   

def readTableOrCreateFile(data,table, count):
    try:
        if(path.isfile(f'./table/{table}.csv') != True):
            CreateTableFirts(table);
        
        if(path.isfile(f'./table/{table}.csv') != False):  
            f = open(f"./table/{table}.csv", "r", )
            line = list(csv.reader(f))
            return line;
        return []
    except:
        print(f"Error read table ")    
        return [];  

def readTableOnly(table, count):
    try:
        with open(f'./table/{table}.csv', 'r', ) as f:
            datalist = list(csv.reader(f))
            print(f"รอบที่ {count} ");
            print("Dest sunbet,        Next hop   Cost");
            print("---------------------------")
            for dattatable in datalist:
                print(dattatable[0],"       ", dattatable[1],"       ", dattatable[2]);
    except:
        print(f"Error read table ")    
 
def getDataFromClient(data):
    try:

        datajson = pickle.loads(data);
        updateTable(datajson)
    except NameError:
        print(NameError);
        print(f"Error get table")

def updateTable(data):
    try:
        if(len(data["data"]) == 0):
            return;
        table = sys.argv[1];
        datatable = readTableOrCreateFile(data,table, 1);
        mytable= np.array(datatable)
        neartable = np.array(data["data"]);
        row_mytable, c_mytable= mytable.shape;
        row_neartable, c_neartable= neartable.shape;
        subnetmyTable = mytable[0:row_mytable,0:1];
        subnetnearTable = neartable[0:row_neartable,0:1];
        position_datarow = np.argwhere(mytable== data["datafrom"]);
        newarrat =  np.concatenate((mytable, neartable), axis=0)
        for i in subnetnearTable:
            if(len(np.argwhere(subnetmyTable== i)) == 0 ):
                positionnear =  np.argwhere(neartable== i);
                subnet = neartable[positionnear[0][0]][positionnear[0][1]];
                fromrouter = neartable[positionnear[0][0]][1];  
                if(fromrouter == '-'):
                   fromrouter = data["datafrom"]
                if(subnet == '-'):
                   return
               
                datanumpi= np.append(mytable, np.array([[subnet,fromrouter,int(neartable[positionnear[0][0]][2])+1]]),axis = 0);
                my_df = pd.DataFrame(datanumpi)
                my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                return;
    except NameError:
        print(NameError);
        print(f"Error update table")
