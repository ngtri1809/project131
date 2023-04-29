from sqlalchemy import or_
from app import db
from glob import escape
from flask import flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Message, User, Todo, Friend
from .forms import ComposeForm, LoginForm, RegisterForm, ChangePasswordForm
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
    sort_by = request.form.get("sort")
    asc = Message.query.filter_by(recipient=current_user).order_by(Message.timestamp.asc()).all()
    des = Message.query.filter_by(recipient=current_user).order_by(Message.timestamp.desc()).all()
    #renders the main page with messages and name filled in as the parameter in mainpage.html

   

    return render_template('mainpage.html', sort_by=sort_by, des=des, asc=asc,name=current_user.username)

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

#request.method == 'POST' and 
#change password
@myapp_obj.route("/changepassword", methods=['GET','POST']) 
@login_required
def changepassword(): 
    form = ChangePasswordForm() #take ChangePasswordForm class in from forms.py
    if request.method == 'POST' and form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first() #checks if user's email matches
        if user: #if email is in db
            user.password = generate_password_hash(form.new_password.data) #Creates hash for new password and assigns it as the actual password
            db.session.commit() #saves new password into database
            return redirect(url_for('mainpage')) #take user back to main page
    return render_template('changepassword.html', form=form) #if conditions not fulfilled then stay on page

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
            return render_template('compose.html', form=form, error=error) #stay on compose page but with error message prompted
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

#add task
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

@myapp_obj.route("/todo", methods=['POST','GET'])
@login_required
def todo():
    todo_list = Todo.query.filter_by(user=current_user)
    return render_template('todo.html', todo_list=todo_list)

#delete account
@myapp_obj.route("/delete", methods=['POST']) #only use POST method to change database, no need to "GET" something from database
@login_required
def delete():
    todo_list = Todo.query.filter_by(user=current_user)
    inbox_messages = Message.query.filter_by(recipient=current_user).all()
    sent_messages = Message.query.filter_by(sender=current_user).all()
    for todo in todo_list:
        db.session.delete(todo)
    for message in sent_messages:
        db.session.delete(message)
    for message in inbox_messages:
        db.session.delete(message)
    db.session.delete(current_user) #delete user from database
    db.session.commit() #commit the changes
    logout_user()
    return redirect(url_for('front')) #go back to front page

@myapp_obj.route("/delete_item/<int:todo_id>", methods=['GET'])
@login_required
def delete_item(todo_id): #delete item from to do list in the database
    todo_item = Todo.query.get(todo_id)
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for("todo"))

from sqlalchemy.exc import IntegrityError

@myapp_obj.route('/add_friend', methods=['GET', 'POST'])
def add_friend(): #add friend object based on the email and friend to the database
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        friend = Friend(name=name, email=email)
        db.session.add(friend)
        #This tries to commit the new Friend object to the database
        try: #if friend with email does not exist commit
            db.session.commit()
            flash('Friend added successfully.')
            return redirect(url_for('friend_list'))
        except IntegrityError: #prompt error message if friend with email already exist
            db.session.rollback()
            flash('Friend with email {} already exists.'.format(email))
            return redirect(url_for('friend_list'))
    return render_template('add_friend.html')

@myapp_obj.route('/delete_friend/<int:id>', methods=['POST'])
def delete_friend(id): #delete friend object in the database
    friend = Friend.query.get_or_404(id) #retrieve Friend object based on the primary key id
    db.session.delete(friend) 
    db.session.commit()
    return redirect(url_for('friend_list'))

@myapp_obj.route('/friend_list', methods=['GET','POST'])
@login_required
def friend_list(): #display all the friend object in the database
    friends = Friend.query.all()
    return render_template('friend_list.html', friends=friends)


