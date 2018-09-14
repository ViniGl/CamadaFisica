
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

from enlaceTransmissao import *
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
serialName = "COM5"                  # Windows(variacao de)


com = enlace(serialName)

def Interface():

    master = Tk()
    Label(master, text="Mensagem").grid(row=0)
    # e1 = Entry(master)
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    img = filedialog.askopenfilename(initialdir = "../img",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    # e1.grid(row=0, column=1)
    Button(master, text='Enviar', command=lambda : main(img)).grid(row=4, column=0, sticky=W, pady=4)
    Button(master, text='Quit', command=master.quit).grid(row=4, column=1, sticky=W, pady=4)



    mainloop()

def sendSync1():
    print("Enviando mensagem tipo 1")
    data = (0).to_bytes(1, "big")
    time.sleep(1)
    com.sendData(data,1) #tipo 1


def sendSync3():
    print("Enviando mensagem tipo 3")
    data = (0).to_bytes(1, "big")
    time.sleep(1)
    com.sendData(data,3) #tipo 3

def closeConnection():
    #Synch 7 (Mensagem tipo 7)
    print("Enviando mensagem tipo 7")
    data = (0).to_bytes(1, "big")
    time.sleep(1)
    com.sendData(data,7) #tipo 7
    print("-------------------------")

def sendMSg(img):
        #Synch 4 (Mensagem tipo 4)
        print("Enviando mensagem tipo 4")
        with open(img, 'rb') as imagem:
            f = imagem.read()
        txBuffer = bytes(f)
        txLen    = len(txBuffer)

        print("Transmitindo {} bytes".format(txLen))
        time.sleep(1)
        com.sendData(txBuffer,4)


def main(img):
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading

    rx = com.rx
    count = 0
    # Ativa comunicacao
    com.enable()
print("Enviando mensagem tipo 2")

    #verificar que a comunicação foi aberta
    print("-------------------------")
    print("Comunicação Aberta")
    print("-------------------------")

    flag1 = False
    while not flag1: #Synch 1 (Mensagem tipo 1)

        sendSync1()
        time.sleep(0.5)
        print("Esperando mensagem tipo 2")
        buffer_tuple, nRx = rx.getNData()
        rxbuffer, tipo = buffer_tuple

        if tipo == 2: #TIPO 2
            break
        elif tipo == "":
            print("Nada recebido")
        else:
            print("Mensagem tipo 2 não recebida")

        print("Reenviando mensagem tipo 1")
        print("-------------------------")
        time.sleep(1)

    flag3 = False
    msg3 = False
    while not flag3: #Synch 3 (Mensagem tipo 3)
        if not msg3:
            sendSync3()

        time.sleep(0.5)

        sendMSg(img)
        count+=1
        datarate = com.fisica.baudrate*8/11
        tempo = txLen*8/datarate
        # time.sleep(1.5+tempo*1.4)
        time.sleep(0.5)

        print("Esperando mensagem tipo 5")
        buffer_tuple, nRx = rx.getNData()
        rxbuffer, tipo = buffer_tuple

        if tipo == 5: #TIPO 5
            break
        elif tipo == 6: #TIPO 6
            msg3 = True
            print("Falha no recebimento")
        elif tipo == "":
            print("Nada recebido")
        else:
            print("Mensagem tipo 5 não recebida")
            print("Reenviando mensagem tipo 3 e 4")

        print("-------------------------")
        if count == 20:
            time.sleep(5)
            rx.clearBuffer()
            count = 0
    closeConnection()

    #Transmissao de dados (Mensagem tipo 4)
    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    '''
    print ("Gerando dados para transmissao")

    ListTxBuffer =list()

    with open(img, 'rb') as imagem:
    	f = imagem.read()

    txBuffer = bytes(f)
    txLen    = len(txBuffer)

    datarate = com.fisica.baudrate*8/11
    tempo = txLen*8/datarate


    # Transmite dado
    print("Transmitindo {} bytes".format(txLen))
    com.sendData(txBuffer)

    # Atualiza dados da transmissão
    com.tx.getStatus()

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

    rxBuffer, nRx = rx.getNData()



    # log
    print ("Lido {} bytes".format(nRx))

    if rxBuffer == "":
        print("Falha no envio!")

    else:

    '''

    # Encerra comunicação
    #time.sleep(1.5+tempo*1.4)

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    Interface()
