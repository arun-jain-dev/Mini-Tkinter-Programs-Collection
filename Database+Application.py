from tkinter import *
from tkinter import ttk
import datetime
import time
import tkinter.messagebox
import sqlite3
 
class School_Portal():
    db_name = 'student.db'
 
    def __init__(self,root):
        self.root = root
        self.root.title('Students Data')
 
        #--------------Logo and Title----------------
 
        self.photo = PhotoImage(file='gp1.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0,column=0)
 
        self.label1 = Label(font=('arial',15,'bold'),text='School Portal System',fg='dark blue')
        self.label1.grid(row=8,column=0)
 
        #--------------New Record--------------------
        frame = LabelFrame(self.root, text='Add New Record')
        frame.grid(row=0,column=1)
 
        Label(frame,text='Firstname:').grid(row=1,column=1,sticky=W)
        self.firstname = Entry(frame)
        self.firstname.grid(row=1,column=2)
 
        Label(frame, text='Lastname:').grid(row=2, column=1, sticky=W)
        self.lastname = Entry(frame)
        self.lastname.grid(row=2, column=2)
 
        Label(frame, text='Username:').grid(row=3, column=1, sticky=W)
        self.username = Entry(frame)
        self.username.grid(row=3, column=2)
 
        Label(frame, text='Email:').grid(row=4, column=1, sticky=W)
        self.email = Entry(frame)
        self.email.grid(row=4, column=2)
 
        Label(frame, text='Subject:').grid(row=5, column=1, sticky=W)
        self.subject = Entry(frame)
        self.subject.grid(row=5, column=2)
 
        Label(frame, text='Age:').grid(row=6, column=1, sticky=W)
        self.age = Entry(frame)
        self.age.grid(row=6, column=2)
 
        #------------------Add Button------------------
        ttk.Button(frame,text='Add Record', command = self.add).grid(row=7,column=2)
 
        #-----------------Message Display---------------
        self.message = Label(text='',fg='red')
        self.message.grid(row=8,column=1)
 
        #----------------Database Table Display Box----
        self.tree = ttk.Treeview(height=10, column=['','','','','',''])
        self.tree.grid(row=9,column=0,columnspan=2)
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50)
        self.tree.heading('#1', text='Firstname')
        self.tree.column('#1', width=80)
        self.tree.heading('#2', text='Lastname')
        self.tree.column('#2', width=80)
        self.tree.heading('#3', text='Username')
        self.tree.column('#3', width=80)
        self.tree.heading('#4', text='Email')
        self.tree.column('#4', width=120)
        self.tree.heading('#5', text='Subject')
        self.tree.column('#5', width=80)
        self.tree.heading('#6', text='Age')
        self.tree.column('#6', width=40, stretch=False)
 
        #----------------Time and Date-----------------
        def tick():
            d = datetime.datetime.now()
            Today = '{:%B %d, %Y}'.format(d)
 
            mytime = time.strftime('%I:%M:%S %p')
            self.lblInfo.config(text=(mytime+'\t'+Today))
            self.lblInfo.after(200,tick)
 
        self.lblInfo = Label(font=('arial',20,'bold'),fg='dark blue')
        self.lblInfo.grid(row=10,column=0,columnspan=2)
        tick()
 
        #------------------Menu Bar-----------------------
        Chooser = Menu()
        itemone = Menu()
 
        itemone.add_command(label = 'Add Record', command = self.add)
        itemone.add_command(label='Edit Record', command = self.edit)
        itemone.add_command(label='Delete Record', command = self.dele)
        itemone.add_separator()
        itemone.add_command(label='Help', command = self.help)
        itemone.add_command(label='Exit', command = self.ex)
 
        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_cascade(label='Add', command = self.add)
        Chooser.add_cascade(label='Edit', command = self.edit)
        Chooser.add_cascade(label='Delete', command = self.dele)
        Chooser.add_cascade(label='Help', command = self.help)
        Chooser.add_cascade(label='Exit', command = self.ex)
 
        root.config(menu=Chooser)
 
        self.viewing_records()
 
    # ---------------View Database Table---------------
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result
 
    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM studentlist'
        db_table = self.run_query(query)
        for data in db_table:
            self.tree.insert('',1000,text=data[0],values=data[1:])
 
    #-----------------Add New Record---------------------------
    def validation(self):
        return len(self.firstname.get()) !=0 and len(self.lastname.get()) !=0 and len(self.username.get()) !=0 and \
               len(self.email.get()) !=0 and len(self.subject.get()) !=0 and len(self.age.get()) !=0
 
    def add_record(self):
        if self.validation():
            query = 'INSERT INTO studentlist VALUES (NULL,?,?,?,?,?,?)'
            parameters = (self.firstname.get(),self.lastname.get(),self.username.get(),self.email.get(),
                          self.subject.get(),self.age.get())
            self.run_query(query,parameters)
            self.message['text']='Record {} {} is added'.format(self.firstname.get(),self.lastname.get())
 
            #--------------------Clear Fields---------------------
            self.firstname.delete(0,END)
            self.lastname.delete(0, END)
            self.username.delete(0, END)
            self.email.delete(0, END)
            self.subject.delete(0, END)
            self.age.delete(0, END)
 
        else:
            self.message['text'] = 'Fields not completed! Fill all fields...'
 
        self.viewing_records()
 
    def add(self):
        ad = tkinter.messagebox.askquestion('Add Record','Want to Add a new Record?')
        if ad == 'yes':
            self.add_record()
 
    def delete_record(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][1]
 
        except IndexError as e:
            self.message['text']='Please, select a record to delete'
            return
 
        self.message['text'] = ''
        number = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM studentlist WHERE ID = ?'
        self.run_query(query,(number,))
        self.message['text'] = 'Record {} is deleted'.format(number)
 
        self.viewing_records()
 
    def dele(self):
        de = tkinter.messagebox.askquestion('Delete Record','Want to Delete a record?')
        if de ==  'yes':
            self.delete_record()
 
    # -------------------Edit Record----------------------------------
    def edit_box(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
 
        except IndexError as e:
            self.message['text']='Please, select a record to edit'
            return
 
        fname = self.tree.item(self.tree.selection())['values'][0]
        lname = self.tree.item(self.tree.selection())['values'][1]
        uname = self.tree.item(self.tree.selection())['values'][2]
        email = self.tree.item(self.tree.selection())['values'][3]
        subject = self.tree.item(self.tree.selection())['values'][4]
        age = self.tree.item(self.tree.selection())['values'][5]
 
        self.edit_root = Toplevel()
        self.edit_root.title('Edit Record')
 
        Label(self.edit_root, text = 'Old Firstname').grid(row = 0, column = 1, sticky = W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=fname),state='readonly').grid(row=0,column=2)
        Label(self.edit_root, text='New Firstname').grid(row=1, column=1, sticky=W)
        new_fname = Entry(self.edit_root)
        new_fname.grid(row = 1, column = 2)
 
        Label(self.edit_root, text='Old Lastname').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=lname), state='readonly').grid(row=2,column=2)
        Label(self.edit_root, text='New Lastname').grid(row=3, column=1, sticky=W)
        new_lname = Entry(self.edit_root)
        new_lname.grid(row=3, column=2)
 
        Label(self.edit_root, text='Old Username').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=uname), state='readonly').grid(row=4,column=2)
        Label(self.edit_root, text='New Username').grid(row=5, column=1, sticky=W)
        new_uname = Entry(self.edit_root)
        new_uname.grid(row=5, column=2)
 
        Label(self.edit_root, text='Old Email').grid(row=6, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=email), state='readonly').grid(row=6, column=2)
        Label(self.edit_root, text='New Email').grid(row=7, column=1, sticky=W)
        new_email = Entry(self.edit_root)
        new_email.grid(row=7, column=2)
 
        Label(self.edit_root, text='Old Subject').grid(row=8, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=subject), state='readonly').grid(row=8,column=2)
        Label(self.edit_root, text='New Subject').grid(row=9, column=1, sticky=W)
        new_subject = Entry(self.edit_root)
        new_subject.grid(row=9, column=2)
 
        Label(self.edit_root, text='Old Age').grid(row=10, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=age), state='readonly').grid(row=10,column=2)
        Label(self.edit_root, text='New Age').grid(row=11, column=1, sticky=W)
        new_age = Entry(self.edit_root)
        new_age.grid(row=11, column=2)
 
        Button(self.edit_root, text='save changes',
               command=lambda: self.edit_record(new_fname.get(), fname, new_lname.get(), lname, new_uname.get()
                                                , uname,new_email.get(), email, new_subject.get(), subject
                                                , new_age.get(),age)).grid(row=12, column=2, sticky=W)
        self.edit_root.mainloop()
 
    def edit_record(self,new_fname,fname,new_lname,lname,new_uname,uname,new_email,email,new_subject,subject,new_age,age):
        query = 'UPDATE studentlist SET Firstname=?, Lastname=?, Username=?, Email=?, Subject=?, Age=? WHERE Firstname=?' \
                'AND Lastname=? AND Username=? AND Email=? AND Subject=? AND Age=?'
        parameters = (new_fname,new_lname,new_uname,new_email,new_subject,new_age,fname,lname,uname,email,subject,age)
        self.run_query(query,parameters)
        self.edit_root.destroy()
        self.message['text'] = '{} details were changed to {}'.format(fname,new_fname)
        self.viewing_records()
 
    def edit(self):
        ed = tkinter.messagebox.askquestion('Edit Record','Want to Edit a record?')
        if ed == 'yes':
            self.edit_box()
 
    def help(self):
        tkinter.messagebox.showinfo('Log','Report sent')
 
    def ex(self):
        exit = tkinter.messagebox.askquestion('Exit Application','Want to close your app?')
        if exit == 'yes':
            root.destroy()
 
 
 
 
if __name__ == '__main__':
    root = Tk()
    root.geometry('530x465+500+200')
    application = School_Portal(root)
    root.mainloop()