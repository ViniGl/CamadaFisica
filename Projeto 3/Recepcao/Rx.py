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

# Threads
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self):
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado.
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self):
        """ Remove n data from buffer
        """



        def contains( small, big):
            l_small = len(small)
            l_big = len(big)
            i = 0
            c = []

            while i < len(big)-2:
                if big[i] == small[0] and big[i+1] == small[1] and big[i+2] == small[2]:
                    c.append([i,i+1,i+2])
                i += 1

            return c

        self.threadPause()
        # print(self.buffer)
        b           = self.buffer
        data = list(b)
        a = 11184810
        eop = list(a.to_bytes(3,'big'))

        c = contains(eop,data)
        if c != []:
            header = b[0:16]
            size = int(str(int.from_bytes(header,byteorder='big')),2)
            payload = b[c[0][0]-size: size + 16]
            eop = b[c[0][0]:]
            overhead = (len(header)+len(payload)+len(eop))/len(payload)

            print("Overhead = {:.2f}".format(overhead))
            print("EOP na posicao" +" "+ str(c[0][0]))
            # self.buffer = self.buffer[nData:]
            self.threadResume()
            self.clearBuffer()
            return(payload)
        else:
            self.clearBuffer()
            print("EOP nao encontrado")
            return ""

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """

        check = False
        tmp = "nan"
        while self.getBufferLen()==0:
            print("Esperando ...")


        while not check:
            BufferRecebido = self.getBufferLen()
            print("recebido =" + str(BufferRecebido))
            if BufferRecebido == tmp:
                check = True
            else:
                tmp = BufferRecebido
            time.sleep(1.3)
        #
        # while(self.getBufferLen() < size):
        #     time.sleep(0.05)


        print("Arquivo capturado com sucesso!")
        return(self.getBuffer(),tmp)


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
