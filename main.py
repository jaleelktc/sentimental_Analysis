import database as db
from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

app.secret_key = "LJHGJSJD&*(A^TYI#UYAGSDJABEWL"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():

    if "submit" in request.form:
        username = request.form['username']
        password = request.form['password']
        if(db.login2(username,password)):

            return redirect(url_for('admin_home'))
        else:
            return render_template('login.html')



    return render_template('login.html')
@app.route('/signup/',methods=['get','post'])
def register():
    #db.signu()
   # username = request.form['l_id']
    #password = request.form['pwd']
    if "submit" in request.form:
        username = request.form['l_id']
        password = request.form['pwd']
        dob=request.form['dob']
        address=request.form['addr']
        fname=request.form['f_name']
        lname=request.form['l_name']
        gender=request.form['gender']
        if(db.login2(fname,lname,address,dob,gender,username,password)):

            return redirect(url_for('product'))
        else:
            return render_template('feature')


   # q = "insert  into login(username,password,type)values('%s','%s','%s')"% (username,password,"user")

    return redirect(url_for('user2'))


@app.route('/admin_home/')
def admin_home():
    if db.is_login():
        return render_template('admin_home.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    db.logout()
    return redirect(url_for('login'))
@app.route('/signup/',methods=['get','post'])
def signup():
    #db.signu()
    username = request.form['username']
    password = request.form['password']

    q = "insert  into login(username,password,type)values('%s','%s','%s')"% (username,password,"user")

    return redirect(url_for('user2'))


if __name__ ==  "__main__":
    app.run(debug=True)



