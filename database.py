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


def login(username,password):
    cnx = mysql.connector.connect(user="root",password="root",host="localhost",database="project")
    cur = cnx.cursor(dictionary=True)
    cur.execute("select * from login where username='%s' and password ='%s'" % (username,password))
    result = cur.fetchall()
    if len(result) == 1 :
        session['user_id'] = result[0]['user_id']
        session['user_type'] = result[0]['user_type']
        return True
    else:
        return False

def is_login():
    if "user_id" in session and "user_type" in session:
        return True
    else:
        return False

def logout():
    session.clear()

def register(fname,lname,address,dob,gender,username,password):
    q = "insert into login (username,passsword,type) values ('%s','%s','%s')" % (username,password,"user")
    login_id = insert(q)
    q = "insert into user2 (`fname`, `lname`, `address`, `dob`, `gender`, `l_id`) VALUES('%s','%s','%s','%s','%s'))" %(fname, lname, address, dob, gender,login_id)
    if(insert(q) > 0):
        return True
    else:
        return False