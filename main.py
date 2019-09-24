from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user-signup:root@localhost:3306/user-signup'
app.config['SQLALCHEMY_ECHO'] = True  #helps debug by giving information in the terminal
db = SQLAlchemy(app)

class Signup(db.Model):
    
    id = db.Column(db.Integer, primary_key=True) #id column in database
    name = db.Column(db.String(20),nullable=False) #username column in database
    pw = db.Column(db.String(20),nullable=False) #password column in database
    email = db.Column(db.String(20),nullable=True) #email column in database


    def __init__(self, name, pw, email):
        self.name = name
        self.pw = pw
        self.email = email

# @app.route('/added-user', methods=['POST']) #after validating entries, get sent to welcome page.
# def welcome():
#     return render_template("welcome.html",username=request.form['username'])

@app.route('/validate', methods=['POST']) #after submitting form, entries are validated
def validate():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    for i in username:
        if i == " ":
            error = "Username should not have any spaces."
            return render_template("index.html",error=error, username=username,email=email)

    for i in password:
        if i == " ":
            error = "Password should not have any spaces."
            return render_template("index.html",error1=error, username=username,email=email)

    for i in email:
        if i == " ":
            error = "Email should not have any spaces."
            return render_template("index.html",error3=error, username=username,email=email)

    
 
    if len(username) < 3 or len(username) > 20:
        error = "Entry is not valid.  Username needs to be between 3-20 character long"
        return render_template("index.html",error=error, username=username,email=email)

    elif len(password) < 3 or len(password) > 20:
        error = "Password entry is not valid.  Password needs to be between 3-20 character long."
        return render_template("index.html",error1=error, username=username,email=email)

    elif len(verify) < 3:
        error = "Password does not match.  Entry does not seem to be long enough."
        return render_template("index.html",error2=error, username=username,email=email)

    elif password != verify:
        error = "Password does not match.  Please confirm they are the same in both fields."
        return render_template("index.html",error2=error, username=username,email=email)

    elif len(email) > 0:
        if "@" not in email:
            error = """Email should contain '@' symbol."""
            return render_template("index.html",error3=error, username=username,email=email)
        
        elif "." not in email:
            error = """Email should contain '.' """
            return render_template("index.html",error3=error, username=username,email=email)

        else:       #after passing above condition, user is sent to welcome page
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                verify = request.form['verify']
                email = request.form['email']
                new_user = Signup(username,password,email)
        
                db.session.add(new_user)
                db.session.commit()
    
        
        return render_template("welcome.html",username=request.form['username'])

        
     
        
 
    
@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run()