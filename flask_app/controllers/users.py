from flask_app import app,bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.users_model import User
from flask_app.models.challenge_model import Challenge

@app.route('/')
def home():
    users=User.get_all_order_by_rank()
    challenges=Challenge.get_all()
    return render_template('index.html',users=users,challenges=challenges)

@app.route('/register_form')
def register_form():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    print(request.form)

    if not User.user_is_valid(request.form):
        return redirect("/register_form")
    User.create(request.form)
    return redirect('/log_in_form')

@app.route('/log_in_form')
def log_in_form():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/log_in',methods=['POST'])
def login():
    data={
        'email':request.form['email'],
        'password':request.form['password']
    }
    if User.validate_login(data):
        return redirect('/')
    return redirect('log_in_form')


@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')

@app.route('/profile/<int:id>')
def profile(id):
    if session['user_id'] == id:
        user = User.get_by_id(id)
        ranks = User.get_5_order_by_rank(user.rank)
        return render_template('profile.html',user=user,ranks=ranks)
    return redirect('/')
    
@app.route('/view/<int:id>')
def view(id):
    if 'user_id' in session:
        if session['user_id']==id:
            return redirect(f'/profile/{id}')
    user = User.get_by_id(id)
    ranks = User.get_5_order_by_rank(user.rank)
    return render_template('view.html',user=user,ranks=ranks)    