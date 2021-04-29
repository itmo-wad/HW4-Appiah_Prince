from flask import flash, redirect,url_for,Flask, send_from_directory, render_template, request
from flask_login import login_required, logout_user,login_user, LoginManager, UserMixin
import random 
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = b'mylittlsecretewrwegiweug093gewjgjoiew'
login_manager = LoginManager()
login_manager.init_app(app)
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.users


class User(UserMixin):
    def __init__(self, username, password):
        self.id = random.randint(1,1000)
        self.password = password
        self.username = username

    def is_active(self):
        return True
    

    def get_id(self):
        return self.username

current_users = {
}
activated_users = {}
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.my_users.find_one({"username": username})
        if user and password == user['password']:
            user = User(username,password)
            login_user(user)
            activated_users[username] = user
            return redirect(url_for('cabinet'))
        else:
            flash('Invalid username or password')
            return render_template('index.html', title='My Image Gallery')
    if request.method == 'GET':
        return render_template('index.html', title='My Image Gallery')
        

@login_manager.user_loader
def load_user(username):
    return activated_users.get(username)

@app.route('/cabinet')
@login_required
def cabinet():
    return render_template('cabinet.html')
    
    


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)
@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
    
    
if __name__ == "__main__":
    app.run(debug=True)

