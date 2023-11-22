import csv
from tkinter import *
from datetime import datetime
from time import localtime

def open_add():
    top = Toplevel(root)
    def timer():
        current_time = localtime()
        return f"{current_time[0]}/{current_time[1]}/{current_time[2]}"


    def add(name, description, due_date):
        with open('tasks.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, description, due_date.strftime('%Y-%m-%d'),timer()])
        top.destroy()  
        listbox.insert(END, name)

    tname = Entry(top)
    tdes = Entry(top)
    t_due_date = Entry(top)
    label = Label(top, text="Enter name:")
    label2 = Label(top, text='Description:')
    label3 = Label(top, text='Due Date (YYYY-MM-DD):')
    btn = Button(top, text='Add', command=lambda: add(tname.get(), tdes.get(), datetime.strptime(t_due_date.get(), '%Y-%m-%d')))
    
    label.pack(pady=5)
    tname.pack(pady=5)
    label2.pack(pady=5)
    tdes.pack(pady=5)
    label3.pack(pady=5)
    t_due_date.pack(pady=5)
    btn.pack(pady=10)

def complete():
    top = Toplevel(root)

    def comp(name):
        with open('tasks.csv', 'r') as file:
            tasks = list(csv.reader(file))

        with open('completed.csv', 'a', newline='') as cfile:
            writer = csv.writer(cfile)

            for row in tasks:
                if row[0].strip() == name.strip():
                    writer.writerow(row)

        with open('tasks.csv', 'w', newline='') as write:
            writer = csv.writer(write)
            writer.writerows([row for row in tasks if row[0].strip() != name.strip()])

        top.destroy()

        def update_listbox():
            listbox.delete(0, END)
            with open('tasks.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) > 0:
                        listbox.insert(END, row[0])

        update_listbox()

    label = Label(top, text='Enter the task name:')
    enter = Entry(top)
    btn = Button(top, text='OK', command=lambda: comp(enter.get()))
    label.pack()
    enter.pack()
    btn.pack()


def delete():
    top = Toplevel(root)

    def clear(name):
        with open('tasks.csv', 'r') as file:
            tasks = list(csv.reader(file))

        with open('tasks.csv', 'w', newline='') as write:
            writer = csv.writer(write)
            writer.writerows([row for row in tasks if row and len(row) > 0 and row[0].strip() != name.strip()])
            
        def update_listbox():
            listbox.delete(0, END)  
            with open('tasks.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) > 0:
                        listbox.insert(END, row[0])

        top.destroy()
        update_listbox()

    label = Label(top, text='Enter the task name:')
    enter = Entry(top)
    btn = Button(top, text='OK', command=lambda: clear(enter.get()))
    label.pack()
    enter.pack()
    btn.pack()


def info():
    top = Toplevel(root)

    def check(name):
        with open('tasks.csv', 'r') as file:
            tasks = list(csv.reader(file))

            for row in tasks:
                if  row[0].strip() == name.strip():
                    label2 = Label(top, text=f'Task Description: {row[1]}\nTime added: {row[3]}\nDue Date: {row[2]}')
                    label2.pack()

    def destro():
        top.destroy()

    label = Label(top, text='Enter the task name:')
    enter = Entry(top)
    btn = Button(top, text='Check', command=lambda: check(enter.get()))
    btn2 = Button(top, text='Cancel', command=destro)

    label.pack()
    enter.pack()
    btn.pack()
    btn2.pack()

def check_completed():
    top = Toplevel(root)

    with open('completed.csv', 'r') as file:
        completed_tasks = list(csv.reader(file))

    if not completed_tasks:
        label = Label(top, text='No completed tasks.')
        label.pack()
    else:
        label = Label(top, text='Completed Tasks:')
        label.pack()

        listbox_completed = Listbox(top, borderwidth=2, relief="groove", font=("Helvetica", 12))
        listbox_completed.pack()

        for row in completed_tasks:
            listbox_completed.insert(END, row[0])

    def destro():
        top.destroy()

    btn = Button(top, text='OK', command=destro)
    btn.pack()


def overdue_tasks():
    top = Toplevel(root)

    with open('tasks.csv', 'r') as file:
        tasks = list(csv.reader(file))

    label = Label(top, text='Overdue Tasks:')
    label.pack()

    listbox_overdue = Listbox(top, borderwidth=2, relief="groove", font=("Helvetica", 12))
    listbox_overdue.pack()

    for row in tasks:
        if row and len(row) > 2:
            due_date = datetime.strptime(row[2], '%Y-%m-%d')
            if due_date < datetime.today():
                listbox_overdue.insert(END, row[0])

    def destro():
        top.destroy()

    btn = Button(top, text='OK', command=destro)
    btn.pack()

root = Tk()
root.title("Task Manager")

label1 = Label(root, text='Tasks:', font=("Helvetica", 14, "bold"))
label2 = Label(root, text='Options', font=("Helvetica", 14, "bold"))
btn1 = Button(root, text='Add Task', command=open_add, width=15, height=2, font=("Helvetica", 12))
btn2 = Button(root, text='Complete Task', command=complete, width=15, height=2, font=("Helvetica", 12))
btn3 = Button(root, text='Delete Task', command=delete, width=15, height=2, font=("Helvetica", 12))
btn4 = Button(root, text='Task Info', command=info, width=15, height=2, font=("Helvetica", 12))
btn5 = Button(root, text='Check Completed Tasks', command=check_completed, width=30, height=2, font=("Helvetica", 12))
btn6 = Button(root, text='Overdue Tasks', command=overdue_tasks, width=30, height=2, font=("Helvetica", 12))

listbox = Listbox(root, borderwidth=2, relief="groove", font=("Helvetica", 12))
scrollbar = Scrollbar(root)

label1.grid(row=0, column=0, pady=10)
listbox.grid(row=1, column=0, padx=20, pady=10)
label2.grid(row=2, column=0, pady=10)
btn1.grid(row=3, column=0, pady=5)
btn2.grid(row=3, column=1, pady=5)
btn3.grid(row=4, column=0, pady=5)
btn4.grid(row=4, column=1, pady=5)
btn5.grid(row=5, column=0, columnspan=2, pady=10)
btn6.grid(row=6, column=0, columnspan=2, pady=10)
scrollbar.grid(row=1, column=1, sticky="ns")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

with open('tasks.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        listbox.insert(END, row[0])  

root.mainloop()
