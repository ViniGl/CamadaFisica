#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################
#Carareto
#17/02/2018
####################################################

# Importa pacote de comunicação serial
import serial

# importa pacote para conversão binário ascii
import binascii

import time

#################################
# Interface com a camada física #
#################################
class fisica(object):
    """ This class implements methods to handler the uart communication
    """
    def __init__(self, name):
        self.name        = name
        self.port        = None
        self.baudrate    = 115200
        #self.baudrate    = 9600
        self.bytesize    = serial.EIGHTBITS
        self.parity      = serial.PARITY_NONE
        self.stop        = serial.STOPBITS_ONE
        self.timeout     = 0.1
        self.tempo = 0

    def open(self):
        """ Opens serial port and configure it
        """
        self.port = serial.Serial(self.name,
                                  self.baudrate,
                                  self.bytesize,
                                  self.parity,
                                  self.stop,
                                  self.timeout)

    def close(self):
        """ Close serial port
        """
        self.port.close()

    def flush(self):
        """ Clear serial data
        """
        self.port.flushInput()
        self.port.flushOutput()

    def encode(self, data):
        """ Encode TX as ASCII data for transmission
        """
        encoded = binascii.hexlify(data)
        return(encoded)

    def write(self, txBuffer):
        """ Write data to serial port

        This command takes a buffer and format
        it before transmit. This is necessary
        because the pyserial and arduino uses
        Software flow control between both
        sides of communication.
        """
        datarate = self.baudrate*8/11
        tempo = (len(txBuffer))*8/datarate
        print("Tempo estimado para transmissão: {:.2f} milisegundos".format(tempo*1000))
        start_time = time.time()
        nTx = self.port.write(self.encode(txBuffer))
        self.port.flush()
        self.tempo = (time.time()-start_time)*1000
        print("Tempo total de transmissão: {:.2f} milisegundos".format(self.tempo))
        return(nTx/2)