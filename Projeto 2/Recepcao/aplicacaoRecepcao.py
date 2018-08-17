
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################


from enlaceRecepcao import *
import time
# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM2"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)
    rx = com.rx
    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("-------------------------")
    print("Comunicação Aberta")
    print("-------------------------")


    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

    rxBuffer, nRx = rx.getNData()



    # log
    print ("Lido {} bytes".format(nRx))

    #print (rxBuffer)

    f2 = open('ArquivoRecebido.jpg', 'wb')
    f2.write(rxBuffer)
    f2.close()

    # D = fisica.baudrate
    # n = 8
    # b = 11
    # time = D*((b+n)/n)
    #print('O tempo de transmissao foi aproximadamente {} segundos'.format(time))

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
