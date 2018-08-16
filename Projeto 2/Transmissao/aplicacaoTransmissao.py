
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

from enlaceTransmissao import *
#from GUI import GUI
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM6"                  # Windows(variacao de)

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("-------------------------")
    print("Comunicação Aberta")
    print("-------------------------")


    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    print ("Gerando dados para transmissao")
  
    ListTxBuffer =list()

    #arquivo = GUI.e1

    """
    with open('../img/gatinho.jpg', 'rb') as imagem:
    	f = imagem.read()

    txBuffer = bytes(f)
    txLen = len(txBuffer)

    print("Total de bytes: {}".format(txLen))

    datarate = com.fisica.baudrate*8/11
    tempo = txLen*8/datarate
    print("Tempo estimado para transmissao: {:.4f}".format(tempo))

    # Atualiza dados da transmissão
    #com.tx.getStatus()

    # Transmite dado
    start_time = time.time()
    com.sendData(txBuffer)
    """
    with open('../img/a.png', 'rb') as imagem:
        f = imagem.read()

    txBuffer = bytes(f)
    txLen    = len(txBuffer)

    datarate = com.fisica.baudrate*8/11
    tempo = txLen*8/datarate

    print("Tempo estimado para transmissao: {:.4f}".format(tempo))

    # Transmite dado
    print("Transmitindo {} bytes".format(txLen))
    start_time = time.time()
    com.sendData(txBuffer)

    # Atualiza dados da transmissão
    com.tx.getStatus()
    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    input("\nPressione enter para sair")
    exit()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()