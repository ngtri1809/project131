from datetime import datetime
from sqlalchemy import not_, or_
from app import db
from glob import escape
from flask import flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Message, User, Todo, Friend
from .forms import ComposeForm, LoginForm, RegisterForm, ChangePasswordForm, updateForm
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
        if '@' not in form.email.data or '.' not in form.email.data or form.email.data.count('.') > 1 or form.email.data.count('@') > 1:
            error = 'Invalid email address. Please enter a valid email address.'
            return render_template('register.html', form=form, error=error)
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
    error = None
    if request.method == 'POST' and form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first() #checks if user's email matches
        if user: #if email is in db
            user.password = generate_password_hash(form.new_password.data) #Creates hash for new password and assigns it as the actual password
            db.session.commit() #saves new password into database
            return redirect(url_for('mainpage')) #take user back to main page
        else:
            error = "Invalid email" #resets the page when user enters the wrong email
            return render_template('changepassword.html', form=form, error=error)
    return render_template('changepassword.html', form=form, error=error) #if conditions not fulfilled then stay on page

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
        message = Message(sender=current_user, recipient=the_recipient, subject=form.subject.data, body=form.body.data, timestamp = datetime.now())
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
    name=request.form.get("name") #get task name
    new_task=Todo(name=name,done=False,user=user) #create new Todo object
    db.session.add(new_task) #add it to database
    db.session.commit() #commit
    return redirect(url_for("todo"))


#update task
@myapp_obj.route("/update/<int:todo_id>")
@login_required
def update(todo_id):
    todo = Todo.query.get(todo_id) #get that task
    todo.done=not todo.done #updates it to done
    db.session.commit() #commit
    return redirect(url_for("todo"))

#todo list
@myapp_obj.route("/todo", methods=['POST','GET'])
@login_required
def todo():
    todo_list = Todo.query.filter_by(user=current_user) #gets todo list of current user
    return render_template('todo.html', todo_list=todo_list)

#delete account
@myapp_obj.route("/delete", methods=['POST']) #only use POST method to change database, no need to "GET" something from database
@login_required
def delete():
    todo_list = Todo.query.filter_by(user=current_user)
    inbox_messages = Message.query.filter_by(recipient=current_user).all()
    sent_messages = Message.query.filter_by(sender=current_user).all()
    friends = Friend.query.filter_by(user_id=current_user.id).all()
    for todo in todo_list:
        db.session.delete(todo)
    for message in sent_messages:
        db.session.delete(message)
    for message in inbox_messages:
        db.session.delete(message)
    for friend in friends:
        db.session.delete(friend)
    db.session.delete(current_user) #delete user from database
    db.session.commit() #commit the changes
    logout_user()
    return redirect(url_for('front')) #go back to front page

#delete todo task
@myapp_obj.route("/delete_item/<int:todo_id>", methods=['GET'])
@login_required
def delete_item(todo_id): 
    todo_item = Todo.query.get(todo_id) #get the task item
    db.session.delete(todo_item) #delete it
    db.session.commit() # commit
    return redirect(url_for("todo"))

@myapp_obj.route("/undo/<int:message_id>", methods=['POST'])
@login_required
def undo(message_id):
    last_message = Message.query.get(message_id) #gets message_id
    db.session.delete(last_message) #deletes the message
    db.session.commit() #saves changes
    return redirect(url_for('sent'))

    
@myapp_obj.route('/add_friend', methods=['GET', 'POST'])
@login_required
def add_friend(): #add friend object based on the email and friend to the database
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if email == current_user.email:
            flash('You cannot add yourself as a friend.')
            return redirect(url_for('friend_list'))
        #This check if email has already been created
        account = User.query.filter_by(username=name,email=email).first()
        if account is None:
            flash('User with email {} or username {} does not exist.'.format(email,name))
            return redirect(url_for('friend_list'))
        usersearch = User.query.filter_by(username=name).first()
        #check if a friend with the same email already exists
        existing_friend = Friend.query.filter_by(email=email, friend_of=current_user).first()
        if existing_friend:
            flash('Friend with email {} already exists.'.format(email))
            return redirect(url_for('friend_list'))
        friend = Friend(name=name, email=email,friend_of=current_user)
        db.session.add(friend)
        db.session.commit()
        flash('Friend added successfully.')
        return redirect(url_for('friend_list'))
        #This tries to commit the new Friend object to the database
    return render_template('add_friend.html')

@myapp_obj.route('/delete_friend/<int:id>', methods=['POST'])
@login_required
def delete_friend(id): #delete friend object in the database
    friend = Friend.query.get_or_404(id) #retrieve Friend object based on the primary key id
    db.session.delete(friend) 
    db.session.commit()
    return redirect(url_for('friend_list'))

@myapp_obj.route('/friend_list', methods=['GET','POST'])
@login_required
def friend_list(): #display all the friend object in the database
    friends = Friend.query.filter_by(friend_of=current_user)
    return render_template('friend_list.html', friends=friends)

@myapp_obj.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():   #renders profile page
    form = updateForm()
    return render_template('profile.html', form=form)

@myapp_obj.route('/editprofile', methods = ['GET', 'POST'])
@login_required
def edit_profile():   #allows the update of the profile
    form = updateForm()
    return render_template('editprofile.html', form=form)

@myapp_obj.route('/updateprofile', methods=['GET', 'POST'])
@login_required
def updateProfile():
    form = updateForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if form.update1.data:  #form to update the name
            user.name = form.name.data
            db.session.commit()
        elif form.update2.data:  #form to update the bio
            user.bio = form.bio.data
            db.session.commit()
        return redirect(url_for('profile'))
    return render_template('editprofile.html', form=form)

@myapp_obj.route('/search_results', methods=['GET'])
@login_required
def search_results():
    query = request.args.get('query')
    search_by = request.args.get("search_by")
    if search_by == "Body":    
        results = Message.query.filter(Message.body.contains(query)).all()  #filter by body   
    elif search_by == "Subject":
        results = Message.query.filter(Message.subject.contains(query)).all()        #filter by subject
    elif search_by == "Username":
        results = Message.query.filter(Message.sender.has(User.username.contains(query))).all()       #filter by username
    else:
        results = Message.query.filter(Message.body.contains(query) | Message.sender.has(User.username.contains(query)) | Message.subject.contains(query)).all() #filter by everything
    return render_template('search_results.html', results=results)

@myapp_obj.route('/message/<int:message_id>/bookmark', methods=['POST'])
@login_required
def bookmark(message_id): #Uses the bookmark boolean to mark it as true
    message = Message.query.get(message_id)
    message.bookmark = True #bookmarked message will now appear in bookmark page
    db.session.commit()
    flash('Message bookmarked!') 
    return redirect(url_for('mainpage'))

@myapp_obj.route('/message/<int:message_id>/unbookmark', methods=['POST'])
@login_required
def unbookmark(message_id): #bookmark boolean becomes false
    message = Message.query.get(message_id)
    message.bookmark = False #bookmark is deleted from bookmark page
    db.session.commit()
    flash('Message unbookmarked!')
    return redirect(url_for('mainpage'))

@myapp_obj.route('/bookmarked', methods = ['GET'])
@login_required
def view_bookmark():
    bookmarked = Message.query.filter_by(bookmark=True).all() #Only displays messages that have bookmark boolean true
    return render_template('bookmarks.html', bookmarked=bookmarked)

@myapp_obj.route('/view_profile/<string:email>', methods = ['GET'])
@login_required
def view_profile(email):
    the_friend = User.query.filter_by(email=email).first()  #allows you to view your friends profile
    return render_template('friend_profile.html', the_friend=the_friend)
    
