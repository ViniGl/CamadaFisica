from tkinter import *

class GUI():

    def __init__(self,COM):
        self.com = COM

    def interface(self):
        master = Tk()
        Label(master, text="Mensagem").grid(row=0)

        e1 = Entry(master)

        e1.grid(row=0, column=1)

        def getTrue():
            print("Mensagem enviada: %s\n" % (e1.get()))
            return e1.get()

        Button(master, text='Enviar', command=self.com.sendData(e1.get())).grid(row=3, column=0, sticky=W, pady=4)
        Button(master, text='Quit', command=master.quit).grid(row=3, column=1, sticky=W, pady=4)

        mainloop( )
