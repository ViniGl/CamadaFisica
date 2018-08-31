
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

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

#serialName = "/dev/ttyACM3"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM9"                  # Windows(variacao de)


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
        flag0 = True
        while flag0:
            buffer_tuple, nRx = rx.getNData()
            rxbuffer, tipo = buffer_tuple
            if tipo == 1:
                print("Recebido solicitação de conexão")
                flag0 = False
            elif tipo == "":
                pass
            else:
                print("Dados recebidos não são de solicitação de conexão")

        flag2 = True
        msg2 = False
        while flag2:
            #Synch 2 (Mensagem tipo 2)
            if not msg2:
                print("Enviando mensagem tipo 2")
                data = (0).to_bytes(1, "big")
                com.sendData(data,2) #tipo 2

                print("Esperando mensagem tipo 3")
                #Synch 3 (Mensagem tipo 3)
                buffer_tuple, nRx = rx.getNData()
                rxbuffer, tipo = buffer_tuple
                time.sleep(0.3)

            if msg2:
                print("Enviando mensagem tipo 6")
                data = (0).to_bytes(1, "big")
                com.sendData(data,6) #tipo 6

                print("Esperando mensagem tipo 4")
                #Synch 4 (Mensagem tipo 4)
                buffer_tuple, nRx = rx.getNData()
                rxbuffer, tipo = buffer_tuple
                time.sleep(0.3)

            if tipo == 3:
                print("Conexão estabelecida")
                msg2 = True
                flag2 = False
                break
            elif tipo == 4:
                flag2 = False
            elif tipo == 0:
                print("Erro na recepção do arquivo")
            elif tipo == "":
                print("Nada recebido")
            else:
                if not msg2:
                    print("Mensagem tipo 3 não recebida")
                else:
                    print("Mensagem tipo 4 não recebida")
            if not msg2:
                print("Reenviando mensagem tipo 2")
            print("-------------------------")
            time.sleep(1)


        f2 = open('ArquivoRecebido.jpg', 'wb')
        f2.write(rxBuffer)
        f2.close()


        flag5 = True
        while flag5:
            #Synch 5 (Mensagem tipo 5)
            print("Enviando mensagem tipo 5")
            data = (0).to_bytes(1, "big")
            com.sendData(data,5) #tipo 5

            print("Esperando mensagem tipo 7")
            #Synch 7 (Mensagem tipo 7)
            buffer_tuple, nRx = rx.getNData()
            rxbuffer, tipo = buffer_tuple
            time.sleep(0.3)

            if tipo == 7:
                flag5 = False
                break
            elif tipo == "":
                print("Nada recebido")
            else:
                print("Mensagem tipo 7 não recebida")

            print("Reenviando mensagem tipo 5")
            print("-------------------------")
            time.sleep(1)

        '''
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
        '''


        # Encerra comunicação
        

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")


    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
