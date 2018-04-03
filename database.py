import mysql.connector
from flask import  session

def select(q):
    cnx = mysql.connector.connect(user="root", password="root", host="localhost", database="project")
    cur = cnx.cursor(dictionary=True)
    cur.execute(q)
    return cur.fetchall()
def insert(q):
    cnx = mysql.connector.connect(user="root", password="root", host="localhost", database="project")
    cur = cnx.cursor(dictionary=True)
    cur.execute(q)
    cnx.commit()
    return cur.lastrowid

#product adding
def addproduct(pname):
    cnx = mysql.connector.connect(user="root", password="root", host="localhost", database="project")
    cur = cnx.cursor(dictionary=True)
    q="insert into product(`pname`) VALUES('%s')" % (pname)
    cur.execute(q)
    cnx.commit()
    return cur.lastrowid



def login2(username,password):
    cnx = mysql.connector.connect(user="root",password="root",host="localhost",database="project")
    cur = cnx.cursor(dictionary=True)
    cur.execute("select * from login2 where uname='%s' and password ='%s'" % (username,password))
    result = cur.fetchall()
    if len(result) == 1 :
        t=result[0]['type']
        session['user_id'] = result[0]['l_id']
        session['user_type'] = result[0]['type']
        return t
    else:
        return False

def is_login():
    if "user_id" in session and "user_type" in session:
        return True
    else:
        return False

def logout():
    session.clear()

def register(fname,lname,dob,gender,username,password):
    q = "insert into login2 (`uname`,`password`,`type`) values ('%s','%s','%s')" % (username,password,"user")
    login_id = insert(q)
    q = "insert into user2 (`fname`, `lname`, `dob`, `gender`, `l_id`) VALUES('%s','%s','%s','%s','%s')" %(fname, lname, dob, gender,login_id)
    if(insert(q) > 0):
        return True
    else:
        return False