from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('signup_form.html', title='Signup')

def verify_input(input):
    if input=='':
        return False
    elif len(input)<3 or len(input)>20:
        return False
    else:
         for letter in input:
            if letter==' ':
                return False
    return True

@app.route('/', methods=['POST'])
def verify():
    username=request.form['username']
    password=request.form['password']
    confirm=request.form['confirm']
    email=request.form['email']
    username_error=''
    password_error=''
    confirm_error=''
    email_error=''
    at_count=0
    dot_count=0
    space_count=0

    if not verify_input(username):
        username_error='Username must be between 3 and 20 characters, and contain no spaces.'   
            
    if not verify_input(password):
        password_error='Password must be between 3 and 20 characters, and contain no spaces.'
        
    if confirm == '':
        confirm_error='Please confirm your password.'
    else:
        for idx in range(len(password)):
            if password[idx] != confirm[idx]:
                confirm_error='Passwords do not match. Please confirm password.'

    if (len(email)>2 and len(email)<21):
        email_error=''
    elif len(email)==0:
        email_error=''
    
    for letter in email:
        if letter == ' ':
            space_count+=1
        if letter=='@':
            at_count += 1
        if letter=='.':
            dot_count += 1
        if (dot_count == 1 and at_count == 1) and space_count==0:
            email_error=''
        else:
            email_error='You must enter a valid email address.'

    if username_error=='' and password_error=='' and confirm_error=='' and email_error=='':
        return redirect('/hello?username={}'.format(username))

    return render_template('signup_form.html', username_error=username_error, password_error=password_error, confirm_error=confirm_error, 
        email_error=email_error, username=username, email=email, title='Signup')
    
@app.route('/hello', methods=['POST', 'GET'])
def display_hello():
    username=''
    username=request.args.get('username')
    return render_template('hello.html', username=username)

app.run()