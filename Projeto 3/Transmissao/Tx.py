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
        self.head_size = 16
        self.eop = 11184810 #101010101010101010101010
        self.eop_size = 3


    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen = self.fisica.write(self.buffer)
                print("O tamanho transmitido. Impressao dentro do thread {}" .format(self.transLen))
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

    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen  = 0
        
        self.buffer = data

        ldata = list(data)
        
        l = self.getBufferLen()
        lb = "{0:b}".format(l)
        lb = int(lb)
        h = lb.to_bytes(self.head_size, "big")

        e = self.eop.to_bytes(self.eop_size, "big")

        #print(ldata)
        #print(list(e))
        
        self.buffer = h + data + e

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

    def contains(small, big):
        l_small = len(small)
        l_big = len(big)
        i = 0
        c = []

        while i < len(big)-1:
            if big[i] == small[0] and big[i+1] == small[1] and big[i+2] == small[2]:
                c.append([i,i+1])
            i += 1
    return c