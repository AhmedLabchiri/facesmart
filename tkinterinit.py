import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
import util
from PIL import Image, ImageTk
import mysql.connector
from tkinter import PhotoImage
from tkinter import ttk
class DatabaseHandler:
    def __init__(self, host, user, passwd, database):
        self.connection = mysql.connector.connect(
            host = host,
            user = user,
            passwd=passwd,
            database=database
        )
        self.cursor = self.connection.cursor()

    def queryExec(self,query,params=None):
        self.cursor.execute(query,params)
        return self.cursor.fetchall()
    def commit(self):
        self.connection.commit()
    def closeConnection(self):
        self.cursor.close()
        self.connection.close()

class App:
    def __init__(self, db):

        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.title("Main Window")
        self.main_window.iconbitmap(r'../icons/face_detect.ico')
        self.imgpath= PhotoImage(file=r"C:\Ahmed Space\updated\facesmart\bg.png")
        self.backimage = tk.Label(self.main_window, image=self.imgpath)
        self.backimage.place(relheight=1, relwidth=1)
        self.entryTextP = util.get_entry_text(self.main_window)
        self.entryTextP.place(x=800, y=150)
        """!!!!!!!"""


        self.textforusername = util.get_text_label(self.main_window, "Please input password \n(for admin only)")
        self.textforusername.place(x=800, y=75)
        self.login_butt_main = util.get_button(self.main_window,"Log In","#BC2023",self.login,)
        self.login_butt_main.place(x=830,y=300)
        self.register_butt_main = util.get_button(self.main_window, "Register", "#255000" , self.register, )
        self.register_butt_main.place(x=830, y=400)
        self.webcam=util.get_img_label(self.main_window)
        self.webcam.place(x=10,y=0, width=700, height=500)
        self.faceweb(self.webcam)
        self.db_dir = "../facestoload"


        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.db = db
        "#Init"
        self.imagesList = []
        self.namesList = []
        self.lName = os.listdir(self.db_dir)
        for self.lN in self.lName:
            self.curImg = cv2.imread(f'{self.db_dir}/{self.lN}')
            self.imagesList.append(self.curImg)
            self.namesList.append(os.path.splitext(self.lN)[0])




    def faceweb(self, label):
        if "cap" not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.place_webcam()

    def imageEncoding(self):
        self.encodeList = []
        for self.img in self.imagesList:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.faceEncode = face_recognition.face_encodings(self.img)[0]
            self.encodeList.append(self.faceEncode)
        return self.encodeList
    def place_webcam(self):
        success, frame = self.cap.read()
        self.recent_cap = frame
        img = cv2.cvtColor(self.recent_cap,cv2.COLOR_BGR2RGB)
        self.recent_cap_pil = Image.fromarray(img)
        imgTk = ImageTk.PhotoImage(image=self.recent_cap_pil)
        self._label.imgtk = imgTk
        self._label.configure(image=imgTk)
        self._label.after(20, self.place_webcam)

        self.imgSize = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        self.imgSize = cv2.cvtColor(self.imgSize, cv2.COLOR_BGR2RGB)





    def start(self):
        self.main_window.mainloop()

    def ret_task(self):
        query = """SELECT task FROM users where username = %s"""
        result = self.db.queryExec(query,(self.name,))
        return result
    def login(self):
        self.pwd = self.entryTextP.get(1.0, "end-1c")
        print("Here is the password,",self.pwd)
        if self.pwd == "ADMIN123":
            self.login_dashboard()
        else:
            self.facesInFrame = face_recognition.face_locations(self.imgSize)
            self.encodeInFrame = face_recognition.face_encodings(self.imgSize, self.facesInFrame)
            self.KnownFaces = self.imageEncoding()

            '#compare capture to known faces in the system'
            for self.encodeFace, self.faceLoc in zip(self.encodeInFrame, self.facesInFrame):
                self.faceMatches = face_recognition.compare_faces(self.KnownFaces, self.encodeFace)
                self.faceDis = face_recognition.face_distance(self.KnownFaces, self.encodeFace)
                self.matchI = np.argmin(self.faceDis)

                if self.faceMatches[self.matchI]:
                    self.name = self.namesList[self.matchI].upper()
                    self.markAttendance()
                    y1, x2, y2, x1 = self.faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(self.recent_cap, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    cv2.rectangle(self.recent_cap, (x1, y2 - 30), (x2, y2), (255, 0, 255), cv2.FILLED)
                    cv2.putText(self.recent_cap, self.name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 2)

                    if self.name == "ADMIN":
                        print(self.pwd)
                        self.login_dashboard()
                    else:
                        task = self.ret_task()
                        str_task = str(task[1])
                        util.msg_box("Login Success!", "Attendance Marked! Welcome back, " + self.name + " Task : " + str_task )


                else:
                    util.msg_box("Login Failed!", "We couldn't capture or identify you, please try again or register")


    def markAttendance(self):
        with open('../attendance.csv', 'r+') as f:
            self.DataList = f.readlines()
            self.names = []
            for line in self.DataList:
                entry = line.split(',')
                self.names.append(entry[0])
                self.now = datetime.now()
                self.dtimes = self.now.strftime('%H:%M:%S')
                f.writelines(f'\n{self.name},{self.dtimes}')
                break


    def register(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.geometry("1200x520+370+120")
        self.register_window.title("Register")
        self.register_window.iconbitmap(r'../icons/face_detect.ico')
        self.backimager = tk.Label(self.register_window, image=self.imgpath)
        self.backimager.place(relheight=1, relwidth=1)
        #entry and others
        '''self.entryText = util.get_entry_text(self.register_window)
        self.entryText.place(x=750,y=150)

        self.textforusername = util.get_text_label(self.register_window, "Please input username")
        self.textforusername.place(x=750,y=70)'''

        self.textforusername = util.create_form_label(self.register_window, "Full Name:")
        self.textforusername.place(x="715", y="10")
        self.entryText = util.get_entry_del(self.register_window)
        self.entryText.place(x="825", y="10")
        #Accept Button
        self.dropdown_create(x=715,y=45,x2=845,y2=45,window= self.register_window)
        self.yearReg = util.create_form_label(self.register_window, "Year of Registration:")
        self.yearReg.place(x="715", y="75")
        self.yearReg_entry = util.get_entry_create(self.register_window)
        self.yearReg_entry.place(x="905", y="75")

        self.name_butt = util.get_button(self.register_window, "Accept", "#255000", self.accept_register, )
        self.name_butt.place(x=800, y=300)

        #Try Again Button
        self.confirm_butt_main = util.get_button(self.register_window, "Try Again", "#BC2023", self.retry_register, )
        self.confirm_butt_main.place(x=800, y=400)
        #the screenshot from cv2
        self.sc = util.get_img_label(self.register_window)
        self.sc.place(x=10, y=0, width=700, height=500)
        self.addsc(self.sc)

    def addsc (self,label):
        imgTk = ImageTk.PhotoImage(image=self.recent_cap_pil)
        label.imgtk = imgTk
        label.configure(image=imgTk)
        self.register_cap = self.recent_cap.copy()
    def insert_query(self,var,query):
        print("insert query function entered")
        self.db.queryExec(query, var)
        self.db.commit()

    def accept_register(self):
        self.nameToUse = self.entryText.get(1.0, "end-1c")
        self.YearToUse = self.yearReg_entry.get(1.0, "end-1c")
        self.taskToUse = "Not Defined"
        if self.nameToUse == "ADMIN":
            util.msg_box("Privilege Error!","You can't register as an Admin, please use your real name instead.")
            self.register_window.destroy()
        else:
            print(self.nameToUse)
            cv2.imwrite(os.path.join(self.db_dir, "{}.jpg".format(self.nameToUse)), self.register_cap)
            util.msg_box("Success!", "User was registered succesfully")
            var = (self.nameToUse,self.selected_item_create,self.YearToUse,self.taskToUse)
            query = """INSERT INTO users(username,major,yearr,task) VALUES(%s,%s,%s,%s)"""
            self.insert_query(var,query)
            self.register_window.destroy()
            """query ='''INSERT INTO users(username) VALUES(%s)'''
            
            self.db.queryExec(query,var)
            self.db.commit()
            self.register_window.destroy()"""

    def retry_register(self):
        self.register_window.destroy()
    def login_dashboard(self):
        print("Entered")

        self.dashboard_window= tk.Toplevel(self.main_window)
        self.dashboard_window.geometry("1200x520+370+120")
        self.backimage = tk.Label(self.dashboard_window, image=self.imgpath)
        self.backimage.place(relheight=1, relwidth=1)
        self.dashboard_window.title("Dashboard")
        self.dashboard_window.iconbitmap(r'../icons/face_detect.ico')
        self.backimage1 = tk.Label(self.dashboard_window, image=self.imgpath)
        self.create_butt = util.get_button_CRUD(self.dashboard_window,"Create","#255000",self.create_CRUD)
        self.create_butt.place(x="40",y="20")
        self.read_butt = util.get_button_CRUD(self.dashboard_window, "Read", "#588100", self.read_CRUD)
        self.read_butt.place(x="40", y="90")
        self.update_butt = util.get_button_CRUD(self.dashboard_window, "Update", "#8db600", self.update_CRUD)
        self.update_butt.place(x="40", y="160")
        self.delete_butt = util.get_button_CRUD(self.dashboard_window, "Delete", "#BC2023", self.delete_CRUD)
        self.delete_butt.place(x="40", y="230")

    def create_CRUD(self):
        self.dashboard_window.destroy()
        self.login_dashboard()
        """Create"""
        self.createform = util.create_form_label(self.dashboard_window, "Enter the full name of the user")
        self.createform.place(x="220", y="10")
        self.creatEntry_name = util.get_entry_del(self.dashboard_window)
        self.creatEntry_name.place(x="530", y="10")

        """Departement"""
        self.dropdown_create(x=220,y=50,x2=530,y2=50,window=self.dashboard_window)


        """Year of registering to the institution"""
        self.creatReg = util.create_form_label(self.dashboard_window, "Enter the year of registration")
        self.creatReg.place(x="220", y="100")
        self.creatReg_entry = util.get_entry_create(self.dashboard_window)
        self.creatReg_entry.place(x="530", y="90")

        self.creatask = util.create_form_label(self.dashboard_window, "Enter the task")
        self.creatask.place(x="220", y="140")
        self.creatask_entry = util.get_entry_create(self.dashboard_window)
        self.creatask_entry.place(x="530", y="140")

        self.tsc_butt = util.get_button(self.dashboard_window, "Take Shot of User", "#BC2023", self.create_camera, )
        self.tsc_butt.place(x="900", y="340")




        """"""

    def confirm_create(self):



        self.EntryYear = self.creatReg_entry.get(1.0, "end-1c")
        self.EntryTask = self.creatask_entry.get(1.0,"end-1c")
        #print("hey", self.EntryDepartment, self.selected_item_create, self.EntryName)
        queryy = """INSERT INTO users(username, major, yearr,task) VALUES(%s,%s,%s,%s)"""
        varr = (self.EntryName, self.selected_item_create, self.EntryYear,self.EntryTask)
        self.insert_query(varr, queryy)
    def create_camera(self):
        self.EntryName = self.creatEntry_name.get(1.0, "end-1c")
        print("Here is the entry name:", self.EntryName)
        self.accept_butt = util.get_button(self.dashboard_window, "Accept", "green", self.confirm_create, )
        self.accept_butt.place(x="900", y="250")
        self.sc = util.get_img_label(self.dashboard_window)
        self.sc.place(x=220, y=160, width=550, height=250)
        self.addsc(self.sc)
        cv2.imwrite(os.path.join(self.db_dir, "{}.jpg".format(self.EntryName)), self.register_cap)
    def read_query(self,):
        print("read query function entered")
        queryy = """SELECT * FROM users WHERE major = %s"""
        rows = self.db.queryExec(queryy,(self.selected_item,))
        return rows
    def readD_query(self,):
        print("read query function entered")
        queryy = """SELECT * FROM users"""
        rows = self.db.queryExec(queryy ,)
        return rows
    def on_select(self,event):
        self.selected_item = self.optionchoosen.get()
        print("Selected Item:", self.selected_item)
        x = 230
        y = 70
        if self.selected_item == ' Software Engineer':
            self.table_read = util.tree_read(self.dashboard_window,x,y,self.read_query())
        elif self.selected_item == ' MBA':
            self.table_read = util.tree_read(self.dashboard_window, x, y, self.read_query())
        elif self.selected_item == ' Computer Science':
            self.table_read = util.tree_read(self.dashboard_window, x, y, self.read_query())
        elif self.selected_item == ' Applied Mathematics':
            self.table_read = util.tree_read(self.dashboard_window, x, y, self.read_query())

    def on_select_create(self,event):
        self.selected_item_create = self.optionchoosen_create.get()
    def dropdown(self):
        self.labelfordropdown = ttk.Label(self.dashboard_window, text="Filter by major:", font=("Helvetica bold", 15))
        self.labelfordropdown.place(x="230", y="30")
        n = tk.StringVar()
        self.optionchoosen = ttk.Combobox(self.dashboard_window, width=27,
                                     textvariable=n)
        self.optionchoosen['values'] = (' Software Engineer',
                                   ' MBA',
                                   ' Computer Science',
                                   ' Applied Mathematics'
                                   )

        self.optionchoosen.grid(column=1, row=15)
        self.optionchoosen.place(x="390", y="35")
        self.optionchoosen.bind("<<ComboboxSelected>>", self.on_select)




    def dropdown_create(self,x,y,x2,y2,window):
        self.labelfordropdown_create = ttk.Label(window, text="Select Major", font=("Helvetica bold", 15))
        self.labelfordropdown_create.place(x=x,y=y)
        n = tk.StringVar()
        self.optionchoosen_create = ttk.Combobox(window, width=27,
                                          textvariable=n)
        self.optionchoosen_create['values'] = (' Software Engineer',
                                        ' MBA',
                                        ' Computer Science',
                                        ' Applied Mathematics'
                                        )
        self.optionchoosen_create.grid(column=1, row=15)
        self.optionchoosen_create.place(x=x2,y=y2)
        self.optionchoosen_create.bind("<<ComboboxSelected>>", self.on_select_create)

    def read_CRUD(self):
        self.dashboard_window.destroy()
        self.login_dashboard()
        self.dropdown()
    def update_queryR(self):

        query = """SELECT username,major,yearr,task FROM users WHERE userid=%s"""
        param = self.useridup_entry.get(1.0, "end-1c")
        rows = self.db.queryExec(query,(param,))
        for row in rows:
            print(row)
            self.unameup_entry.insert(tk.END, row[0])
            self.majorup_entry.insert(tk.END, row[1])
            self.yearup_entry.insert(tk.END, row[2])
            self.taskup_entry.insert(tk.END, row[3])
        self.conf_upd_butt = util.get_button(self.dashboard_window,"Update User","green",self.update_query)
        self.conf_upd_butt.place(x="220",y="370")
        print("Hola",self.majorup_entry.get(1.0,"end-1c"))

    def update_query(self):
        update_queryy = """UPDATE users 
                              SET username = %s, major = %s, yearr = %s, task = %s 
                              WHERE userid = %s"""

        # Define the parameters for the query
        P1 = self.unameup_entry.get(1.0,"end-1c")
        P2 =  self.majorup_entry.get(1.0,"end-1c")
        P3 = self.yearup_entry.get(1.0, "end-1c")
        P4 = self.taskup_entry.get(1.0,"end-1c")
        P5 =  self.useridup_entry.get(1.0, "end-1c")
        params = (P1,P2,P3 ,P4,P5)
        self.db.queryExec(update_queryy, params)
        self.db.commit()
    def update_CRUD(self):
        self.dashboard_window.destroy()
        self.login_dashboard()
        self.useridup = util.create_form_label(self.dashboard_window, "Enter the userid to update:")
        self.useridup.place(x="220", y="20")
        self.useridup_entry = util.get_entry_del(self.dashboard_window)
        self.useridup_entry.place(x="460", y="20")
        self.confirmup_butt = util.get_button(self.dashboard_window, "Fetch for user", "#BC2023", self.update_queryR, )
        self.confirmup_butt.place(x="500", y="370")

        self.unameup = util.create_form_label(self.dashboard_window, "Enter the new name:")
        self.unameup.place(x="220", y="60")
        self.unameup_entry = util.get_entry_del(self.dashboard_window)
        self.unameup_entry.place(x="460", y="60")

        self.majorup = util.create_form_label(self.dashboard_window, "Select the new major:")
        self.majorup.place(x="220", y="90")
        self.majorup_entry = util.get_entry_del(self.dashboard_window)
        self.majorup_entry.place(x="460", y="90")

        self.yearup = util.create_form_label(self.dashboard_window, "Enter the new task:")
        self.yearup.place(x="220", y="120")
        self.yearup_entry = util.get_entry_del(self.dashboard_window)
        self.yearup_entry.place(x="460", y="120")

        self.taskup = util.create_form_label(self.dashboard_window, "Enter the new year:")
        self.taskup.place(x="220", y="150")
        self.taskup_entry = util.get_entry_del(self.dashboard_window)
        self.taskup_entry.place(x="460", y="150")

    def on_select(self,event):
        self.selected_item = self.optionchoosen.get()
        print("Selected Item:", self.selected_item)
        x = 230
        y = 70
        if self.selected_item == ' Software Engineer':
            self.table_read = util.tree_read(self.dashboard_window,x,y,self.read_query())
        elif self.selected_item == ' MBA':
            self.table_read = util.tree_read(self.dashboard_window, x, y, self.read_query())
        elif self.selected_item == ' Computer Science':
            self.table_read = util.tree_read(self.dashboard_window, x, y, self.read_query())
        elif self.selected_item == ' Applied Mathematics':
            self.table_read = util.tree_read(self.dashboard_window, x, y, self.read_query())
    def delete_CRUD(self):
        self.dashboard_window.destroy()
        self.login_dashboard()
        self.DeleteUserId = util.create_form_label(self.dashboard_window, "Enter the id of the user to delete")
        self.DeleteUserId .place(x="220", y="20")
        self.EntryUserId = util.get_entry_del(self.dashboard_window)
        self.EntryUserId.place(x="530", y="20")
        self.cdelete = util.get_button_CRUD(self.dashboard_window, "Delete User", "red", self.delete_query, )
        self.cdelete.place(x="850", y="10")


        self.deletegrid = util.treed_read(self.dashboard_window, self.readD_query())

    def delete_query(self):
        self.deleteEntry = self.EntryUserId.get(1.0, "end-1c")
        print("Here is the delete entry,", self.deleteEntry)
        query = """DELETE FROM users WHERE userid = %s"""
        param = (self.deleteEntry,)
        self.db.queryExec(query , param)
        self.db.commit()
        self.dashboard_window.destroy()
        self.login_dashboard()
        self.delete_CRUD()




if __name__=="__main__":
    db = DatabaseHandler("localhost", "root", "password", "testdb")
    app=App(db)
    app.start()



