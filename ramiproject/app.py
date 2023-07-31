from flask import Flask, render_template, request, url_for, redirect
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyBCit4rhA69ery5AOUwapwgIuBxQ6dPTcU",
  "authDomain": "perproject-b8374.firebaseapp.com",
  "databaseURL": "https://perproject-b8374-default-rtdb.firebaseio.com",
  "projectId": "perproject-b8374",
  "storageBucket": "perproject-b8374.appspot.com",
  "messagingSenderId": "915840003376",
  "appId": "1:915840003376:web:ae516d55bf176ddcb42cf5",
  "measurementId": "G-CR36N26NJQ",
  "databaseURL":"https://perproject-b8374-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



app = Flask(__name__,template_folder = 'templates' ,static_folder = 'static' )
app.config['SECRET_KEY'] = 'super-secret-key'



# @app.route('/',methods=['GET'])  # '/' for the default page
# def index():
#   if request.method == 'GET':
#     return render_template('index.html')
  

@app.route('/',methods=['GET', 'POST'])  # '/' for the default page
def index():
  return render_template("index.html")





@app.route('/login',methods=['GET', 'POST'])  # '/' for the default page
def login():
  
  if request.method == 'GET':
    return render_template('login.html')
  else:
    try:
      email = request.form["email"]
      password = request.form["password"]
      
      login_session['user'] = auth.sign_in_with_email_and_password(email,password)
      print("231wdaw2")
      return redirect(url_for('main'))


    except Exception as e :
      print(e)
      return render_template("login.html")




@app.route('/signup',methods=['GET', 'POST'])  # '/' for the default page
def signup():
 
  
  if request.method == 'GET':
    return render_template('signup.html')
  else:
    try:
      name = request.form["fullname"]
      username = request.form["username"]
      password = request.form["password"]
      email = request.form["email"]
      pic = request.form["pic"]
      info = {"username":username,"name":name,"email":email,"pic": pic,"following":{"user":"user"},"added":{"ihf98ew34r9ur93u4r93u4r"}}
      login_session['user']= auth.create_user_with_email_and_password(email,password)
      uid = login_session['user']['localId']
      db.child('users').child(uid).set(info)
      return redirect(url_for("main"))
    except Exception as e:
      print("dawdawdawd")
      print(e)
      return render_template("signup.html")




@app.route('/main',methods=['GET', 'POST'])  # '/' for the default page
def main():
  if request.method == 'GET':
    dict =db.child('users').child(login_session['user']['localId']).get().val()
    return render_template('main.html',id = dict['username'], seid =login_session['user']['localId'] ,db = db,dict1 = db.child('users').get().val())
  else:
    x = 'profile/'+request.form["search"]
    return redirect(url_for('profile', name = request.form['search']))




@app.route('/profile/<string:name>',methods=['GET', 'POST'])  # '/' for the default page
def profile(name):
  try:

    r =0 



    y = ""
    for x in db.child('users').get().val():
      if name == db.child('users').get().val()[x]["username"]:
        y = x
        break
    data = db.child("users").child(login_session['user']['localId']).child("following").get().val()
    if name in data.values():
      r= 1



    return render_template('profile.html',db = db.child("users").get().val(),id = y,seid =login_session['user']['localId'],r = r)
  except Exception as e:
      print(e)
      return redirect(url_for("main"))

@app.route('/add',methods=['GET', 'POST'])  # '/' for the default page
def add():
  
  if request.method == 'GET':
    return render_template('add.html')
  else:
    try:
      movie = request.form["name"]
      url = request.form["url"]
      note = request.form["note"]
      
      rate = {"name":movie,"url":url,"note":note,"number":0}
      uid = login_session['user']['localId']
      db.child('users').child(uid).child("rates").push(rate)

      return redirect(url_for("main"))
    except :
      return render_template('add.html')


@app.route('/add/<string:name2>/<string:x6>',methods=['GET', 'POST'])  # '/' for the default page
def join(name2,x6):
    
    dict6 =db.child('users').child(x6).child("rates").get().val()
    for t in dict6:
      print("===========================")
      print(t)
      if name2 == dict6[t]["name"]:
        db.child('users').child(x6).child("rates").child(t).child("number").set(dict6[t]["number"]+1)
        db.child("users").child(login_session['user']['localId']).child("added").push(t)
        return redirect(url_for('main'))


    print(dict6)
    return redirect(url_for('main' ))
  



@app.route('/logout')
def logout():
  auth.current_user = None
  login_session['user'] = None
  return redirect(url_for('main'))





@app.route('/follow/<string:name1>',methods=['GET'])  # '/' for the default page
def follow(name1):
  x1 = db.child('users').child(name1).get().val()
  b1 = db.child('users').child(login_session['user']['localId']).get().val()
  print("=================================")
  print(db.child('users').child(name1).get().val()['username'])
  db.child('users').child(login_session['user']['localId']).child('following').push(x1['username'])

  print(db.child('users').child(login_session['user']['localId']).child('username').get().val())
  return redirect(url_for("main"))


@app.route('/following',methods=['GET'])  # '/' for the default page
def following():
  dict3 =db.child('users').child(login_session['user']['localId']).get().val()
  return render_template("following.html",id = dict3['username'],dict2=list(db.child('users').child(login_session['user']['localId']).get().val()['following'].values()),dict1 = db.child('users').get().val())


@app.route('/about',methods=['GET'])  # '/' for the default page
def about():
  return render_template("about.html")


if __name__ == '__main__':
  app.run(debug=True)