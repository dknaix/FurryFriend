from datetime import datetime
import sqlite3
import socket
import threading as t
import os
try:
    import pandas as pd
except:
    print("Pandas is not installed!!! trying to install pandas")
    os.system("pip3 install pandas")
    import pandas as pd

global ip,port
ip='192.168.0.106'
port=9999



def create_table(db_conn):
    print("[+] Creating New Table")
    c = db_conn.cursor()
    #For User_info
    try:
        c.execute('''CREATE TABLE User_info (
            Userid varchar(255) NOT NULL,
            Pass varchar(255) NOT NULL
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
    #For Contact_info
    try:
        c.execute('''CREATE TABLE Contact_info (
            datetime varchar(255) NOT NULL,
            name varchar(255) NOT NULL,
            email varchar(255) NOT NULL,
            message varchar(255) NOT NULL
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
    #For Volunteer_info
    try:
        c.execute('''CREATE TABLE Volunteer_info (
           datetime varchar(255) NOT NULL,
            name varchar(255) NOT NULL,
            email varchar(255) NOT NULL,
            contact int NOT NULL
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
    #For Pet_Shop
    try:
        c.execute('''CREATE TABLE Pet_shop (
            item_id int ,
            item_name varchar(255) NOT NULL,
            item_cost int NOT NULL,
            item_desc varchar(255) NOT NULL,
            catagory varchar(255) NOT NULL,
            item_img varchar(255) NOT NULL
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )

    #For Order Table
    try:
        c.execute('''CREATE TABLE Orders (
            datetime varchar(255) NOT NULL,
            uname varchar(255) NOT NULL,
            id_x_count varchar(255) NOT NULL,
            address varchar(255) NOT NULL,
            total int NOT NULL
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        


def chk_login(db_conn,login,password):
    c = db_conn.cursor()
    chk_login=r"SELECT ROWID from User_info  WHERE Userid='{}' and Pass='{}';".format(login,password)
    print(chk_login)
    try:
        c.execute(chk_login)
        db_conn.commit()
        reply=c.fetchall()
        print(reply)
        return reply
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return None

def add_user(db_conn,login,password):
    c = db_conn.cursor()
    temp_str=r"INSERT INTO User_info (Userid,Pass)VALUES (?,?)"
    data=(login,password) #sending data in tuple
    try:
        c.execute(temp_str,data)
        db_conn.commit()
        print("[+] New Entry Created")
        return "new_acc_success"
    except Exception as e:
        print("Error in DB-add new user ")
        print("[-] "+str(e) )
        return "err_creating_acc"


def admin_add_item(db_conn,item_name,item_catagory,item_cost,item_desc,item_img):
    c = db_conn.cursor()
    item_id=999
    temp_str=r"INSERT INTO Pet_shop (item_id,item_name,item_cost,item_desc,catagory,item_img)VALUES (?,?,?,?,?,?)"
    data=(item_id, item_name, item_cost, item_desc, item_catagory, item_img) #sending data in tuple
    try:
        c.execute(temp_str,data)
        db_conn.commit()
        print("[+] New Entry Created")
        #return "new_item_add_success"
    except Exception as e:
        print("Error in DB-add new user ")
        print("[-] "+str(e) )
        return "err_addmin_new_item"

    temp_str=r"SELECT ROWID from Pet_shop where item_id='999'"
    try:
        c.execute(temp_str)
        db_conn.commit()
        new_id=c.fetchall()
        new_id=new_id[0][0]
        print("New Id:"+str(new_id))
        
    except Exception as e:
        print("Error in DB-add new item's rowid ")
        print("[-] "+str(e) )



    temp_str=r"Update Pet_shop Set item_id='{}' where item_id='999';".format(new_id)
    try:
        c.execute(temp_str)
        db_conn.commit()
        print("New item_id set:")
        return "new_item_add_success"
        
    except Exception as e:
        print("Error in DB-item id last step ")
        print("[-] "+str(e) )
        



def admin_fetch_item(db_conn,catg="",item_id="",order=False):
    c = db_conn.cursor()

    if catg!="":temp_str=r"Select * from Pet_Shop Where catagory='{}'".format(catg)#for client

    elif item_id!="":temp_str=r"Select * from Pet_Shop Where Item_id='{}'".format(item_id)#for admin

    elif order==True:temp_str=r"SELECT * from Orders" #for admin
    
    else:temp_str=r"Select * from Pet_Shop"
    
    try:
        c.execute(temp_str)
        db_conn.commit()
        data=c.fetchall()
        return data
    except Exception as e:
        print("Error in DB-Fetch admin_item_list ")
        print("[-] "+str(e) )
        return "err_fetch_admin_item"

def admin_delete_item(db_conn,item_id):
    c = db_conn.cursor()
    temp_str=r"Delete from Pet_Shop where Item_id='{}'".format(item_id)
    
    try:
        c.execute(temp_str)
        db_conn.commit()
        return "admin_delete_item_sucess"
    except Exception as e:
        print("Error in DB-Delete admin_item_list ")
        print("[-] "+str(e) )
        return "admin_delete_item_err"



def contact_us_add(db_conn,name,email,message): #(admin)
    c = db_conn.cursor()
    today=str(datetime.now())
    temp_str=r"INSERT INTO Contact_info (datetime,name,email,message)VALUES (?,?,?,?)"
    data=(today,name,email,message) #sending data in tuple
    try:
        c.execute(temp_str,data)
        db_conn.commit()
        print("[+] New Contact_us entry Created")
        return "new_contactus_add_success"
    except Exception as e:
        print("Error in DB-add Contact us ")
        print("[-] "+str(e) )
        return "err_contactus_add"


def volunteer_add(db_conn,name,email,contact): #(admin)
    c = db_conn.cursor()
    today=str(datetime.now())
    temp_str=r"INSERT INTO Volunteer_info (datetime,name,email,contact)VALUES (?,?,?,?)"
    data=(today,name,email,contact) #sending data in tuple
    try:
        c.execute(temp_str,data)
        db_conn.commit()
        print("[+] New Volunteer entry Created")
        return "new_volunteer_add_success"
    except Exception as e:
        print("Error in DB-add Volunteer ")
        print("[-] "+str(e) )
        return "err_volunteer_add"

def common_fetch(db_conn,loc): #for contact n volunteer(admin)
    c = db_conn.cursor()
    temp_str=r"Select * from {}".format(loc)
    
    try:
        c.execute(temp_str)
        db_conn.commit()
        data=c.fetchall()
        return data
    except Exception as e:
        print("Error in DB-Fetch Common list of:"+str(loc))
        print("[-] "+str(e) )
        return "err_fetch_admin_common_data"


def add_post_order(db_conn,acc_name,itemxcount,address,total):
    today=str(datetime.now())
    c = db_conn.cursor()
    temp_str=r"INSERT INTO Orders (datetime,uname,id_x_count,address,total)VALUES (?,?,?,?,?)"
    data=(today,acc_name,itemxcount,address,total) #sending data in tuple
    try:
        c.execute(temp_str,data)
        db_conn.commit()
        print("[+] New Entry Created")
        return "new_order_success"
    except Exception as e:
        print("Error in DB-add Order ")
        print("[-] "+str(e) )
        return "err_placing_order"
    

#create_table()
#add_user("dk","mypass")
#chk_login("dk","mypass")

def listen(): #Main Thread
    db_conn = sqlite3.connect('furryfriend_db.db')
    create_table(db_conn)
    db_conn.close()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Trying to start server at ",ip,port)
        s.bind((ip,port))
    except OSError:
        print("Error binding, address already in use, exiting")
        exit()
    print("Bind Sucessfull!!!")
    s.listen(50)
    print("listener running......")
    while 1:
        conn, addr = s.accept()
        print("\nNew Connection at",addr)
        t.Thread(target=run,args=(conn,addr,)).start() 
        #runn_thread=int(t.activeCount())-2
        #print("Total threads:{}".format(runn_thread))


def run(conn,addr):
    db_conn = sqlite3.connect('furryfriend_db.db') #sql conn obj
    global temp_frame_store  # for tracking already named temp frames
    data_x=""
    print("Threaad run...")
    
    try:
        data = conn.recv(10000)
        try: # for catching Frame/text Decoding err
            data_x=data.decode("utf-8")
            data_x=str(data_x)
            print(data_x)
        except:
            print("[*]Data_x not found, raw_binstream data rcv")
        
        if "--login" in data_x:
            print("[*]Rcv php login req")
            temp=data_x.split("--")
            x=chk_login(db_conn,temp[0],temp[1])
            if x:
                print("Login Sucess")
                conn.send(b"login_success")
            else:conn.send(b"login_fail")
            

        elif "--new_acc" in data_x:
            print("[*]Recv php new acc req")
            temp=data_x.split("--")
            x=add_user(db_conn,temp[0],temp[1])
            if x=="new_acc_success":conn.send(b"new_acc_success")
            else:conn.send(b"err_creating_acc")

        elif "--new_item" in data_x:
            print("[*]Recv php new item_add req")
            temp=data_x.split("--")
            
            x=admin_add_item(db_conn,temp[0],temp[1],temp[2],temp[3],temp[4])
            if x=="new_item_add_success":conn.send(b"new item add ez")
            else:conn.send(b"err_adding_item")

        elif "--get_admin_item_list" in data_x:
            print("[*]Recv php new fetch admin_item req")
            temp=data_x.split("--")
            x=admin_fetch_item(db_conn) #[(1,2),(3,4)]

            if x=="err_fetch_admin_item":conn.send(b"err_fetch_admin_item") # if err 
            else: #processing op
                temp_holder=[]
                for data0 in x:
                    for data1 in data0:
                        temp_holder.append(str(data1)) #["1","2","3","4"]
                temp_holder2=""
                for data in temp_holder:
                    temp_holder2=temp_holder2+data+"--"
                temp_holder2=temp_holder2[:-2]
                #print(temp_holder2) # "1--2--3--4"
                temp_holder2=bytes(temp_holder2,'utf-8')
                conn.send(temp_holder2)
                
        elif "--delete_admin_item" in data_x:
            print("[*]Recv php new admin_delete_item req")
            temp=data_x.split("--")
            x=admin_delete_item(db_conn,temp[0])
            if x=="admin_delete_item_sucess":conn.send(b"admin_delete_item_sucess")
            else:conn.send(b"admin_delete_item_err")



        elif "--contact_us_add" in data_x:
            print("[*]Recv php new add_contact req")
            temp=data_x.split("--")
            x=contact_us_add(db_conn,temp[0],temp[1],temp[2])
            if x=="new_contactus_add_success":conn.send(b"new_contactus_add_success")
            else:conn.send(b"new_contactus_add_ERR")

        elif "--volunteer_add" in data_x:
            print("[*]Recv php new add_volunteer req")
            temp=data_x.split("--")
            x=volunteer_add(db_conn,temp[0],temp[1],temp[2])
            if x=="new_volunteer_add_success":conn.send(b"new_volunteer_add_success")
            else:conn.send(b"new_volunteer_add_ERR")


        elif "--get_contact" in data_x:
            print("[*]Recv php new add_volunteer req")
            temp=data_x.split("--")
            x=common_fetch(db_conn,"Contact_info")

            if x=="err_fetch_admin_common_data":conn.send(b"err_fetch_admin_common_data") # if err 
            else: #processing op
                temp_holder=[]
                for data0 in x:
                    for data1 in data0:
                        temp_holder.append(str(data1)) #["1","2","3","4"]
                temp_holder2=""
                for data in temp_holder:
                    temp_holder2=temp_holder2+data+"--"
                temp_holder2=temp_holder2[:-2]
                temp_holder2=temp_holder2+"--contact_us_gg"
                #print(temp_holder2) # "1--2--3--4"
                temp_holder2=bytes(temp_holder2,'utf-8')
                conn.send(temp_holder2)

        elif "--get_volunteer" in data_x:
            print("[*]Recv php new add_volunteer req")
            temp=data_x.split("--")
            x=common_fetch(db_conn,"Volunteer_info")

            if x=="err_fetch_admin_common_data":conn.send(b"err_fetch_admin_common_data") # if err 
            else: #processing op
                temp_holder=[]
                for data0 in x:
                    for data1 in data0:
                        temp_holder.append(str(data1)) #["1","2","3","4"]
                temp_holder2=""
                for data in temp_holder:
                    temp_holder2=temp_holder2+data+"--"
                temp_holder2=temp_holder2[:-2]
                temp_holder2=temp_holder2+"--volunteer_gg"
                #print(temp_holder2) # "1--2--3--4"
                temp_holder2=bytes(temp_holder2,'utf-8')
                conn.send(temp_holder2)


        elif "--get_client_item_list" in data_x:
            print("[*]Recv php new Get_Client_item req")
            temp=data_x.split("--")
            x=admin_fetch_item(db_conn,temp[0])
            if len(x)==0:conn.send(b'No items Yet');return
            if x=="err_fetch_admin_common_data":conn.send(b"err_fetch_admin_common_data") # if err 
            else: #processing op
                temp_holder=[]
                for data0 in x:
                    for data1 in data0:
                        temp_holder.append(str(data1)) #["1","2","3","4"]
                temp_holder2=""
                for data in temp_holder:
                    temp_holder2=temp_holder2+data+"--"
                temp_holder2=temp_holder2[:-2]
                #print(temp_holder2) # "1--2--3--4"
                temp_holder2=bytes(temp_holder2,'utf-8')
                conn.send(temp_holder2)

        elif "--0get_client_item_list_cart" in data_x:
            print("[*]Recv php new Get_Client_item_CART req")
            temp=data_x.split("--")
            x=admin_fetch_item(db_conn,"",temp[0]) #do not change param structure 
            if len(x)==0:conn.send(b'No items Yet');return
            if x=="err_fetch_admin_common_data":conn.send(b"err_fetch_admin_common_data") # if err 
            else: #processing op
                temp_holder=[]
                for data0 in x:
                    for data1 in data0:
                        temp_holder.append(str(data1)) #["1","2","3","4"]
                temp_holder2=""
                for data in temp_holder:
                    temp_holder2=temp_holder2+data+"--"
                temp_holder2=temp_holder2[:-2]
                #print(temp_holder2) # "1--2--3--4"
                temp_holder2=bytes(temp_holder2,'utf-8')
                conn.send(temp_holder2)


        elif "--post_order" in data_x:
            print("[*]Recv php new add_Post_Order req")
            temp=data_x.split("--")
            temp[1]=temp[1][:-2] #removeing extra ^^ from back
            x=add_post_order(db_conn,temp[0],temp[1],temp[2],temp[3])
            if x=="new_order_success":conn.send(b"new_order_success")
            else:conn.send(b"new_order_failed")

        elif "--get_admin_order_list" in data_x:
            print("[*]Recv php new Get_Client_order req")
            temp=data_x.split("--")
            x=admin_fetch_item(db_conn,temp[0],order=True)
            if len(x)==0:conn.send(b'No items Yet');return
            if x=="err_fetch_admin_common_data":conn.send(b"err_fetch_admin_common_data") # if err 
            else: #processing op
                temp_holder=[]
                for data0 in x:
                    for data1 in data0:
                        temp_holder.append(str(data1)) #["1","2","3","4"]
                temp_holder2=""
                for data in temp_holder:
                    temp_holder2=temp_holder2+data+"--"
                temp_holder2=temp_holder2[:-2]
                #print(temp_holder2) # "1--2--3--4"
                temp_holder2=bytes(temp_holder2,'utf-8')
                conn.send(temp_holder2)

        else:print("Error in req rcv...")

    except BufferError as e:
        print("[-] Remote Conn Dc")
        print(e)
        return # thread will die

    print("Closing conn")
    conn.close()

listen()
