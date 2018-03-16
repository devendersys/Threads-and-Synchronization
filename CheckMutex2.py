# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 13:55:57 2018
"""
from MutexAcrossProcess import mutexAcrossProcess
import time

if __name__ == '__main__':
     evMutex = mutexAcrossProcess(b"ChangeMutexName")
     print("Start while loop")
     x = 0
     while x < 10:
         evMutex.acquire()
         fo = open("foo.txt", "ab")
         fo.write(b"2- ")
         print("Test Mutex 2")
         fo.close()  
         evMutex.release()
         time.sleep(1)    
         x =x+1
     print("End of while loop")
