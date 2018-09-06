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
        data = bytearray(b)
        a = 658188
        eop = bytearray(a.to_bytes(3,'big'))
        byte_stuffing = bytearray(b'\n\x00\x0b\x00\x0c\x00')
        # byte_stuffing = bytearray(byte_stuffing.to_bytes(6, 'big'))
        tipo = b[2]
        header = b[8:16]
        try:
            eop_pos, data = self.eop_e_desstuffing(data,eop,byte_stuffing)
            if eop_pos < 17:
                print("EOP posicao invalida")
                self.clearBuffer()
                return "",0
            else:
                size = int(str(int.from_bytes(header,byteorder='big')),2)
                #print(data)
                #print(eop)
                #print(byte_stuffing)

                #print(data)
                if eop_pos == 0:
                    self.clearBuffer()
                    print("Erro: EOP não encontrado")
                    return "", 0

                payload = b[eop_pos - size: eop_pos]
        except Exception as e:
            self.clearBuffer()
            print("Erro")
            return "", 0

        if len(payload) != size:
            self.clearBuffer()
            print("Erro: Tamanho do payload não igual ao informado no Head")
            return "", 0

        eop = b[eop_pos:]

        overhead = (len(header)+len(payload)+len(eop))/len(payload)
        print("Overhead: {:.3f}".format(overhead))
        print("EOP na posição " + str(eop_pos))
        print("Mensagem recebida tipo " + str(tipo))
        print("-------------------------")
        # self.buffer = self.buffer[nData:]
        self.threadResume()
        self.clearBuffer()
        return payload, tipo


    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
        check = False
        tmp = "nan"
        print("Esperando ...")
        start_time = time.time()
        # print(self.getBufferLen())
        while self.getBufferLen()==0:
            if time.time()-start_time >= 5:
                return ("",""),""

        while not check:
            BufferRecebido = self.getBufferLen()
            print("* Recebendo: {} bytes".format(str(BufferRecebido)))
            if BufferRecebido == tmp:
                check = True
                print("Fim da recepção")
                print("-------------------------")
            else:
                tmp = BufferRecebido
            time.sleep(1.2)

        return self.getBuffer(),tmp

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""

    def eop_e_desstuffing(self, lista,eop,byte_stuffing):
        queue = bytearray()
        eop_pos = 0
        for i in range(len(lista)):
            queue.append(lista[i])
            if len(queue) >= 3:
                if queue[-3:] == eop:
                    eop_pos = i-2
            if len(queue) >= 6:
                if queue[-6:] == byte_stuffing:
                    del(queue[-5])
                    del(queue[-3])
                    del(queue[-1])
            i += 1
        return eop_pos, queue
