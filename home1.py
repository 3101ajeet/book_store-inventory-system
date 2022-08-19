from select import select
from tkinter import*
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from registration_page import Book
from login_forget_pw import LoginPage
from api_fatch_data import BookTypes

class Home:
    def __init__(self, root):
        self.root=root
        self.root.title("Inventory Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="peachpuff")

        self.search_txt=StringVar()
        self.searchDept=StringVar()

        lbl_title=Label(self.root, text="Home Page", relief=SUNKEN, font=("arial", 20, "bold"), fg="green", bg="lightyellow", bd=10)
        lbl_title.pack(side=TOP, fill=X)

        frm=Frame(self.root, bd=5, bg="aliceblue", relief=GROOVE, background="paleturquoise")
        frm.place(x=0, y=55, height=640,width=400)

        self.ttl_lbl=Label(frm, text="No. of Books : [0]", font=("arial", 20, "bold"), bd=3, bg="greenyellow", relief=SUNKEN)
        self.ttl_lbl.place(x=0, y=0, height=80, width=390)
        self.ttl_typ=Label(frm, text="No. of Subject : [0]", font=("arial", 20, "bold"), bd=3, bg="greenyellow", relief=SUNKEN)
        self.ttl_typ.place(x=0, y=80, height=80, width=390)

        page_lbl_frm=LabelFrame(frm, text="Page", font=("arial", 20, "bold"), bg="paleturquoise")
        page_lbl_frm.place(x=0, y=180, height=190, width=390)
        btn_reg=Button(page_lbl_frm, text="Registration", font=("arial", 20, "bold"), bd=5, cursor="hand2", relief=GROOVE, bg="seagreen", command=self.registration)
        btn_reg.place(x=0,y=0, height=50, width=390)
        btn_login=Button(page_lbl_frm, text="LogIn", font=("arial", 20, "bold"), bd=5, cursor="hand2", relief=GROOVE, bg="seagreen", command=self.login)
        btn_login.place(x=0,y=50, height=50, width=390)
        btn_api=Button(page_lbl_frm, text="Data Entry", font=("arial", 20, "bold"), bd=5, cursor="hand2", relief=GROOVE, bg="seagreen", command=self.bookEntryType)
        btn_api.place(x=0,y=100, height=50, width=390)

        d_lbl_frm=LabelFrame(frm, text="Filter", font=("arial", 20, "bold"), bg="paleturquoise")
        d_lbl_frm.place(x=0, y=400, height=200, width=390)
        d_lbl=Label(d_lbl_frm, text="Book Department", font=("arial", 15, "bold"), bg="light pink", relief=GROOVE)
        d_lbl.place(x=2, y=10, height=50, width=170)
        self.combo_search=ttk.Combobox(d_lbl_frm, width=12, textvariable=self.searchDept, font=("arial", 15, "bold"), justify=CENTER, state="readonly", background="blue")
        self.combo_search["value"]=("IT", "DataBase", "Other")
        self.combo_search.place(x=172, y=10, height=50, width=210)
        # d_lbl_sub=Label(d_lbl_frm, text="Subject", font=("arial", 15, "bold"), bg="light pink", relief=GROOVE)
        # d_lbl_sub.place(x=2, y=60, height=40, width=170)
        # # self.txt_search=Entry(d_lbl_frm, font=("arial", 15, "bold"), textvariable=self.search_txt, width=15, bd=5, relief=GROOVE)
        # # self.txt_search.place(x=172, y=60, height=40, width=210)
        # sub_search=Entry(d_lbl_frm, font=("arial", 15), textvariable=self.search_txt, bd=3)
        # sub_search.place(x=172, y=60, height=40, width=210)
        
        btn_search=Button(d_lbl_frm, font=("arial", 20, "bold"), width=10,cursor="hand2", text="Search", bd=5, bg="seagreen", command=self.search)
        btn_search.place(x=2, y=80, height=50, width=185)
        btn_clr=Button(d_lbl_frm, font=("arial", 20, "bold"), width=10,cursor="hand2", text="Clear", bd=5, bg="seagreen", command=self.clear)
        btn_clr.place(x=193, y=80, height=50, width=185)

        all_bk_frm=Frame(self.root, bd=5, bg="aliceblue", relief=GROOVE, background="paleturquoise")
        all_bk_frm.place(x=435, y=55, height=640,width=910)
        
        ########################################## tree view ##########################################

        scrol_x=Scrollbar(all_bk_frm, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        scrol_y=Scrollbar(all_bk_frm, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        self.b_grid=ttk.Treeview(all_bk_frm, columns=("book_title", "dept", "subject"), xscrollcommand=scrol_x.set, yscrollcommand=scrol_y.set)
        scrol_x.config(command=self.b_grid.xview)
        scrol_y.config(command=self.b_grid.yview)
        #self.b_grid.heading("book_id", text="ID")
        self.b_grid.heading("book_title", text="Book Name")
        self.b_grid.heading("dept", text="Department")
        self.b_grid.heading("subject", text="Subject")
        self.b_grid["show"]="headings"
        #self.b_grid.column("book_id", width=150, anchor=CENTER)
        self.b_grid.column("book_title", width=450, anchor=CENTER)
        self.b_grid.column("dept", width=100, anchor=CENTER)
        self.b_grid.column("subject", width=200, anchor=CENTER)

        self.b_grid.pack(fill=BOTH, expand=1)
        self.fetchDataHome()

    def clear(self):
        self.combo_search.set("")
        self.sub.set("")
        self.fetchDataHome()

    def search(self):
        con=sqlite3.connect(database=r"bookInventory.db")
        cur=con.cursor()
        cur.execute("select book_title, dept, subject from bookRecordInventory where dept=? or subject=?",(self.searchDept.get(), self.search_txt.get().capitalize()))
        rows=cur.fetchall()
        print("rows<<<<>>>>>", rows)
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
    def fetchDataHome(self):
        con=sqlite3.connect(database=r"bookInventory.db")
        cur=con.cursor()
        cur.execute("select book_title, dept, subject from bookRecordInventory")
        rows=cur.fetchall()
        t=[]
        #print("list=====", rows)
        for i in rows:
            t.append(i[1])
        x=len(set(t))
        #print("x========", x)
        self.ttl_lbl.config(text=f'No. of Books : {str(len(rows))}')
        self.ttl_typ.config(text=f'No. of Subjects : {str(x)}')
        if len(rows) != 0:
            self.b_grid.delete(*self.b_grid.get_children())
            for row in rows:
                self.b_grid.insert('', END, values=row)
            con.commit()
        #print("chk data==========", type(rows))
            return 
        con.close()

    def registration(self):
        self.reg_window=Toplevel(self.root)
        self.reg_obj=Book(self.reg_window)

    def login(self):
        self.login_window=Toplevel(self.root)
        self.login_obj=LoginPage(self.login_window)

    def bookEntryType(self):
        self.entry_window=Toplevel(self.root)
        self.entry_obj=BookTypes(self.entry_window)

if __name__=="__main__":
    root=Tk()
    ob=Home(root)
    root.mainloop()

    