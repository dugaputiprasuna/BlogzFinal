from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://prasuna1:prasuna1@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    Blogs = db.relationship('Blogs', backref='owner', lazy='dynamic')
    def __init__(self, username , password):
        self.username  = username 
        self.password = password

        
class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(120))
    post = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
 
    def __init__(self,title,post,owner):
        self.title = title
        self.post = post
        self.owner=owner



@app.route('/login', methods=['POST', 'GET'])
def login():
    user=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
  
        if len(username)==0:
            unamemsg=" Username is blank"
            return render_template('login.html',username=username,unamemsg=unamemsg)  
        elif len(password)==0:
            passwordmsg="Password is Blank"
            return render_template('login.html',username=username,passwordmsg=passwordmsg)
            
        user= User.query.filter_by(username=username).first()
        if user and user.password==password:
  
            session['username']=user.username
            session['userid']=user.id
            return render_template('newpost.html')
        elif user and user.password!=password:
            passwordmsg='User password incorrect!!'
            return render_template('login.html',username=username,passwordmsg=passwordmsg)
        else:
            unamemsg='Invalid User credentials!!'
            return render_template('login.html',username=username,unamemsg=unamemsg)
    else:
        return render_template('login.html')
@app.route('/register', methods=['POST', 'GET'])
def registeruser():
     return render_template('signup.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
   
    if request.method == 'POST':
      
        username = request.form['username']
        password = request.form['password']
        verifypassword= request.form['verifypassword']
        signupmessage=""
        errormsg=""
       
        if len(username)==0:
            unamemsg=" Username is blank"
            return render_template('signup.html',username=username,unamemsg=unamemsg)  
        elif len(password)==0:
            passwordmsg="Password is Blank"
            return render_template('signup.html',username=username,passwordmsg=passwordmsg)
        elif len(verifypassword)==0:       
            verifyPasswordmsg="Verify Password is Blank"
            return render_template('signup.html',username=username,verifyPasswordmsg=verifyPasswordmsg)  
        elif password != verifypassword:
            errormsg="Password and Confirm password mismatch! "
            return render_template('signup.html',username=username,passwordmsg=errormsg)
       
        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            signupmessage="User has been added successfully!"
            session['username']=username
            return render_template('newpost.html',signupmessage=signupmessage)
        else:
            signupmessage="User  "+ username + "  already exists"
            return render_template('signup.html',signupmessage=signupmessage)
            

@app.route("/blog", methods=['POST', 'GET'])
def blogInfo():
       bid=""  
       blogs=""
       userid=""
       
       if request.method == 'GET':
          id = request.args.get('id')
          userid=request.args.get('userid')
       
       if id :
           bid=id
           blogs = Blogs.query.filter_by(id=bid).all()
       elif userid:
            blogs = Blogs.query.filter_by(owner_id=userid).all()

       else:
           blogs = Blogs.query.all()
         
       return render_template('blog.html',blogs=blogs,id=bid)


@app.route('/logout')
def logout():
    if session.get('username') is not None:
        del session['username']
    
    return redirect('/')

@app.route("/newpost", methods=['POST', 'GET'])
def newpostInfo():
        if session.get('username') is not None:
          return render_template('newpost.html')
        else:
            return render_template('login.html')



@app.route("/Saveblog", methods=['POST'])
def SavePostInfo():
      title = request.form['title']
      post = request.form['post']
      titlemsg=""
      postmsg=""
      owner = User.query.filter_by(username=session['username']).first()

      if len(title) == 0:
          titlemsg = "please enter the blog title"
      if len(post) == 0:
          postmsg="please enter the blog post"
  
      if len(titlemsg) or len(postmsg):
          return render_template('newpost.html',title=title,post=post,titlemsg=titlemsg,postmsg=postmsg)
      else:
           
          new_blog = Blogs(title, post,owner)
          db.session.add(new_blog)
          db.session.commit()
         
          #return redirect('/blog')
          return redirect('/blog?id='+str(new_blog.id))
         
     
@app.route('/', methods=['POST', 'GET'])
def index():
   users=""


   users = User.query.all()
   return render_template('index.html',users=users)

if __name__ == '__main__':
    app.run()
