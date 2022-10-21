from flask import render_template,redirect,request,session,flash
from flask_app.models.challenge_model import Challenge
from flask_app import app

@app.route('/challenge',methods=['POST'])
def challenge():
    data ={
        'challenger_id':session['user_id'],
        'challenged_id':request.form['challenged_id']
    }
    Challenge.challenge(data)
    user = session['user_id']
    return redirect(f'/profile/{user}')