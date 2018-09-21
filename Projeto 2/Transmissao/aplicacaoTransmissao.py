
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

<<<<<<< Updated upstream
<<<<<<< Updated upstream
#serialName = "/dev/ttyACM3"           # Ubuntu (variacao de)
=======
serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
>>>>>>> Stashed changes
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM8"                  # Windows(variacao de)

<<<<<<< Updated upstream
def Interface():

    master = Tk()
    Label(master, text="Mensagem").grid(row=0)
    # e1 = Entry(master)
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    img = filedialog.askopenfilename(initialdir = "../img",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    # e1.grid(row=0, column=1)
    print(type(img))
    Button(master, text='Enviar', command=lambda : main(img)).grid(row=4, column=0, sticky=W, pady=4)
    # Button(master, text='Quit', command=master.quit).grid(row=3, column=1, sticky=W, pady=4)


=======
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)
>>>>>>> Stashed changes

    mainloop()

def main(img):
=======
def main():
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
    ListTxBuffer =list()
=======
    # ListTxBuffer =list()
>>>>>>> Stashed changes


    with open("../img/gatinho.jpg", 'rb') as imagem:
    	f = imagem.read()

    txBuffer = bytes(f)
    txLen    = len(txBuffer)
<<<<<<< Updated upstream
=======
    # print(txLen)
    print("Total de bytes: {}".format(txLen))
>>>>>>> Stashed changes

    datarate = com.fisica.baudrate*8/11
    tempo = txLen*8/datarate


    # Transmite dado
    print("Transmitindo {} bytes".format(txLen))
    com.sendData(txBuffer)

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
    # Atualiza dados da transmissão
    com.tx.getStatus()


    # Encerra comunicação
    time.sleep(1.5+tempo*1.4)
    
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
