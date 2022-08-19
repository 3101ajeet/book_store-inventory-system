import email
from email.mime import base
from http import client
from re import T
import sqlite3
from tkinter import*
from tkinter import messagebox
import pyotp
from timeit import default_timer as dt
from twilio.rest import Client
from django import views
from tkinter import ttk
#import registration_page

class LoginPage:
    def __init__(self, root):
        self.root=root
        self.root.title("Inventory Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="peachpuff")

        lbl_title=Label(self.root, text="Login Page", relief="groove", font=("arial", 20, "bold"), fg="green", bg="lightyellow", bd=10)
        lbl_title.pack(side=TOP, fill=X)

        self.email=StringVar()
        self.email_forget=StringVar()
        self.login_password=StringVar()
        self.pw_forget=StringVar()
        self.C_password=StringVar()
        self.contact_no=StringVar()
        self.enter_otp=StringVar()
        self.otp_db_ent=StringVar()

        f_login_frame=LabelFrame(self.root, text="LogIn", font=("arial", 25, "bold"), bg="peachpuff", relief=RIDGE, bd=3)
        f_login_frame.place(x=20, y=65, height=310, width=650)

        m_login_email=Label(f_login_frame, text="Email", font=("arial", 15, "bold"), bg="light green", relief="raised")
        m_login_email.place(x=10, y=15, height=40, width=200)
        self.txt_login_email=Entry(f_login_frame, font=("arial", 15), bd=3, relief="ridge", bg="light blue", textvariable=self.email)
        self.txt_login_email.place(x=210, y=15, height=40, width=420)

        m_login_password=Label(f_login_frame, text="Password", font=("arial", 15, "bold"), bg="light green", relief="raised")
        m_login_password.place(x=10, y=65, height=40, width=200)
        self.txt_login_password=Entry(f_login_frame, font=("arial", 15), bd=3, relief="ridge", bg="light blue", textvariable=self.login_password, show="*")
        self.txt_login_password.place(x=210, y=65, height=40, width=420)

        b_fg_login=Button(f_login_frame, text="Login", cursor="hand2",bd=5, font=("arial", 15, "bold"), bg="light pink", command=self.checkFieldLogin)
        b_fg_login.place(x=150, y=125, height=40, width="250")
        # btn_rgtn=Button(f_login_frame, text="Registration", cursor="hand2",bd=5, font=("arial", 15, "bold"), bg="light pink", command="")
        # btn_rgtn.place(x=280, y=125, height=40, width="250")
        
        self.btn_db=Button(f_login_frame, text="DataBase", cursor="hand2",bd=5, font=("arial", 15, "bold"), bg="light pink", command=self.db)
        self.btn_db.place(x=10, y=180, height=40, width="250")

        otp_lbl_db=Label(f_login_frame, text="OTP", font=("arial", 15, "bold"), bg="light green", relief="raised")
        otp_lbl_db.place(x=280, y=180, height=40, width=90)
        self.otp_DB=Entry(f_login_frame, font=("arial", 15), bd=3, relief="ridge", bg="light blue", textvariable=self.otp_db_ent)
        self.otp_DB.place(x=370, y=180, height=40, width=100)
        btn_otp_ok=Button(f_login_frame, text="Ok", cursor="hand2",bd=5, font=("arial", 15, "bold"), bg="light pink", command=self.detail)
        btn_otp_ok.place(x=480, y=180, height=40, width="50")

        f_pw_frame=LabelFrame(self.root, text="Forget Password", font=("arial", 25, "bold"), bg="peachpuff", relief=RIDGE, bd=3)
        f_pw_frame.place(x=20, y=435, height=250, width=650)

        email_lbl=Label(f_pw_frame, text="Enter your registered email", font=("arial", 15, "bold"), bg="light green", relief=RAISED)
        email_lbl.place(x=10, y=25, height=40, width=310)
        self.email_ent=Entry(f_pw_frame, font=("arial", 15), bd=3, textvariable=self.email_forget, relief=RIDGE, bg="lightblue")
        self.email_ent.place(x=325, y=25, height=40, width=305)
        
        mbl_lbl=Label(f_pw_frame, text="Enter your registered mobile no.", font=("arial", 15, "bold"), bg="light green", relief=RAISED)
        mbl_lbl.place(x=10, y=75, height=40, width=310)
        self.mbl_ent=Entry(f_pw_frame, font=("arial", 15), bd=3, textvariable=self.contact_no, relief=RIDGE, bg="lightblue")
        self.mbl_ent.place(x=325, y=75, height=40, width=150)

        otp_lbl=Label(f_pw_frame, text="Enter OTP", font=("arial", 15, "bold"), bg="lightgreen", relief=RAISED)
        otp_lbl.place(x=10, y=125, height=40, width=310)
        self.otp_pw=Entry(f_pw_frame, font=("arial", 15), bg="lightblue", relief=RIDGE, bd=3, textvariable=self.enter_otp)
        self.otp_pw.place(x=325, y=125, height=40, width=150)

        b_fg_pw=Button(f_pw_frame, text="Submmit", cursor="hand2",bd=5, font=("arial", 15, "bold"), bg="light pink", command=self.checkField_FP)
        b_fg_pw.place(x=480, y=75, height=40, width="150")
        b_otp=Button(f_pw_frame, text="Enter", cursor="hand2",bd=5, font=("arial", 15, "bold"), bg="light pink", command=self.detail)
        b_otp.place(x=480, y=125, height=40, width="150")

########################################## latest book ##########################################################

        book_frame=LabelFrame(self.root, text="My Data", font=("arial", 25, "bold"), bg="peachpuff", relief=RIDGE, bd=3)
        book_frame.place(x=700, y=65, height=620, width=640)

        scrol_x=Scrollbar(book_frame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        scrol_y=Scrollbar(book_frame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        self.b_grid=ttk.Treeview(book_frame, columns=("book_title", "dept", "subject", "quantity"), xscrollcommand=scrol_x.set, yscrollcommand=scrol_y.set)
        scrol_x.config(command=self.b_grid.xview)
        scrol_y.config(command=self.b_grid.yview)
        #self.b_grid.heading("book_id", text="ID")
        self.b_grid.heading("book_title", text="Book Name")
        self.b_grid.heading("dept", text="Department")
        self.b_grid.heading("subject", text="Subject")
        self.b_grid.heading("quantity", text="Quantity")
        self.b_grid["show"]="headings"
        #self.b_grid.column("book_id", width=150, anchor=CENTER)
        self.b_grid.column("book_title", width=450, anchor=CENTER)
        self.b_grid.column("dept", width=100, anchor=CENTER)
        self.b_grid.column("subject", width=200, anchor=CENTER)
        self.b_grid.column("quantity", width=100, anchor=CENTER)

        self.b_grid.pack(fill=BOTH, expand=1)
        #self.fetchDataHome()

########################################## login varification ###################################################
########################################## featch data ##########################################################
    def featchData(self):
        con=sqlite3.connect(database=r"bookInventory.db")
        cur=con.cursor()
        cur.execute("select book_title, dept, subject, quantity from bookRecordInventory where email=?", (self.email.get(),))
        rows=cur.fetchall()
        #print("email====", row)
        try:
            if len(rows)==0:
                messagebox.showinfo("Item", "This is not available!!")
            elif len(rows)!=0:
                self.b_grid.delete(*self.b_grid.get_children())
                for row in rows:
                    self.b_grid.insert('', END, values=row)
                con.commit()
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
    
    def loginConnection(self):
        con=sqlite3.connect(database=r"bookInventory.db")
        cur=con.cursor()
        cur.execute("select * from inventory where email=? and password=?",(self.email.get(), self.login_password.get()))
        self.row=cur.fetchone()
    
    def db(self):
        if self.email.get()=="" or self.login_password.get()=="":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                self.loginConnection()
                if self.row==None:
                    messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
                else:
                    self.otpGenerator()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)     

    def checkField_FP(self):
        global x                #this x is used in change pw automatically
        x=self.email_forget.get()
        if self.email_forget.get()=="" or self.contact_no.get()=="":
            messagebox.showerror("Error", "Email and Mobile no. are required!!", parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r"bookInventory.db")
                cur=con.cursor()
                cur.execute("select *from inventory where email=? and contact_no=?", (self.email_forget.get(), self.contact_no.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", f"Its not registered email or contact no!!", parent=self.root)
                else:
                    self.otpGenerator()
            except Exception as es:
                messagebox.showerror("Error", f"Error due to:{str(es)}", parent=self.root)

    def checkFieldLogin(self):
        try:
            if self.email.get()=="" or self.login_password.get()=="":
                messagebox.showerror("Error","All fields are required!!")
            else:
                self.loginConnection()
                if self.row==None:
                    messagebox.showerror("Error", f"Its not registered email or password!!", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Welcome", parent=self.root)
                    self.featchData()
                    self.clear()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)   

    def otpGenerator(self):
        with open('key.txt', 'r') as rf:
            base_32_key=rf.read()
            timeBaseOtp=pyotp.TOTP(base_32_key)
            self.current_otp=timeBaseOtp.now() #>>>>>>>>>>>>>>>>>>>>>>
        print(self.current_otp)
        account_sid = 'ACb509e047f98cc097f88ae09e61eb0717'
        auth_token = '148e9735f4e5fbe8b16bd17461f9b15c'
        client=Client(account_sid, auth_token)
        # self.client_no=input("Enter Mobile no. : ")
        # self.country_code='+91'
        # self.no=self.country_code+self.client_no
        message=client.messages.create(
            body=f"OTP {self.current_otp} for reset your password!!",
            from_='+16066719892',
            #to=self.no
            to='+919015028276'
        )
        messagebox.showinfo("OTP", "OTP send on your registered number!!!", parent=self.root)

    def verification_otp(self,time_interval, enter_otp):
        if enter_otp=="":
            messagebox.showerror("Error", "Enter OTP!!", parent=self.root)
        elif (time_interval)<30 and (enter_otp==self.current_otp):
            if self.otp_DB.get()==self.current_otp:
                messagebox.showinfo("Connect", "For Future Use!!!")
                self.clear()
            else:
                print("Successfully")
                self.clear()
                self.changePassword()
            return
        elif (time_interval)<30 and (enter_otp != self.current_otp):
            messagebox.showerror("Error", "OTP is not correct!!", parent=self.root)
        elif (time_interval)>=30:
            messagebox.showinfo("Time out", "Please try again, Time Out!!", parent=self.root)

    def detail(self):
        while True:
            start=dt()
            end=dt()
            time_interval=end-start
            if self.otp_DB.get() !="":
                self.verification_otp(time_interval, self.otp_DB.get())
            else:
                self.verification_otp(time_interval, self.enter_otp.get())
            break

    def changePassword(self):
        self.new_window=Toplevel(self.root)
        self.new_window.title("Change Password")
        self.new_window.geometry("650x250+20+435")
        
        self.con=sqlite3.connect(database=r"bookInventory.db")
        self.cur=self.con.cursor()
        self.cur.execute("select email from inventory")
        row=self.cur.fetchone()
        lab=Label(self.new_window, text=x, font=("arial", 15, "bold"), bg="lightblue", bd=3, relief=RIDGE) #forget pw email automatically update here
        lab.place(x=20, y=10, height=40, width=600)
        new_pw_lbl=Label(self.new_window, text="New Password", font=("arial", 15, "bold"), bd=3, bg="lightblue", relief=RIDGE)
        new_pw_lbl.place(x=20, y=60, height=40, width=210)
        self.new_pw=Entry(self.new_window, show="*", bd=3, bg="aquamarine", relief=RIDGE, textvariable=self.pw_forget)
        self.new_pw.place(x=230, y=60, height=40, width=390)
        confirm_pw_lbl=Label(self.new_window, text="Confirm Password", font=("arial", 15, "bold"), bd=3, bg="lightblue", relief=RIDGE)
        confirm_pw_lbl.place(x=20, y=110, height=40, width=210)
        self.confirm_pw=Entry(self.new_window, show="*", bd=3, bg="aquamarine", relief=RIDGE)
        self.confirm_pw.place(x=230, y=110, height=40, width=390)

        pw_chng=Button(self.new_window, text="Update Password", cursor="hand2", font=("arial", 15, "bold"), bg="light pink", command=self.updatePassword)
        pw_chng.place(x=20, y=160, height=40, width="210")

    def updatePassword(self):
        try:
            if self.pw_forget.get()=="":
                messagebox.showerror("Error", "Filled can not be blank!!")
            
            elif self.pw_forget.get() != self.confirm_pw.get():
                messagebox.showerror("Error", "Both field is not same!!!")
            else:
                self.cur.execute("update inventory set password=? where email=?", (
                        self.pw_forget.get(), self.email_ent.get()
                    ))
                self.con.commit()
                messagebox.showinfo("Success", "Password has been Updated!!")
                self.con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        self.clear()
            
    def clear(self):
        self.email.set("")
        self.email_forget.set("")
        self.login_password.set("")
        self.pw_forget.set("")
        self.C_password.set("")
        self.otp_db_ent.set("")
        self.enter_otp.set("")
        self.contact_no.set("")

if __name__=="__main__":
    root=Tk()
    ob=LoginPage(root)
    root.mainloop()

    