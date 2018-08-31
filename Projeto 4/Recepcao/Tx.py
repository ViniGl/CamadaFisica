#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time
import bitstring
import numpy as np

# Threads
import threading

# Class
class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False
        self.head_payload = 8
        self.eop = 658188 #0a0b0c
        self.eop_size = 3
        self.stuff = 0


    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen = self.fisica.write(self.buffer)
                print("O tamanho total transmitido: {:.0f} bytes" .format(self.transLen))
                time.sleep(1.5)
                try:
                    print("Through Put: {:.3f} bytes por segundo".format(self.getBufferLen()/self.fisica.tempo))
                except:
                    print("Through Put: Tempo muito baixo para calcular through put!")
                
                self.threadMutex = False

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def sendBuffer(self, data, tipo):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """

        if tipo == 1:
            tipo = (1).to_bytes(1,"big")
        elif tipo == 2:
            tipo = (2).to_bytes(1,"big")
        elif tipo == 3:
            tipo = (3).to_bytes(1,"big")
        elif tipo == 4:
            tipo = (4).to_bytes(1,"big")
        elif tipo == 5:
            tipo = (5).to_bytes(1,"big")
        elif tipo == 6:
            tipo = (6).to_bytes(1,"big")
        elif tipo == 7:
            tipo = (7).to_bytes(1,"big")
            

        self.transLen  = 0

        #data para teste Byte stuffing
        #data = 11042562902796 #0a0b0c0a0b0c
        #data = data.to_bytes(6, "big")

        data = bytearray(data)
        self.buffer = data
        #print(data)

        ini = (0).to_bytes(2,"big") #Dois primeiros bytes do head

        resto = (0).to_bytes(5,"big") #Bytes 4 a 8 do head

        e = self.eop.to_bytes(self.eop_size, "big")

        #Byte stuffing
        data = self.stuffing(data)

        l = self.getBufferLen()
        lb = "{0:b}".format(l)
        lb = int(lb)
        ps = lb.to_bytes(self.head_payload, "big")

        #data para teste Head size
        #data = 11042562902796 #0a0b0c0a0b0c
        #data = data.to_bytes(6, "big")

        data = bytes(data)
        #print(data)
        self.buffer = ini + tipo + resto + ps + data + e
        #print(self.buffer)

        self.threadMutex  = True
        print("Buffer enviado")

    

    def getBufferLen(self):
        """ Return the total size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)


    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)

    def contains(self, small, big):
        l_small = len(small)
        l_big = len(big)
        i = 0
        c = []

        while i < len(big)-2:
            if big[i] == small[0] and big[i+1] == small[1] and big[i+2] == small[2]:
                c.append([i,i+1])
            i += 1
        return c

    def stuffing(self, lista):
        ltarget = [10, 11, 12] #0a0b0c
        i=0
        while i < len(lista):
            check = lista[i]
            target = ltarget[0]
            stuff = 0

            if check == target:
                try:
                    t1 = lista[i+1]
                    t2 = lista[i+2]
                    if t1 == ltarget[1] and t2 == ltarget[2]:
                        lista.insert(i+1,stuff)
                        lista.insert(i+3,stuff)
                        lista.insert(i+5,stuff)
                except:
                    pass

            i += 1

        return lista
