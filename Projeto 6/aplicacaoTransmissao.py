
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

#serialName = "/dev/ttyACM3"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM15"                  # Windows(variacao de)


def Interface():

    master = Tk()
    Label(master, text="Mensagem").grid(row=0)
    # e1 = Entry(master)
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    img = filedialog.askopenfilename(initialdir = "../img",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
    # e1.grid(row=0, column=1)
    Button(master, text='Enviar', command=lambda : main(img)).grid(row=4, column=0, sticky=W, pady=4)
    Button(master, text='Quit', command=master.quit).grid(row=4, column=1, sticky=W, pady=4)



    mainloop()

def divide(lista):
    i = 0
    n = 128
    lp = []
    while True:
        if len(lista) >= n:
            lp.append(lista[i:n])
            i += 128
            n += 128
        else:
            if len(lista[i:]) == 0:
                return lp
            lp.append(lista[i:])
            return lp

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

    flag1 = False
    while not flag1: #Synch 1 (Mensagem tipo 1)
        print("Enviando mensagem tipo 1")
        com.tx.tpacotes = 1
        data = (0).to_bytes(1, "big")
        time.sleep(0.3)
        com.sendData(data,1,1,0) #tipo 1

        print("Esperando mensagem tipo 2")
        #Synch 2 (Mensagem tipo 2)
        buffer_tuple, nRx = rx.getNData()
        rxbuffer, tipo , erro_npacote = buffer_tuple

        if tipo == 2: #TIPO 2
            break
        elif tipo == "":
            print("Nada recebido")
        else:
            print("Mensagem tipo 2 não recebida")
        print("-------------------------")
        time.sleep(0.3)


    print("Enviando mensagem tipo 3")

    print("Enviando mensagem tipo 4")
    with open(img, 'rb') as imagem:
        f = imagem.read()
    txBuffer = bytes(f)
    txLen    = len(txBuffer)
    print(txBuffer)

    pacotes = divide(txBuffer)
    com.tx.tpacotes = len(pacotes)

    print("Transmitindo {} bytes em {} pacotes".format(txLen, com.tx.tpacotes))
    time.sleep(0.3)

    pacote_trans = 0
    msg3 = False
    while pacote_trans < com.tx.tpacotes:
        if not msg3:
            com.tx.tpacotes = 1
            data = (0).to_bytes(1, "big")
            time.sleep(0.3)
            com.sendData(data,3,1,0)
            com.tx.tpacotes = len(pacotes)

        print("Enviando pacote {} de {}".format(pacote_trans+1, com.tx.tpacotes))
        print(pacote_trans+1)
        com.sendData(pacotes[pacote_trans],4,pacote_trans+1,0)
        time.sleep(1)

        print("Esperando mensagem tipo 5")
        buffer_tuple, nRx = rx.getNData()
        rxbuffer, tipo, erro_npacote = buffer_tuple
        if tipo == 5: #TIPO 5
            msg3 = True
            pacote_trans += 1
            continue
        elif tipo == 6: #TIPO 6
            msg3 = True
            print("Falha no recebimento")
        elif tipo == 8:
            pacote_trans = erro_npacote-1
        elif tipo == "":
            print("Nada recebido")

    print("-------------------------")
    #Synch 7 (Mensagem tipo 7)
    print("Enviando mensagem tipo 7")
    com.tx.tpacotes = 1
    data = (0).to_bytes(1, "big")
    time.sleep(0.3)
    com.sendData(data,7,1,0) #tipo 7

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    Interface()
