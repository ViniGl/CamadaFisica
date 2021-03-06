
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

print("comecou")

from enlace import *
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)



print("porta COM aberta com sucesso")



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
   
    ListTxBuffer =list()

    with open('gato.jpg', 'rb') as imagem:
    	f = imagem.read()

    txBuffer = bytes(f)
    txLen    = len(txBuffer)

    datarate = txLen*11*2/com.fisica.baudrate

    print("Tempo estimado para transmissao: {:.4f}".format(datarate))

    # Transmite dado
    print("Transmitindo {} bytes".format(txLen))
    start_time = time.time()
    com.sendData(txBuffer)

    

        
    # Atualiza dados da transmissão
    #txSize = com.tx.getStatus()
   

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    #bytesSeremLidos=com.rx.getBufferLen()
  
        
    rxBuffer, nRx = com.getData(txLen)

    # log
    print ("Lido {} bytes".format(nRx))
    print("Tempo demorado: {:.4f}".format(time.time() - start_time))
    
    #print (rxBuffer)

    f2 = open('gato2.jpg', 'wb')
    f2.write(rxBuffer)
    f2.close()

    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()