
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
<<<<<<< Updated upstream:Projeto 2/Recepcao/aplicacaoRecepcao.py
=======
from interfaceFisica import fisica
import enlaceRx
>>>>>>> Stashed changes:Projeto 2/aplicacaoRx.py
# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

<<<<<<< Updated upstream:Projeto 2/Recepcao/aplicacaoRecepcao.py
serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)
=======
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)

# fisica = fisica()
#
# enlacerx = RX()


print("porta COM aberta com sucesso")
>>>>>>> Stashed changes:Projeto 2/aplicacaoRx.py



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)
<<<<<<< Updated upstream:Projeto 2/Recepcao/aplicacaoRecepcao.py
    rx = com.rx
=======
    rx = RX()

>>>>>>> Stashed changes:Projeto 2/aplicacaoRx.py
    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("-------------------------")
    print("Comunicação Aberta")
    print("-------------------------")


    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

<<<<<<< Updated upstream:Projeto 2/Recepcao/aplicacaoRecepcao.py
    rxBuffer, nRx = rx.getNData()


=======
    check = False
    tmp = 0
    buffer = []
    while not check:
        if rx.getBufferLen():
            rxBuffer, nRx = com.getData(enlacerx.getBuffer(-1))
            recebido = rxBuffer
            if recebido == tmp:
                check = True
            else:
                buffer.append(recebido)
                tmp = recebido
>>>>>>> Stashed changes:Projeto 2/aplicacaoRx.py

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
<<<<<<< Updated upstream:Projeto 2/Recepcao/aplicacaoRecepcao.py
    #print('O tempo de transmissao foi aproximadamente {} segundos'.format(time))
=======
    # print('O tempo de transmissao foi aproximadamente {} segundos'.format(time))
>>>>>>> Stashed changes:Projeto 2/aplicacaoRx.py

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
