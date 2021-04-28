from tkinter import *

def save_continue(master, listbox, var):
    sel = listbox.curselection()
    for e in list(sel):
        var.append(listbox.get(e))
        
def listSelect(selVar, selList, title):
    window = Tk()
    window.title(title)

    listbox = Listbox(window, selectmode = 'multiple')
    for item in selList:
        listbox.insert(END, item)
    listbox.pack()

    b1 = Button(window, text='Save', width=15, height=2, command=lambda: save_continue(window,listbox,selVar))
    b1.pack()

    mainloop()