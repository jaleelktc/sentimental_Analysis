import database as db
from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

app.secret_key = "LJHGJSJD&*(A^TYI#UYAGSDJABEWL"

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():

    if "submit" in request.form:
        username = request.form['username']
        password = request.form['password']
        #if(db.login2(username,password)):
            # pass
        res=db.login2(username,password)
        if (res=='admin'):
            return redirect(url_for('admin_home'))
        #else:
        elif(res=='user'):
            return redirect(url_for('user_home'))
            # pass
        else:
         return render_template('index.html')

@app.route('/user2/',methods=['get','post'])
def register():
    if "submit" in request.form:
        username = request.form['l_id']
        password = request.form['pwd']
        dob=request.form['dob']
        fname=request.form['f_name']
        lname=request.form['l_name']
        gender=request.form['gender']
        if(db.register(fname,lname,dob,gender,username,password)):


            return redirect(url_for('product'))
        else:
            return render_template('feature')


   # q = "insert  into login(username,password,type)values('%s','%s','%s')"% (username,password,"user")

    return render_template('user2.html')


@app.route('/admin_home/')
def admin_home():
    if db.is_login():
        return render_template('admin_home.html')
    else:
        return redirect(url_for('index'))

@app.route('/user_home/')
def user_home():
    if db.is_login():
        return render_template('user_home.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout/')
def logout():
    db.logout()
    return redirect(url_for('index'))

@app.route('/signup/',methods=['get','post'])
def signup():
    username = request.form['username']
    password = request.form['password']

    q = "insert  into login(username,password,type)values('%s','%s','%s')"% (username,password,"user")

    return redirect(url_for('user2'))


@app.route('/about/',methods=['get','post'])
def about():
    return render_template("about.html")
@app.route('/contact/',methods=['get','post'])
def contact():
    return render_template("contact.html")
@app.route('/product/',methods=['get','post'])
def product():
    if "submit" in request.form:
        pname = request.form['pname']
        if (db.addproduct(pname)):
            return redirect(url_for('product'))
        else:
            print ("errr")

    return render_template("product.html")

if __name__ ==  "__main__":
    app.run(debug=True)



