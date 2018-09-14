
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
serialName = "COM12"                  # Windows(variacao de)


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

def main(img):
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)
    rx = com.rx

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("-------------------------")
    print("Comunicação Aberta")
    print("-------------------------")

    flag1 = True
    flag3 = True
    

    while flag1:
        #Synch 1 (Mensagem tipo 1)
        time.sleep(0.3)
        print("Enviando mensagem tipo 1")
        data = (0).to_bytes(1, "big")
        com.sendData(data,1) #tipo 1

        print("Esperando mensagem tipo 2")
        #Synch 2 (Mensagem tipo 2)
        buffer_tuple, nRx = rx.getNData()
        rxbuffer, tipo = buffer_tuple
        time.sleep(0.3)

        if tipo == 2:
            time.sleep(2)
            break
        if tipo == 7:
            flag3 = False
            print("Encerrando comunicação")
            break
        elif tipo == "":
            print("Nada recebido")
        else:
            print("Mensagem tipo 2 não recebida")

        print("Reenviando mensagem tipo 1")
        print("-------------------------")
        time.sleep(0.3)

    msg3 = False
    while flag3:
        if not msg3:
            time.sleep(0.3)
            print("Enviando mensagem tipo 3")
            data = (0).to_bytes(1, "big")
            com.sendData(data,3)
            time.sleep(5)

        print("Enviando mensagem tipo 4")
        with open(img, 'rb') as imagem:
            f = imagem.read()
        txBuffer = bytes(f)
        txLen    = len(txBuffer)

        print("Transmitindo {} bytes".format(txLen))
        com.sendData(txBuffer,4)

        datarate = com.fisica.baudrate*8/11
        tempo = txLen*8/datarate
        time.sleep(1.5+tempo*1.4)

        print("Esperando mensagem tipo 5")
        buffer_tuple, nRx = rx.getNData()
        rxbuffer, tipo = buffer_tuple
        time.sleep(0.3)
        if tipo == 5:
            time.sleep(2)
            break
        elif tipo == 6:
            msg3 = True
            print("Falha no envio")
        elif tipo == 7:
            print("Encerrando comunicação")
            break
        elif tipo == "":
            print("Nada recebido")
        else:
            print("Mensagem tipo 5 não recebida")

        if not msg3:
            print("Reenviando mensagem tipo 3")
        print("Reenviando mensagem tipo 4")
        print("-------------------------")
        time.sleep(1)


    #Synch 7 (Mensagem tipo 7)
    print("Enviando mensagem tipo 7")
    data = (0).to_bytes(1, "big")
    com.sendData(data,7) #tipo 7
    time.sleep(3)

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    Interface()
