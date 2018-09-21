
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

serialName = "/dev/ttyACM4"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM4"                  # Windows(variacao de)


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)
    rx = com.rx
    tx = com.tx
    # Ativa comunicacao
    com.enable()
    rx.clearBuffer()

    #verificar que a comunicação foi aberta
    print("-------------------------")
    print("Comunicação Aberta")
    print("-------------------------")
    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso

    flag2 = True
    flag5 = True
    flag6 = True

    while True:
        buffer_tuple, nRx = rx.getNData()

        rxbuffer, tipo = buffer_tuple
        if tipo == 1:
            print("Recebido solicitação de conexão")
            break
        if tipo == 7:
            print("Encerrando comunicação")
            flag2 = False
            flag5 = False
            flag6 = False
            break


    msg2 = False
    while flag2:
        #Synch 2 (Mensagem tipo 2)
        if not msg2:
            print("Enviando mensagem tipo 2")
            data = (0).to_bytes(1, "big")
            com.sendData(data,2) #tipo 2
            time.sleep(0.5)
            print("Esperando mensagem tipo 3")
            #Synch 3 (Mensagem tipo 3)
            buffer_tuple, nRx = rx.getNData()
            rxbuffer, tipo = buffer_tuple
            time.sleep(0.3)

        if tipo == 3:
            print("Conexão estabelecida")
            msg2 = True
            break
        elif tipo == 0:
            print("Erro na recepção do arquivo")
        if tipo == 7:
            print("Encerrando comunicação")
            flag5 = False
            flag6 = False
            break
        elif tipo == "":
            print("Nada recebido")
        else:
            print("Mensagem tipo 3 não recebida")

        print("Reenviando mensagem tipo 2")
        print("-------------------------")
        time.sleep(1)

    while flag6:
        print("Esperando mensagem tipo 4")
        #Synch 4 (Mensagem tipo 4)
        buffer_tuple, nRx = rx.getNData()
        msg, tipo = buffer_tuple
        if tipo == 4:
            f2 = open('ArquivoRecebido.jpg', 'wb')
            f2.write(msg)
            f2.close()
            break
        if tipo == 3:
            time.sleep(0.3)
        if tipo == 0:
            print("Falha no recebimento")
            print("Enviando mensagem tipo 6")
            data = (0).to_bytes(1, "big")
            com.sendData(data,6)
            time.sleep(1)
        if tipo == 7:
            print("Encerrando comunicação")
            flag5 = False
            break
        else:
            print("Nada recebido")
        time.sleep(1)



    start = time.time()
    while flag5:
        #Synch 5 (Mensagem tipo 5)
        print("Enviando mensagem tipo 5")
        data = (0).to_bytes(1, "big")
        com.sendData(data,5) #tipo 5
        time.sleep(0.3)
        print("Esperando mensagem tipo 7")
        #Synch 7 (Mensagem tipo 7)
        buffer_tuple, nRx = rx.getNData()
        rxBuffer, tipo = buffer_tuple

        time.sleep(0.3)

        if tipo == 7:
            break
        elif tipo == "":
            print("Nada recebido")
        else:
            print("Mensagem tipo 7 não recebida")

        print("Reenviando mensagem tipo 5")
        print("-------------------------")
        time.sleep(1)
        final = time.time() - start
        if final >= 20:
            break

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")


    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
