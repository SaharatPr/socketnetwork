 # Module sys has to be imported:
import sys
from socketServer import * 
from socketClient import *
from time import time, sleep
import asyncio
import os
import threading
from multiprocessing import Process, Pool
async def main():
    try:
        if(len(sys.argv) <= 1):
            print("Please enter paramitter ex. python3 routers [filename]");
            return;
        if(path.isfile(f'./table/{sys.argv[1]}.csv') != False):
            os.remove(f'./table/{sys.argv[1]}.csv')

        f = open(f"./profile/{sys.argv[1]}.txt", "r")
        line = f.readlines();
        host = line[1].split(',')[2].split(':')[0];
        port = line[1].split(',')[2].split(':')[1];
        Process(target=socketServer,args=(sys.argv[1],host, port)).start();
        count = 1;
        while True:
            await asyncio.sleep(5)
            for x in range(1,len(line)):
                socketClient(line[x],sys.argv[1],count)
            count =  count+1;
    except NameError:
        print(NameError)
if __name__ == '__main__':
    asyncio.run(main());
# line[x].split(",")[1],int(line[x].split(",")[2])