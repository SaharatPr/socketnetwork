 # Module sys has to be imported:
import sys
from socketServer import * 
from socketClient import *
from time import time, sleep
import threading
from multiprocessing import Process, Pool
def main():
    try:
        if(len(sys.argv) <= 1):
            print("Please enter paramitter ex. python3 routers [filename]");
            return;
        f = open(f"./profile/{sys.argv[1]}.txt", "r")
        line = f.readlines();
        Process(target=socketServer,args=(line[0].split('\n'), int(line[1].split(":")[1]))).start();
        while True:
            sleep(1 - time() % 1);
            for x in range(2,len(line)):
                socketClient(line[x],sys.argv[1], );
    except NameError:
        print(NameError)
if __name__ == '__main__':
    main();
# line[x].split(",")[1],int(line[x].split(",")[2])