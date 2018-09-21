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
import crcTransmissao

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
        self.head_payload = 1
        self.eop = 658188 #0a0b0c
        self.eop_size = 3
        self.stuff = 0
        self.tpacotes = 1
        self.key = '10001'


    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen = self.fisica.write(self.buffer)
                print("O tamanho total transmitido: {:.0f} bytes" .format(self.transLen))
                time.sleep(0.4)
                try:
                    print("Through Put: {:.3f} bytes por segundo".format(self.getBufferLen()/self.fisica.tempo))
                except:
                    pass
                
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

    def sendBuffer(self, data, tipo, n, erro):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen  = 0

        data = bytearray(data)
        self.buffer = data

        npacote = (n).to_bytes(1,"big") #Byte 1
        tpacotes = (self.tpacotes).to_bytes(1,"big") #Byte 2
        tipo = (tipo).to_bytes(1,"big") #Byte 3
        erro_npacote = (erro).to_bytes(1,"big") #Byte 4
        
        crc = (crcTransmissao.encodeData(self.buffer, self.key)).to_bytes(1,"big") #Byte 5
        print("crc {} {}".format(crc, type(crc)))
        resto = (0).to_bytes(3,"big") #Byte 6 a 8
        q = (0).to_bytes(1,"big") #Byte 10

        e = self.eop.to_bytes(self.eop_size, "big")

        #Byte stuffing
        data = self.stuffing(data)

        l = self.getBufferLen()
        ps = l.to_bytes(self.head_payload, "big") #Byte 9

        data = bytes(data)

        self.buffer = npacote + tpacotes + tipo + erro_npacote + crc + resto + ps + q + data + e
        

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