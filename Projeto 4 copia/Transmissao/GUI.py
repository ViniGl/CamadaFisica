from tkinter import *
from tkinter.filedialog import askopenfilename



class GUI():

    def interface(self):

        master = Tk()
        Label(master, text="Mensagem").grid(row=0)
        img = askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

        e1 = Entry(master)

        e1.grid(row=0, column=1)

        def getTrue():
            print("Mensagem enviada: %s\n" % (e1.get()))
            return e1.get()

        Button(master, text='Enviar', command="").grid(row=2, column=0)
        Button(master, text='Quit', command=master.quit).grid(row=2, column=1)

        mainloop()

i = GUI()

i.interface()
