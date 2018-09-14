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

# Construct Struct
#from construct import *

# Interface Física
from fisicaRecepcao import fisica

# enlace Tx e Rx
from Rx import RX
from Tx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.tx          = TX(self.fisica)
        self.rx          = RX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.tx.threadStart()
        self.rx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.tx.threadKill()
        self.rx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data, tipo):
        """ Send data over the enlace interface
        """
        self.tx.sendBuffer(data, tipo)

    def getData(self, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('Entrou na leitura e tentara ler ' + str(size) + ' bytes')
        data = self.rx.getNData(size)
       
        return(data, len(data))
