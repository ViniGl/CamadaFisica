
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

from enlace import *
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

serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM9"                  # Windows(variacao de)
com = enlace(serialName)
def sendSync2():
    print("Enviando mensagem tipo 2")
    data = (0).to_bytes(1, "big")
    time.sleep(1)
    com.sendData(data,2,1,0) #tipo 2

def sendSync5():
    print("Enviando mensagem tipo 5")
    data = (0).to_bytes(1, "big")
    time.sleep(1)
    com.sendData(data,5,1,0) #tipo 5

def sendSync6():
    print("Enviando mensagem tipo 6")
    data = (0).to_bytes(1, "big")
    time.sleep(1)
    com.sendData(data,6,1,0)

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading

    flag = False
    rx = com.rx
    tx = com.tx
    # Ativa comunicacao
    com.enable()

    while True:

        #verificar que a comunicação foi aberta
        print("-------------------------")
        print("Comunicação Aberta")
        print("-------------------------")
        # a seguir ha um exemplo de dados sendo carregado para transmissao
        # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
        #como fazer isso
        flag0 = False
        flag2 = False
        flag5 = False
        msg2 = False
        count = 0
        rx.clearBuffer()
        while not flag0:
            buffer_tuple, nRx = rx.getNData()
            rxbuffer, tipo, erro_npacote = buffer_tuple
            if tipo == 1:
                print("Recebido solicitação de conexão")
                flag0 = True
            elif tipo == 7:
                flag5, flag2 = True, True
                break



        while not flag2: #Synch 2 (Mensagem tipo 2)

            sendSync2()

            time.sleep(0.5)

            print("Esperando mensagem tipo 3")
            buffer_tuple, nRx = rx.getNData()
            rxbuffer, tipo, erro_npacote = buffer_tuple

            if tipo == 1:
                sendSync2()
                time.sleep(0.5)
            if tipo == 3:
                print("Conexão estabelecida")
                msg2 = True
                break
            elif tipo == 7:
                flag5= True
                break
            elif tipo == 0:
                print("Erro na recepção do arquivo")
            elif tipo == "":
                print("Nada recebido")
            else:
                print("Mensagem tipo 3 não recebida")

            print("Reenviando mensagem tipo 2")
            print("-------------------------")

        while msg2: #Synch 4 (Mensagem tipo 4)
            time.sleep(0.5)
            print("Esperando mensagem tipo 4")


            while not rx.done:
                buffer_tuple, nRx = rx.getNData()
                msg, tipo, erro_npacote = buffer_tuple


                if tipo == 3:
                        count+=1
                        sendSync6()

                elif tipo == 7:
                    flag5,msg2 = True
                    break

                else:

                    sendSync6()



        start = time.time()
        while not flag5: #Synch 5 (Mensagem tipo 5)
            sendSync5()

            time.sleep(0.5)

            print("Esperando mensagem tipo 7")
            #Synch 7 (Mensagem tipo 7)
            buffer_tuple, nRx = rx.getNData()
            rxBuffer, tipo, erro_npacote = buffer_tuple

            if tipo == 7:
                break
            else:
                print("Mensagem tipo 7 não recebida")

            print("Reenviando mensagem tipo 5")
            print("-------------------------")
            timeout = time.time() - start
            if timeout >= 20:
                break
            time.sleep(0.3)



        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")


    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
