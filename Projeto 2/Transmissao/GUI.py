from tkinter import *

class Interface():

    def __init__(self,COM):
        self.com = COM
        self.flag = False

    def setFlag(self):
        self.flag = True

    def interface(self):
        master = Tk()
        Label(master, text="Mensagem").grid(row=0)
        # e1 = Entry(master)

        # e1.grid(row=0, column=1)

        Button(master, text='Enviar', command=self.setFlag()).grid(row=4, column=0, sticky=W, pady=4)
        Button(master, text='Quit', command=master.quit).grid(row=3, column=1, sticky=W, pady=4)

        if self.flag:
            return(True)

        mainloop()
