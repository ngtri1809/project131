from sqlalchemy import or_
from app import db
from glob import escape
from flask import flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from app.models import Message, User, Todo
from .forms import ComposeForm, LoginForm, RegisterForm
from app import myapp_obj

# the front page of the website, uses "base.html" for the format
# have login and create account buttons
@myapp_obj.route("/")
def front():
    return render_template('base.html')

# login page
@myapp_obj.route("/login", methods=['GET', 'POST']) #uses GET and POST method to request or send data to the database
def login():
    form = LoginForm() #login form - includes username and password fields
    error = None  
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() #finds user in database with inputted username
        if user:           # if user exists in database
            if user.check_password(form.password.data): #checks password
                login_user(user)                        #log user in
                return redirect(url_for('mainpage'))    #send user to mainpage
            else:         # password does not match
                error = 'Invalid password. Please try again.'
        else: # username doesn't exist
            error = 'Invalid username. Please try again.'
    return render_template('login.html', form=form, error=error) #stay on login page with error message prompted

# register page
@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm() #register form - includes username, email, and password fields
    error = None
    if form.validate_on_submit():
        #check for existing user in database
        existing_user = User.query.filter(or_(User.username==form.username.data, User.email==form.email.data)).first()
        if existing_user: #if username or/and email already exist in database: prompt error message
            if existing_user.username == form.username.data and existing_user.email != form.email.data:
                error = 'This username is already taken. Please choose a different one.'
            if existing_user.email == form.email.data and existing_user.username != form.username.data:
                error = 'This email is already taken. Please choose a different one.'
            if existing_user.email == form.email.data and existing_user.username == form.username.data:
                error = 'This username and email is already taken. Please choose a different ones.'
            return render_template('register.html', form=form, error=error) #stay on register page but with error message prompted
        new_account = User(username=form.username.data, email = form.email.data) #if not an existing user, create new user in database
        new_account.set_password(form.password.data) #set password
        db.session.add(new_account) #add new account into database (like staging changes into database)
        db.session.commit() #commit the change
        return render_template('registered.html', name=new_account.username) #sends user to a successful registration screen
    return render_template('register.html', form=form) #stay on register page (failed registration)

#main page of the website
@myapp_obj.route("/mainpage", methods=['GET', 'POST'])
@login_required #needs to be logged in to access this page
def mainpage():
    messages = current_user.received_messages() #get sent messages
    #renders the main page with messages and name filled in as the parameter in mainpage.html
    return render_template('mainpage.html', messages=messages, name = current_user.username)

#logout
@myapp_obj.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user() #log user out
    return redirect(url_for('login')) #go back to login page

#settings page
@myapp_obj.route("/settings")
@login_required #
def settings():
    return render_template('settings.html') #has delete account button (for now)

#delete account button
@myapp_obj.route("/delete", methods=['POST']) #only use POST method to change database, no need to "GET" something from database
@login_required
def delete():
    db.session.delete(current_user) #delete user from database
    db.session.commit() #commit the changes
    logout_user()
    return redirect(url_for('front')) #go back to front page

#compose message page
@myapp_obj.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    form = ComposeForm() #includes recipient, subject, and body fields, with send button
    error = None
    if form.validate_on_submit():
        the_recipient = User.query.filter_by(username=form.recipient.data).first() #finds inputted recipient from database
        if the_recipient is None: #if recipient doesn't exist in database
            error = "Invalid recipient"
            render_template('compose.html', form=form, error=error) #stay on compose page but with error message prompted
        
        #generate new Message object with inputted data from the user 
        message = Message(sender=current_user, recipient=the_recipient, subject=form.subject.data, body=form.body.data)
        db.session.add(message) #puts message into database
        db.session.commit() #commit the changes
        return redirect(url_for('mainpage')) #go back to main page
    return render_template('compose.html', form=form, error=error) #stay on compose page (failed composing)

#view received messages
@myapp_obj.route('/message/<int:message_id>')
@login_required
def message(message_id):
    message = Message.query.get(message_id) #get the Message object id from the database
    return render_template('message.html', message=message) #renders the message

#view sent messages
@myapp_obj.route('/sent')
@login_required
def sent():
    #get the Message object sent by the user, orderd by time sent
    messages = Message.query.filter_by(sender=current_user).order_by(Message.timestamp.desc()).all()
    return render_template('sent.html', messages=messages) #renders the sent messsages page

#To Do List
@login_required
@myapp_obj.route('/add', methods=['POST'])
def add():
    user=current_user
    name=request.form.get("name")
    new_task=Todo(name=name,done=False,user=user)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("todo"))

@myapp_obj.route("/update/<int:todo_id>")
@login_required
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done=not todo.done
    db.session.commit()
    return redirect(url_for("todo"))

@myapp_obj.route("/delete_item/<int:todo_id>", methods=['GET'])
def delete_item(todo_id):
    todo_item = Todo.query.get(todo_id)
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for("todo"))

@myapp_obj.route("/todo", methods=['POST','GET'])
def todo():
    todo_list = Todo.query.filter_by(user=current_user)
    return render_template('todo.html', todo_list=todo_list)

