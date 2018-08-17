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
        self.threadPause()
        # print(self.buffer)
        b           = self.buffer
        # self.buffer = self.buffer[nData:]
        self.threadResume()
        self.clearBuffer()
        return(b)

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """

        check = False
        tmp = "nan"
        while self.getBufferLen()==0:
            print("Esperando ...")

        datarate = self.fisica.baudrate*8/11
        tempo = txLen*8/datarate

        print("Tempo estimado para transmissao: {:.4f}".format(tempo))

        while not check:
            BufferRecebido = self.getBufferLen()
            print("recebido =" + str(BufferRecebido))
            if BufferRecebido == tmp:
                start_time = time.time()

                check = True
            else:
                tmp = BufferRecebido
            time.sleep(1.3)
        #
        # while(self.getBufferLen() < size):
        #     time.sleep(0.05)


        print("Arquivo capturado com sucesso!")
        print("%s segundos" % (time.time() - start_time))
        return(self.getBuffer(),tmp)


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
