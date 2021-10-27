import csv
from os import path
import pickle
import sys
import numpy as np
import pandas as pd

from sendmessage import processClinetSendmessage, readdatatable
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
            # print(f"รอบที่ {count} ");
            print("Dest sunbet,        Next hop   Cost");
            print("---------------------------")
            for dattatable in datalist:
                print(dattatable[0],"       ", dattatable[1],"       ", dattatable[2]);
    except:
        print(f"Error read table ")    
 
def getDataFromClient(data):
    try:

        datajson = pickle.loads(data);
        if(datajson["type"] == "message"):
            data = readdatatable('./table/'+sys.argv[1]+'.csv')
            processClinetSendmessage(datajson,data,sys.argv[1]);
        else:
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
            if(len(np.argwhere(subnetmyTable== i) != 0)):
                validatecost = mytable[np.argwhere(subnetmyTable== i[0])[0][0]:np.argwhere(subnetmyTable== i[0])[0][0]+1,0:3]
                constmytable = validatecost[0][2];
                # datarowchange = validatecost;
                validatecost= neartable[np.argwhere(subnetnearTable== i[0])[0][0]:np.argwhere(subnetnearTable== i[0])[0][0]+1,0:3]
                constneartable = validatecost[0][2];
                if(int(constmytable) > int(constneartable)+1):
                    mytable[np.argwhere(subnetmyTable== i[0])[0][0]] = [i[0],data["datafrom"], int(neartable[np.argwhere(subnetnearTable== i[0])[0][0]][2])+1];
                    my_df = pd.DataFrame(mytable)
                    my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 

            if(len(np.argwhere(subnetmyTable== i)) == 0 ):
                positionnear =  np.argwhere(neartable== i);
                subnet = neartable[positionnear[0][0]][positionnear[0][1]];
                fromrouter = neartable[positionnear[0][0]][1];  
                fromintable = fromrouter
                if(fromrouter == '-'):
                   fromrouter = data["datafrom"]
                else:
                   fromrouter = data["datafrom"]
                if(subnet == '-'):
                   return
                for somedata in neartable:
                    if(len(somedata) != 0):
                        if(fromintable != table):
                            datanumpi= np.append(mytable, np.array([[subnet,fromrouter,int(neartable[positionnear[0][0]][2])+1]]),axis = 0);
                            my_df = pd.DataFrame(datanumpi)
                            my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                # datanumpi= np.append(mytable, np.array([[subnet,fromrouter,int(neartable[positionnear[0][0]][2])+1]]),axis = 0);
                # my_df = pd.DataFrame(datanumpi)
                # my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                return;


                # print(subnet);
        
        

        rowdelete = [];
        for datamytable_ in mytable:
            if(datamytable_[1] == data["datafrom"]):
                c = np.argwhere(neartable== datamytable_[0]);
                if(len(c) == 0):
                    rowdelete.append(datamytable_);

        if(len(rowdelete) != 0):
            for i in rowdelete:
                c = np.argwhere(mytable== i[0]);
                for row in c:
                    if(mytable[row[0]][1] == data["datafrom"]):
                        mytable = np.delete(mytable, row[0], 0)
                        break;
            my_df = pd.DataFrame(mytable)
            my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                    # print(row[0]);
        # for datamytable_ in mytable:
        #     if(datamytable_[1] == data["datafrom"]):
        #         for dataneartable_ in neartable:
        #             if(datamytable_[0] == dataneartable_[0]):
        #                 print(datamytable_[0]);
                    
                # print(datamytable_);
    except NameError:
        print(NameError);
        print(f"Error update table")

def EditTableDisconnect(datatable, columeconnect, table, cost, count):
    #datatable คือ table ใน router
    #columeconnect คือ colume ปัจจุบัน
    #table คือชื่อ Routers หรือชื่อตาราง
    try:
        # if(len(datatable) == 0):
        #     return;

        # if(count> 1):
           
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
                        for datadelete in position_datarow:
                            mytable = np.delete(mytable,position_datarow[0][0], 0)
                            # mytable[:, 3] =  count;
                            # new_array = [tuple(row) for row in mytable]
                            # uniques = np.unique(new_array,axis=0)
                            # datanumpi =np.append(datalist, np.array(uniques),axis = 0);
                        my_df = pd.DataFrame(mytable)
                        my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
                        # print(mytable[position_datarow[0][0]]);
                        # print(datatable.split(','));
                        # print(datatable.split(',')[0]);


        # x = np.array(datatable)
        # r, c= x.shape;
        # datarouter = x[0:r,0:1];
        # subnet = columeconnect.split(",")[1];
        # position_datarow = np.argwhere(datarouter== subnet);
        # if(len(position_datarow) == 0 and subnet != "-"):
        #     datanumpi = np.append(x, np.array([[subnet,"-",cost, count]]),axis = 0);
        #     my_df = pd.DataFrame(datanumpi)
        #     my_df.to_csv(f'./table/{table}.csv', index=False,header=False) 
        

    except NameError:
        print(NameError);
        print(f"Error update table ")    