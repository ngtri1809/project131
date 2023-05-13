# Sigma Mail (S-mail)
## Contributors
- Tri Nguyen - ngtri1809
- Jasper Nguyen - jasper-nguyen
- Kevin Aquino - Fireality
- Trung Tran - trungtran1234

## Introduction
Sigma Mail is a modern, web-based email application that allows registered users to manage their emails online. With features like composing email and todo list, this app makes it easy to stay on top of your email game. Built with python, html, and css, Sigma mail is a reliable and efficient way to manage your emails from anywhere with an internet connection.

## Installation  
1. Clone the repository:   
SSH Clone:  
git clone git@github.com:ngtri1809/project131.git   
HTTPS Clone:  
https://github.com/ngtri1809/project131.git  

2. Use pip to install libraries:   
pip install sqlalchemy, flask, flask_login, flask_sqlalchemy, sqlalchemy, flask_wtf, wtf_forms, datetime, werkzeug

3. Run the program (in the terminal):  
cd project131  
python3 run.py  
Link to go on the webpage:  
http://127.0.0.1:5000  

4. Exit the program:  
In the terminal, press ctrl + C and it will end the program  

## How to use
1. Create account: The user can create an account
2. Log-in: User can log in using the account that they created
3. Log-out: User can log out of their account
4. Delete account: The user can delete their account through the settings page
5. Changing password: The user can change their password through the settings page
6. Compose: User can compose an email where they will fill in the recipient, subject, and body of the email. They can click "send" to send it to the selected user afterwards
7. Sort-by-date: User can view their message sorted by date by selecting the order in the dropdown menu and clicking "sort"
8. Create to-do list: The user can create a to-do list, update, and delete item inside the list
9. Search bar: User can search in text box, and use the drop down function to search by subject, username, message body, or all of the above. 
10. Friends list: search for an existing username and email to add the user in a list. Similar to a contact list. User can also view their friend's profile, and delete the a friend from their friend's list. 
11. Undo: User can go to the sent messages page, and click the "undo" button to delete the message they sent 
12. Bookmarking: User can click on the "bookmark" button on a message in their inbox, and it will be displayed on the bookmark page. When user clicks the "Unbookmark" button on message that is already bookmarked, the message is removed from the page
13. Edit profile: User can click on the "Profile" header, and click on the "edit profile" button. They can change their appearing name, and create, change or delete their bio. 

## Technologies Used
1. Coding Languages: Python, HTML, CSS
2. Libraries: sqlalchemy, flask, flask_login, flask_wtf, wtforms, glob, flask_sqlalchemy, datetime, werkzeug
3. Collaboration platforms: Github and Discord

## Acknowledgments
- Tri Nguyen - Implemented todo list, and add or remove friend from friends list 
- Jasper Nguyen - Implemented sort messages by date, search bar with drop down function, edit profile, and user profile
- Kevin Aquino - Implemented change password, Undo button, and bookmarking function
- Trung Tran - Implemented compose,login,logout,register,delete account
