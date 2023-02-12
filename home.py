#mw->main window aw->add window f1->add widow f2->withraw add f3->add view f4->withdraw view  f5,6->add,withdraw update f7,8->add,withdraw delete
#save->will save emp data

from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

root=Tk()
root.title("E.M.S")
root.geometry("600x700+50+50")
root.configure(bg='lightgreen')
f=("Simsun",25,"bold")

def f1():
	root.withdraw()
	aw.deiconify()

def f2():
	aw.withdraw()
	root.deiconify()

def f3():
	root.withdraw()
	vw.deiconify()
	vw_em_data.delete(1.0,END)
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="select * from emp order by emp_id"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info+"id = "+str(d[0])+"  "+"name = "+str(d[1])+"  "+"salary = "+str(d[2])+"\n"+("*"*10)+"\n"
		vw_em_data.insert(INSERT,info)
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()

def f4():
	vw.withdraw()
	root.deiconify()
def f5():
	root.withdraw()
	uw.deiconify()

def f6():
	uw.withdraw()
	root.deiconify()
def f7():
	root.withdraw()
	dw.deiconify()

def f8():
	dw.withdraw()
	root.deiconify()

def save():
    con = None
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql = "insert into emp values('%d','%s','%d')"
        id = int(aw_ent_id.get())
        name = aw_ent_name.get()
        salary = int(aw_ent_salary.get())
        try:
            cursor.execute(sql % (id, name, salary))
            con.commit()
            showinfo("Success", "Record created")
        except IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                showerror("Error", "ID already exists")
            else:
                showerror("Error", e)
    except Exception as e:
        con.rollback()
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()
        aw_ent_id.delete(0, END)
        aw_ent_name.delete(0, END)
        aw_ent_salary.delete(0, END)
        aw_ent_id.focus()


def saveupdate():
	con=None
	try:
		
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "update emp set name=?, salary=? where emp_id=?"
		id = uw_ent_id.get()
		name = uw_ent_name.get()
		salary = uw_ent_salary.get()
		cursor.execute(sql, (name, salary, id))
		con.commit()
		showinfo("Success", "record updated")

	except Exception as e:
		con.rollback()
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
		uw_ent_id.delete(0,END)
		uw_ent_name.delete(0,END)
		uw_ent_salary.delete(0,END)
		uw_ent_id.focus()
	

def delete():
    con = None
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        id1 = int(dw_ent_id.get())
        cursor.execute("SELECT * FROM emp WHERE emp_id=?", (id1,))
        record = cursor.fetchone()
        if record:
            cursor.execute("DELETE FROM emp WHERE emp_id=?", (id1,))
            con.commit()
            showinfo("Success", "Record deleted")
        else:
            showerror("Error", "id does not exist's")
    except Exception as e:
        con.rollback()
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()
        dw_ent_id.delete(0, END)
        dw_ent_id.focus()





def f9():
	con=connect("ems.db")
	cursor=con.cursor()
	da=pd.read_sql("select * from emp order by salary desc limit 5",con)
	da.to_csv('data.csv',index=	False)
	id=da["emp_id"]
	x=da["name"]
	y=da["salary"]
	plt.bar(x, y, label='Employee data', color='red')
	plt.xlabel('Employee names')
	plt.ylabel('Employee salaries')
	plt.title('Employee data')
	plt.legend()
	plt.show()
	

mw_btn_add=Button(root,text="Add",font=f,width=15,command=f1)
mw_btn_add.place(x=130,y=15)
mw_btn_view=Button(root,text="View",font=f,width=15,command=f3)
mw_btn_view.place(x=130,y=100)
mw_btn_update=Button(root,text="Update",font=f,width=15,command=f5)
mw_btn_update.place(x=130,y=200)
mw_btn_delete=Button(root,text="Delete",font=f,width=15,command=f7)
mw_btn_delete.place(x=130,y=300)
mw_btn_charts=Button(root,text="Charts",font=f,width=15,command=f9)
mw_btn_charts.place(x=130,y=400)
try:
	wa="https://ipinfo.io/"
	res=requests.get(wa)
	#print(res)
	data=res.json()
	#print(data)
	city_name=data["city"]
		
	a1="https://api.openweathermap.org/data/2.5/weather"
	a2="?q="+city_name
	a3="&appid="+"d4394a022c5ee94741570c6f8f6c37dd"
	a4="&units="+"metric"
	wa1=a1+a2+a3+a4
	res1=requests.get(wa1)
	#print(res)
	data1=res1.json()
	#print(data1)
	temp=data1["main"]["temp"]
	
	
	mw_lab_loc=Label(root,text="Location :"+city_name,borderwidth=1,relief="solid",font=f,bg="lightgreen")
	mw_lab_loc.place(x=15,y=500)
	mw_lab_loc=Label(root,text="Temp :"+str(temp),borderwidth=1,relief="solid",font=f,bg="lightgreen")
	mw_lab_loc.place(x=15,y=600)

except Exception as e:
	print("issue",e)





aw=Toplevel(root)
aw.title("Add Emp")
aw.geometry("600x700+50+50")
aw_lab_id=Label(aw,text="enter id:",font=f,bg="lightblue")
aw_lab_id.pack(pady=20)
aw_ent_id=Entry(aw,font=f)
aw_ent_id.pack(pady=10)
aw_lab_name=Label(aw,text="enter name:",font=f,bg="lightblue")
aw_lab_name.pack(pady=20)
aw_ent_name=Entry(aw,font=f)
aw_ent_name.pack(pady=10)
aw_lab_salary=Label(aw,text="enter salary:",font=f,bg="lightblue")
aw_lab_salary.pack(pady=20)
aw_ent_salary=Entry(aw,font=f)
aw_ent_salary.pack(pady=10)

aw_btn_save=Button(aw,text="Save",font=f,command=save)
aw_btn_Back=Button(aw,text="Back",font=f,command=f2)
aw_btn_save.pack(pady=10)
aw_btn_Back.pack(pady=10)
aw.configure(bg="lightblue")
aw.withdraw()


vw=Toplevel(root)
vw.title("View emp")
vw.geometry("600x700+50+50")
vw_em_data=ScrolledText(vw,font=18,width=50,height=8)
vw_em_data.pack(pady=20)
vw_btn_back=Button(vw,text="Back",font=f,command=f4)
vw_btn_back.pack(pady=20)
vw.configure(bg="lightpink")
vw.withdraw()

uw=Toplevel(root)
uw.title("Update Emp")
uw.geometry("600x700+50+50")
uw_lab_id=Label(uw,text="enter id:",font=f,bg="orchid1")
uw_lab_id.pack(pady=20)
uw_ent_id=Entry(uw,font=f)
uw_ent_id.pack(pady=10)
uw_lab_name=Label(uw,text="enter name:",font=f,bg="orchid1")
uw_lab_name.pack(pady=20)
uw_ent_name=Entry(uw,font=f)
uw_ent_name.pack(pady=10)
uw_lab_salary=Label(uw,text="enter salary:",font=f,bg="orchid1")
uw_lab_salary.pack(pady=20)
uw_ent_salary=Entry(uw,font=f)
uw_ent_salary.pack(pady=10)

uw_btn_save=Button(uw,text="Save",font=f,command=saveupdate)
uw_btn_Back=Button(uw,text="Back",font=f,command=f6)
uw_btn_save.pack(pady=10)
uw_btn_Back.pack(pady=10)
uw.configure(bg="orchid1")

uw.withdraw()

dw=Toplevel(root)
dw.title("Delete Emp")
dw.geometry("600x700+50+50")
dw_lab_id=Label(dw,text="enter id:",font=f,bg="blue")
dw_ent_id=Entry(dw,font=f)
dw_lab_id.pack(pady=20)
dw_ent_id.pack(pady=20)
dw_btn_save=Button(dw,text="Save",font=f,command=delete)
dw_btn_Back=Button(dw,text="Back",font=f,command=f8)
dw_btn_save.pack(pady=10)
dw_btn_Back.pack(pady=10)
dw.configure(bg="blue")

dw.withdraw()

		


root.mainloop()
