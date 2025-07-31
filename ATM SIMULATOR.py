from dataclasses import dataclass
from tkinter import PhotoImage, Label, Entry, Button, Frame
from tkinter import messagebox
import datetime as dt
from tkinter.constants import VERTICAL
from tkinter.ttk import Combobox, Treeview, Scrollbar

#----------------------------------------------------------------------------
# ATM SIMULATOR

# MySQL CONNECTION
import mysql.connector as sql

db = sql.connect(host = 'localhost',
                 user = 'root',
                 password = 'Gaurav@07',
                 database = 'project')
cur = db.cursor()
cur.execute("create table if not exists ATM (ID int primary key auto_increment, NAME varchar(30), MOBILE varchar(10) unique, PIN varchar(4), BALANCE decimal(10,2) default 10000.00)")
cur.execute('create table if not exists TRANSACTION (ID int primary key auto_increment, DATE date, TIME time, MOBILE varchar(10), AMOUNT_BEFORE decimal(10,2), TYPE varchar(6), AMOUNT decimal(10,2), AMOUNT_AFTER decimal(10,2))')
db.commit()

# TKINTER ACTIVATE
import tkinter as tk
window = tk.Tk()

# WINDOW CONFIGURATION
window.title('HDFC ATM')
window.geometry('500x500')
window.resizable(False,False)
icon = PhotoImage(file = r"C:\Users\Gaurav\Downloads\hdfc logo.png")
window.iconphoto(True,icon)
window.config(bg = '#3498db')

# MENU
Label(window, text = 'USER LOGIN', bg = 'white', fg = 'red', font = ('bold',24)).place(x=150,y=30)
logo = PhotoImage(file = r"C:\Users\Gaurav\Downloads\hdfc logo.png")
Label(image=logo).place(x=10,y=10)

Label(window, text = 'MOBILE - ',bg = '#3498db', fg = 'white', font = ('bold',15)).place(x=100,y=100)
mobile_entry_log = Entry(width = 35)
mobile_entry_log.place(x=200,y=105)

Label(window, text = 'ATM PIN - ',bg = '#3498db', fg = 'white', font = ('bold',15)).place(x=100,y=180)
atm_pin_entry_log = Entry(width=35, show = '*')
atm_pin_entry_log.place(x=200,y=185)

# user check
def user_check():
    mobile = mobile_entry_log.get().strip()
    pin = atm_pin_entry_log.get().strip()

    # checking for empty user input
    if not mobile or not pin:
        messagebox.showerror(title = 'Error!',message = 'Empty input(s)!')
    else:
        # character length checking
        if not len(mobile) == 10 or not len(pin) == 4 or not pin.isdigit() or not mobile.isdigit():
            messagebox.showerror('Error!','Mobile number must be of 10 digits and ATM Pin number must be of 4 digits!')
            mobile_entry_log.delete(0,'end')
            atm_pin_entry_log.delete(0,'end')
            return

        # mobile number validation
        if not int(6000000000) < int(mobile) < 9999999999:
            messagebox.showerror('Error!','Invalid mobile number!')
            mobile_entry_log.delete(0,'end')
            return

        # checking credentials
        user_exist = None
        try:
            cur.execute('select * from ATM where mobile=%s and pin=%s', (mobile, pin))
            user_exist = cur.fetchone()
            db.commit()
            if not user_exist:
                messagebox.showerror('Error!', f'User not found!')
                return

        except Exception as ex:
            messagebox.showerror('Error!',f'Database error!\n{str(ex)}')
            mobile_entry_log.delete(0,'end')
            atm_pin_entry_log.delete(0,'end')

        # ------------------- user exist -------------------------
        if user_exist:
            mobile_entry_log.delete(0, 'end')
            atm_pin_entry_log.delete(0, 'end')
            messagebox.showinfo(title='Login successful!', message='Welcome back!')

            # user atm menu
            frame = Frame(window, width=500, height=500)
            frame.place(x=0, y=0)
            frame.config(bg='#3498db')

            logo_ = PhotoImage(file=r"C:\Users\Gaurav\Downloads\hdfc logo - Copy.png")
            Label(frame, image=logo_).place(x=10, y=10)
            frame.logo_ = logo_

            # getting info from the database and showing in the page
            cur.execute('select NAME from ATM where mobile=%s and pin=%s', (mobile, pin))
            show_name = cur.fetchone()[0]
            db.commit()

            Label(frame, text=f"Name - {show_name}", bg='#3498db', fg='white', font=('bold', 12)).place(x=100, y=20)
            Label(frame, text='MENU - ', bg='#3498db', fg='white', font=('bold', 15)).place(x=100, y=100)

            # balance check button
            def balance():
                frame_balance = Frame(window, width=500, height=500)
                frame_balance.place(x=0, y=0)
                frame_balance.config(bg='#3498db')

                logo_ = PhotoImage(file=r"C:\Users\Gaurav\Downloads\hdfc logo - Copy.png")
                Label(frame_balance, image=logo_).place(x=10, y=10)
                frame_balance.logo_ = logo_

                cur.execute('select balance from atm where mobile=%s and pin=%s', (mobile, pin))
                show_balance = cur.fetchone()[0]
                db.commit()

                Label(frame_balance, text=f"Your available balance - Rs. {show_balance}", bg='#3498db', fg='white',font=('bold', 12)).place(x=100, y=100)

                # go back button
                Button(frame_balance, text='Back to Menu', bg='white', bd=5, cursor='hand2', font=('bold', 12),command=frame_balance.destroy).place(x=370, y=400)

            Button(frame, text='Check Balance', bg='#3498db', fg='white', bd=0, cursor='hand2', font=('bold', 15),command=balance).place(x=100, y=150)

            # deposit button
            def deposit():
                frame_deposit = Frame(window, width = 500 , height = 500)
                frame_deposit.place(x=0, y=0)
                frame_deposit.config(bg='#3498db')

                logo_ = PhotoImage(file=r"C:\Users\Gaurav\Downloads\hdfc logo - Copy.png")
                Label(frame_deposit, image=logo_).place(x=10, y=10)
                frame_deposit.logo_ = logo_

                Label(frame_deposit, text = 'Deposit Amount (Rs.) - ', bg='#3498db', fg='white',font=('bold', 12)).place(x=100,y=100)
                entry_deposit = Entry(frame_deposit,width = 35)
                entry_deposit.place(x=100,y=150)

                def submit_deposit():
                    # amount checking
                    amount = entry_deposit.get().strip()
                    if not amount.isdigit() or not int(amount) >= 100 or not (int(amount) % 100 == 0):
                        messagebox.showerror('Error!','Amount must be a positive number which is a multiple of 100!')
                        entry_deposit.delete(0,'end')
                        return

                    # amount saving in the database
                    d = dt.datetime.now()
                    date = d.strftime('%Y-%m-%d')
                    time = d.strftime('%H:%M:%S')

                    cur.execute('select BALANCE from atm where mobile=%s and pin=%s', (mobile, pin))
                    show_balance = cur.fetchone()[0]
                    db.commit()
                    amount_before = show_balance
                    type_ = 'Credit'
                    amount_after = float(show_balance)+float(amount)

                    cur.execute('update atm set balance = balance + %s where mobile=%s and pin=%s',(float(amount),mobile,pin))
                    cur.execute('insert into transaction (DATE,TIME,MOBILE,AMOUNT_BEFORE,TYPE,AMOUNT,AMOUNT_AFTER) values(%s,%s,%s,%s,%s,%s,%s)',(date,time,mobile,float(amount_before),type_,float(amount),float(amount_after)))
                    db.commit()
                    messagebox.showinfo('Deposit successful!',f'You have successfully deposited Rs.{amount}.')
                    entry_deposit.delete(0,'end')

                # deposit submit button
                Button(frame_deposit, text = 'SUBMIT' , bg = 'white', bd = 5, font = ('bold',20), cursor = 'hand2', command = submit_deposit).place(x=190,y=350)

                # go back button
                Button(frame_deposit, text='Back to Menu', bg='white', bd=5, cursor='hand2', font=('bold', 12),command=frame_deposit.destroy).place(x=370, y=400)

            Button(frame, text='Cash Deposit', bg='#3498db', fg='white', bd=0, cursor='hand2', font=('bold', 15) , command = deposit).place(x=100, y=200)

            # withdraw button
            def withdraw():
                frame_withdraw = Frame(window, width = 500 , height = 500)
                frame_withdraw.place(x=0,y=0)
                frame_withdraw.config(bg='#3498db')

                logo_ = PhotoImage(file=r"C:\Users\Gaurav\Downloads\hdfc logo - Copy.png")
                Label(frame_withdraw, image=logo_).place(x=10, y=10)
                frame_withdraw.logo_ = logo_

                Label(frame_withdraw, text='Withdraw Amount (Rs.) - ', bg='#3498db', fg='white', font=('bold', 12)).place(x=100, y=100)
                entry_withdraw = Entry(frame_withdraw, width=35)
                entry_withdraw.place(x=100, y=150)

                def submit_withdraw():
                    amount = entry_withdraw.get().strip()
                    if not amount.isdigit() or not int(amount) >= 100 or not int(amount) % 100 == 0:
                        messagebox.showerror('Error!', 'Amount must be a positive number and multiple of 100 (minimum Rs.100 for withdrawal) and must be within your available balance amount!')
                        entry_withdraw.delete(0, 'end')
                        return

                    # getting available balance amount
                    cur.execute('select balance from atm where mobile=%s and pin=%s',(mobile,pin))
                    balance_ = cur.fetchone()
                    available_balance = balance_[0]
                    db.commit()

                    if not int(amount) <= available_balance or not int(amount) <= 20000:
                        messagebox.showerror('Error!','You cannot withdraw amount exceeding limits - \n1. Rs. 20,000 (per transaction).\n2. Amount exceeding your available balance.')
                        return

                    # amount deduction saving in the database
                    d = dt.datetime.now()
                    date = d.strftime('%Y-%m-%d')
                    time = d.strftime('%H:%M:%S')
                    cur.execute('select BALANCE from atm where mobile=%s and pin=%s', (mobile, pin))

                    show_balance = cur.fetchone()[0]
                    amount_before = show_balance
                    type_ = 'Debit'
                    amount_after = float(show_balance) - float(amount)

                    cur.execute('update atm set balance = balance - %s where mobile=%s and pin=%s',(float(amount),mobile,pin))
                    cur.execute('insert into transaction (DATE,TIME,MOBILE,AMOUNT_BEFORE,TYPE,AMOUNT,AMOUNT_AFTER) values(%s,%s,%s,%s,%s,%s,%s)',(date, time, mobile, float(amount_before), type_, float(amount), float(amount_after)))
                    db.commit()
                    messagebox.showinfo('Withdrawal successful!', f'You have successfully withdrew Rs.{amount}.')
                    entry_withdraw.delete(0, 'end')

                # deposit submit button
                Button(frame_withdraw, text='SUBMIT', bg='white', bd=5, font=('bold', 20), cursor='hand2',command = submit_withdraw).place(x=190, y=350)

                # go back button
                Button(frame_withdraw, text='Back to Menu', bg='white', bd=5, cursor='hand2', font=('bold', 12),command=frame_withdraw.destroy).place(x=370, y=400)

            Button(frame, text='Cash Withdraw', bg='#3498db', fg='white', bd=0, cursor='hand2', font=('bold', 15) , command = withdraw).place(x=100, y=250)

            # view transaction button
            def transaction(): # THIS FEATURE NOT WOKING PROPERLY!!!!!!!!!!!
                frame_transaction = Frame(window,width = 500 , height = 500)
                frame_transaction.place(x=0,y=0)
                frame_transaction.config(bg='#3498db')

                logo_ = PhotoImage(file=r"C:\Users\Gaurav\Downloads\hdfc logo - Copy.png")
                Label(frame_transaction, image=logo_).place(x=10, y=10)
                frame_transaction.logo_ = logo_

                Label(frame_transaction, text='View Transaction - ', bg='#3498db', fg='white',font=('bold', 12)).place(x=100, y=100)
                choices = Combobox(frame_transaction,values=["LAST 5","LAST 10","1 MONTH","2 MONTHS","6 MONTHS","BY DATE"],state='readonly')
                choices.set("LAST 5")
                choices.place(x=250,y=103)

                def submit_transaction():
                    choice = choices.get()

                    if choice == 'LAST 5':
                        # removing table for previous data, if any
                        for i in frame_transaction.winfo_children():
                            if isinstance(i, Treeview):
                                i.destroy()

                        # checking if data is available in the database
                        cur.execute('select DATE,TIME,TYPE,AMOUNT from transaction where mobile=%s', (mobile,))
                        tran = cur.fetchall()
                        if not tran:
                            messagebox.showerror('Error!', 'Your transaction log is empty!')
                            return

                        # creating new table for new data
                        columns = ("DATE", "TIME", "TYPE", "AMOUNT")
                        table = Treeview(frame_transaction, columns=columns, show='headings', height=5)
                        # column heading
                        '''table.heading('ID', text='ID')
                        table.heading('Date', text='Date')
                        table.heading('Time', text='Time')
                        table.heading('Type', text='Type')
                        table.heading('Amount', text='Amount')'''
                        # or this way
                        for i in columns:
                            table.heading(i, text=i)  # headings done
                            table.column(i, width=80)

                        # inserting data into table
                        cur.execute(
                            'select DATE,TIME,TYPE,AMOUNT from transaction where mobile=%s order by ID desc limit 5',
                            (mobile,))
                        last5 = cur.fetchall()
                        for i in last5:
                            table.insert('', 'end', values=i)

                        # table placement in the frame
                        table.place(x=103, y=160)

                    elif choice == 'LAST 10':
                        # removing table for previous data, if any
                        for i in frame_transaction.winfo_children():
                            if isinstance(i, Treeview):
                                i.destroy()

                        # checking if data is available in the database
                        cur.execute('select DATE,TIME,TYPE,AMOUNT from transaction where mobile=%s', (mobile,))
                        tran = cur.fetchall()
                        if not tran:
                            messagebox.showerror('Error!', 'Your transaction log is empty!')
                            return

                        # creating new table for new data
                        columns = ("DATE", "TIME", "TYPE", "AMOUNT")
                        table = Treeview(frame_transaction, columns=columns, show='headings', height=5)
                        # column heading
                        '''table.heading('ID', text='ID')
                        table.heading('Date', text='Date')
                        table.heading('Time', text='Time')
                        table.heading('Type', text='Type')
                        table.heading('Amount', text='Amount')'''
                        # or this way
                        for i in columns:
                            table.heading(i, text=i)  # headings done
                            table.column(i, width=80)

                        # inserting data into table
                        cur.execute(
                            'select DATE,TIME,TYPE,AMOUNT from transaction where mobile=%s order by ID desc limit 10',
                            (mobile,))
                        last5 = cur.fetchall()
                        for i in last5:
                            table.insert('', 'end', values=i)

                        # table placement in the frame
                        table.place(x=103, y=160)

                    #elif choice == '1 MONTH':

                    #elif choice == '2 MONTHS':

                    # elif choice == '6 MONTHS':

                    # elif choice == 'BY DATE':


                # transaction submit button
                Button(frame_transaction, text='SUBMIT', bg='white', bd=5, font=('bold', 20), cursor='hand2', command = submit_transaction).place(x=190, y=350)

                # go back button
                Button(frame_transaction, text='Back to Menu', bg='white', bd=5, cursor='hand2', font=('bold', 12),command=frame_transaction.destroy).place(x=370, y=400)

            Button(frame, text = 'View Transaction', bg='#3498db', fg='white', bd=0, cursor='hand2', font=('bold', 15) , command = transaction).place(x=100, y=300)

            # go back to LOGIN PAGE (EXIT)
            Button(frame, text='Exit', bg='white', font=('bold', 15), bd=5, cursor='hand2',command=frame.destroy).place(x=400, y=400)

# LOGIN BUTTON
Button(window,text = 'LOGIN', bg = 'white', font = ('bold',20), bd = 5, cursor = 'hand2', command = user_check).place(x=200,y=260)

# user registration
def user_registration():
    frame = Frame(window,width = 500, height = 500)
    frame.place(x=0,y=0)
    frame.config(bg = '#3498db')

    Label(frame,text = 'USER REGISTRATION', bg = 'white', fg = 'red', font = ('bold',24)).place(x=125,y=30)
    logo_ = PhotoImage(file = r"C:\Users\Gaurav\Downloads\hdfc logo - Copy.png")
    Label(frame,image = logo_).place(x=10,y=10)
    frame.logo_ = logo_ # WITHOUT THIS YOU WON'T SEE THE IMAGE, THIS IS FOR REFERENCE!

    Label(frame,text = 'NAME - ',bg = '#3498db', fg = 'white', font = ('bold',15)).place(x=100,y=100)
    name_entry_reg = Entry(frame,width = 35)
    name_entry_reg.place(x=230,y=105)

    Label(frame,text = 'MOBILE - ',bg = '#3498db', fg = 'white', font = ('bold',15)).place(x=100,y=150)
    mobile_entry_reg = Entry(frame,width = 35)
    mobile_entry_reg.place(x=230,y=155)

    Label(frame,text = 'ATM PIN - ',bg = '#3498db', fg = 'white', font = ('bold',15)).place(x=100,y=200)
    atm_pin_entry_reg1 = Entry(frame,width = 35)
    atm_pin_entry_reg1.place(x=230,y=205)

    Label(frame,text = 'RE-ENTER\nATM PIN - ',bg = '#3498db', fg = 'white', font = ('bold',14)).place(x=100,y=250)
    atm_pin_entry_reg2 = Entry(frame, width=35)
    atm_pin_entry_reg2.place(x=230, y=265)

    Label(frame, text='Minimum A/c Balance - Rs. 10,000.00', bg='#3498db', fg='white', font=('bold', 12)).place(x=100, y=315)

    def submit_registration():
        # getting user inputs
        name = name_entry_reg.get().strip().title()
        mobile = mobile_entry_reg.get().strip()
        pin1 = atm_pin_entry_reg1.get().strip()
        pin2 = atm_pin_entry_reg2.get().strip()

        # checking for empty user input
        if not name or not mobile or not pin1 or not pin2:
            messagebox.showerror(title='Error!', message='Empty input(s)!')

        else:
            # user input validation
            if not len(name) <= 30:
                messagebox.showerror(title='Error!', message='Name is too long, must be within 30 characters!')
                name_entry_reg.delete(0,'end')

            elif not len(mobile) == 10 or not mobile.isdigit() or not int(6000000000) < int(mobile) < int(9999999999):
                messagebox.showerror(title='Error!', message='Invalid mobile number!')
                mobile_entry_reg.delete(0,'end')

            elif not pin1 == pin2 or not pin1.isdigit() or not pin2.isdigit() or not len(pin1) == 4 or not len(pin2) == 4:
                messagebox.showerror(title='Error!', message='ATM Pin Number must be matching and of 4 digits!')
                atm_pin_entry_reg1.delete(0,'end')
                atm_pin_entry_reg2.delete(0, 'end')

            else:
                try:
                    # user duplicate check
                    cur.execute('select MOBILE from atm where mobile=%s and pin=%s',(mobile,pin1))
                    duplicate_ = cur.fetchone()
                    if duplicate_:
                        messagebox.showerror('Error!','This mobile number is already registered with us!')

                    # user being registered
                    else:
                        cur.execute("create table if not exists ATM (ID int primary key auto_increment, NAME varchar(30), MOBILE varchar(10) unique, PIN varchar(4), BALANCE decimal(10,2) default 10000.00)")
                        cur.execute('insert into ATM (NAME,MOBILE,PIN) values(%s,%s,%s)',(name,mobile,pin1))
                        messagebox.showinfo(title = 'Registration successful!', message = 'Thanks for registering with HDFC!')
                        db.commit()

                except Exception as ex:
                    messagebox.showerror('Error!',f"Database error!\n{str(ex)}")

    # SUBMIT REGISTRATION FORM BUTTON
    Button(frame,text = 'SUBMIT', bg = 'white', bd = 5, font = ('bold',20), cursor = 'hand2', command = submit_registration).place(x=190,y=350)

    # GO BACK TO LOGIN PAGE
    Button(frame,text = 'Back to Login Page', bg = '#3498db' , bd = 0 , fg = 'white',font = ('bold',12) , command = frame.destroy).place(x=330,y=370)

# REGISTRATION BUTTON
Button(window,text = "Don't have an account?\nREGISTER here", bg = '#3498db', fg = 'white', bd = 0, font = ('bold',12), cursor = 'hand2', command = user_registration).place(x=170,y=350)

# GUI CLOSE BUTTON
Button(window, text = 'EXIT', bg='red', font=('bold', 15), bd=5, cursor='hand2',command=window.destroy).place(x=400, y=400)

window.mainloop()

db.close()
cur.close()