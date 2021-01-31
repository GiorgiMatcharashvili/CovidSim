import Errors
import sqlite3
from tkinter import *
from tkinter import ttk


conn = sqlite3.connect('CovidSim_Database.db')
c = conn.cursor()

def create():
    c.execute('CREATE TABLE IF NOT EXISTS patients (id Text,Name TEXT,Surname TEXT,Date TEXT,IDnum TEXT,Area TEXT,Status TEXT)')
create()
def readAll():
    lst = []
    c.execute('SELECT * FROM patients')
    for i in c.fetchall():
        lst.append(i)
    return lst

def checkId(id):
    lst = []
    c.execute('SELECT IDnum FROM patients')
    for i in c.fetchall():
        lst.append(i[0])
    if id in lst:
        return True
    else:
        return False

def lastId():
    lst = []
    c.execute('SELECT id FROM patients')
    for i in c.fetchall():
        lst.append(int(i[0]))
    try:
        return str(max(lst))
    except:
        return "0"

def addpat(di,name,surname,date,id,area,status):
    create()
    c.execute("INSERT INTO patients (id,Name,Surname,Date,IDnum,Area,Status) VALUES (?,?,?,?,?,?,?)",
              (di,name,surname,date,id,area,status))
    conn.commit()

root = Tk()
root.geometry("500x200")
root.title("CovidSim")
root.configure(bg="#80b3ff")
root.iconbitmap('C:\\Users\\nemoh\\OneDrive\\Desktop\\icon2.ico')

root_menu = Menu(root)
root.config(menu=root_menu)

def addPatient():
    add = Toplevel()
    add.title("Add new patient")
    add.configure(bg="#80b3ff")
    add.geometry("550x150")
    add.iconbitmap('C:\\Users\\nemoh\\OneDrive\\Desktop\\icon2.ico')

    def error(msg):
        error_message['text'] = ""

        def make_error():
            if "successfully" in msg:
                error_message['fg'] = "green"
            else:
                error_message['fg'] = "red"
            error_message['text'] = msg

        add.after(30, make_error)

    def create_new():
        pname = name.get()
        psurname = surname.get()
        pdate = date.get()
        pid = ID.get()
        parea = area.get()
        pstatus = status.get()

        answer = Errors.check(pname,psurname,pdate,pid,parea,pstatus)

        if "successfully" in answer:
            create()
            lastid = lastId()
            answer = checkId(pid)
            if answer == False:
                addpat(str(int(lastid)+1),pname,psurname,pdate,pid,parea,pstatus)
                answer = "Patient added successfully"
            else:
                answer = "Id already exists."
        error(answer)


    Label(add, text="Please fill all the fields to add new patient", fg="black", bg="#80b3ff").grid(row=0,column=0,
                                                                                                    columnspan=5)

    Label(add, text="Name:", fg="black", bg="#80b3ff").grid(row=1, column=0)
    Label(add, text="Surname:", fg="black", bg="#80b3ff").grid(row=1, column=2)
    Label(add, text="Date of the birth(dd/mm/yyyy):", fg="black", bg="#80b3ff").grid(row=2, column=0)
    Label(add, text="ID number:", fg="black", bg="#80b3ff").grid(row=2, column=2)
    Label(add, text="Infection area:", fg="black", bg="#80b3ff").grid(row=3, column=0)
    Label(add, text="Status:", fg="black", bg="#80b3ff").grid(row=3, column=2)

    error_message = Label(add, text="",bg="#80b3ff" ,fg="red")
    error_message.grid(row=4, column=2, columnspan=4)


    name = Entry(add,width=20, bg="white", fg="black", borderwidth=1)
    surname = Entry(add, width=20, bg="white",fg="black", borderwidth=1)
    date = Entry(add, width=20, bg="white", fg="black", borderwidth=1)
    ID = Entry(add, width=20, bg="white", fg="black", borderwidth=1)
    area = Entry(add, width=20, bg="white", fg="black", borderwidth=1)
    status = Entry(add, width=20, bg="white", fg="black", borderwidth=1)

    name.grid(row=1,column=1)
    surname.grid(row=1, column=3)
    date.grid(row=2, column=1)
    ID.grid(row=2, column=3)
    area.grid(row=3, column=1)
    status.grid(row=3, column=3)

    addButton = Button(add,text="Create", padx=25, pady=3, bg="#ADD8E6", fg="black", command=create_new).grid(row=4,
                                                                                                column=0)

def changePatient():
    search = Toplevel()
    search.title("Search patient")
    search.configure(bg="#80b3ff")
    search.geometry("300x200")
    search.iconbitmap('C:\\Users\\nemoh\\OneDrive\\Desktop\\icon2.ico')

    def find():
        def do():
            status = i[6]
            newStatus = doEntry.get()
            if newStatus in Errors.statuses:
                if status == 'dead':
                    error_mes['text'] = "You can't change status."
                elif status == "recovered" and newStatus != "dead":
                    c.execute('DELETE FROM patients WHERE IDnum = ' + str(id))
                    conn.commit()
                    addpat(i[0], i[1], i[2], i[3], i[4], i[5], str(newStatus))
                    conn.commit()
                elif status == "infected":
                    #c.execute('UPDATE patients SET Status = '+str(newStatus)+' WHERE IDnum='+str(id))
                    c.execute('DELETE FROM patients WHERE IDnum = '+str(id))
                    conn.commit()
                    addpat(i[0],i[1],i[2],i[3],i[4],i[5],str(newStatus))
                    conn.commit()
                else:
                    error_mes['text']="Invalid Status"
            elif newStatus == "remove":
                c.execute('DELETE FROM patients WHERE IDnum = ' + str(id))
                conn.commit()
            else:
                error_mes['text']="Invalid Status"

        id = detail.get()
        c.execute('SELECT * FROM patients WHERE IDnum='+str(id))
        for i in c.fetchall():
            detpat['text']= str("|".join(i))

        Label(search,text="Enter Status:",bg="#80b3ff").grid(row=2,column=0)
        doEntry = Entry(search,width=20, bg="white", fg="black", borderwidth=1)
        doEntry.grid(row=2, column=1)
        doButton = Button(search, text="Do",bg="red",command=do).grid(row=2,column=2)

    Label(search, text="Enter Id:",bg="#80b3ff").grid()
    detail = Entry(search,width=20, bg="white", fg="black", borderwidth=1)
    detail.grid(row=0,column=1)
    SearchButton = Button(search, text="Search",bg="red",command=find).grid(row=0,column=2,columnspan=3)
    detpat = Label(search, text = "", bg="#80b3ff")
    detpat.grid(row=1, column=0,columnspan=5)
    error_mes = Label(search, text="", bg="#80b3ff")
    error_mes.grid(row=3,columnspan=3)

def viewPatient():
    view = Toplevel()
    view.title("view patients")
    view.configure(bg="#80b3ff")
    view.geometry("600x400")
    view.iconbitmap('C:\\Users\\nemoh\\OneDrive\\Desktop\\icon2.ico')

    Label(view, text="id|Name|Surname|Date|IDnum|Area|Status", font=("Courier", 15),bg="#80b3ff").pack()

    main_frame = Frame(view)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas)

    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")


    lst = readAll()
    for i in lst:
        Label(second_frame, text="|".join(i),font=("Courier", 12)).grid(row=int(i[0]), column=0)

Label(root, text="Welcome back!", fg="black",bg="#80b3ff").pack()
Label(root, text="___________________________", fg="black",bg="#80b3ff").pack()
Label(root, text="This is the program for counting covid-19 infected patients.", fg="black",bg="#80b3ff").pack()
Label(root, text="Click 'Menu' and next 'Add' to Add new patients.", fg="black",bg="#80b3ff").pack()
Label(root, text="Click 'Change' to change status of patients.", fg="black",bg="#80b3ff").pack()
Label(root, text="Click 'view' to see every patients.", fg="black",bg="#80b3ff").pack()


file_menu = Menu(root_menu)
admin_menu = Menu(root_menu)

root_menu.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="Add", command=addPatient)
file_menu.add_command(label="View", command=viewPatient)
file_menu.add_command(label="Change", command=changePatient)
file_menu.add_command(label="Exit", command=root.quit)


root.mainloop()
c.close()
conn.close()