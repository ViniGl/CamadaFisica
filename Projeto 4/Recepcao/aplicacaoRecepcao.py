
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

from enlaceTransmissao import *
from enlaceRecepcao import *
from tkinter import filedialog
from tkinter import *
#from GUI import GUI
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM3"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM5"                  # Windows(variacao de)

def checkDataType(data):
    if type == 1:
        return 1
    elif type == 2:
        return 2
    elif type == 3:
        return 3
    elif type == 4:
        return 4
    elif type == 5:
        return 5
    elif type == 6:
        return 6

def SyncMaker(type):
    noth = (0).to_bytes(2,"big")
    noth2 = (0).to_bytes(13,"big")
    payload =(0).to_bytes(1,"big")
    eop = (658188).to_bytes(3,"big")
    if type == 1:
        t = (2).to_bytes(1,"big")
        data = noth + t +noth2+ payload+ eop
        return data
    elif type == 3:
        t = (4).to_bytes(1,"big")
        data = noth + t +noth2+ payload+ eop
        return data

    elif type == 6:
        t = (6).to_bytes(1,"big")
        data = noth + t +noth2+ payload+ eop



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)
    flag = False
    rx = com.rx
    tx = com.tx
    # Ativa comunicacao
    com.enable()

    while not flag:
        #verificar que a comunicação foi aberta
        print("-------------------------")
        print("Comunicação Aberta")
        print("-------------------------")

        # a seguir ha um exemplo de dados sendo carregado para transmissao
        # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
        #como fazer isso

        # Faz a recepção dos dados
        print ("Recebendo dados .... ")

        rxBuffer, nRx = rx.getNData()


        # log
        print ("Lido {} bytes".format(nRx))

        type = checkDataType(rxBuffer)


        if type != 4:
            msg = SyncMaker(type)
            tx.sendBuffer(msg)

        elif type == "":
            msg = SyncMaker(6)
            tx.sendBuffer(msg)

        else:
            msg = SyncMaker(5)
            tx.sendBuffer(msg)
            f2 = open('ArquivoRecebido.jpg', 'wb')
            f2.write(rxBuffer)
            f2.close()
            flag = True


        # Encerra comunicação
        time.sleep(1.5+tempo*1.4)

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")


    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    Interface()
