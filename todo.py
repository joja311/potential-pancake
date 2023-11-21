import csv
from tkinter import *

root = Tk()
label1 = Label(root, text='Tasks:')

listbox = Listbox(root, borderwidth=2, relief="groove")

label1.pack()
listbox.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


with open('tasks.csv', 'r') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        listbox.insert(index, row[0])
root.mainloop()
