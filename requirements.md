## Functional Requirements

User should be able to:
1. Changing password - Kevin
2. Undo sent messages - Kevin
3. Bookmarking messages - Kevin
4. Delete account - Trung
5. Compose messages - Trung
6. Create an account - Trung
7. Edit profile page - Jasper
8. Sort by date - Jasper
9. Search messages - Jasper
10. Remove Friend - Tri Nguyen
11. Create to-do list - Tri Nguyen
12. Add Friend - Tri Nguyen


## Non-functional Requirements

1. Messages should have font Arial in size 12
2. Compatible with Google Chrome, Safari, Microsoft Edge, Opera, and 
Firefox


## Use Cases

### Name: Add friend (Tri Nguyen)
- Summary: User can add friend to their friend list
- Actor(s):User
- Pre-condition:
1. The user is logged in to their account on website
- Trigger: User click "Friend List" button
- Primary Sequence:
1. The system displays the search bar, along with an "Add Friend" button
2. The user type in the username for of the friend they want to add
3. The user select "Add friend" button
4. The system sends a friend requets to the selected friend's email address
- Alternate Sequence: 
1. If the entered name or email address is invalid, the system displays an error message and prompts the user to enter a valid name or email address.
2. If a friend request has already been sent to the selected friend, the system displays a message indicating that the request has already been sent.
- Postconditions:
The user's friend list is updated to if the friend accept the request 
	

### Name: Edit To-do component(Tri Nguyen)
- Sumamry: The user can create a to-do list
- Actor(s): User
- Pre-condition: The user is logged in to their account on website
- Trigger: User click "To-do" button or link
- Primary Sequence:
1. The website open a to-do list that showed all the tasks the user has created, sorted in due date
2. The user write down all the tasks
3. The user click the "Add" button
- Alternative sequencde:
If the user does not have any to-do tasks, the system prompts message the user has no tasks.
- Post Condition:
The user is able to update a task as done or undone, and delete a task
	

### Name: Search messages (Jasper)
- Summary: The use can enter keywords to look for a specific email that contains these keywords
- Actors: User
- Pre-conditions: The user must be logged in
- Trigger: Selecting the search bar and type in specific keywords of what you are searching for
- Primary Sequence:  
1. User selects the search bar
2. User types in key words that may be contained in the title, sender, subject, or body of the message
3. A list of received messages with a match appear
4. User selects the message they are looking for
- Alternative Sequence:
User entered key words that yielded no results. Message saying “Not found” shows up
- Post-Condition: 
Messages that have matching keywords from the search bar are displayed OR “Not Found” 
message is displayed as there are no matches

### Name: Edit Profile (Kevin)
- Summary: The user clicks on the "Edit Profile" button that takes them to the Edit Profile page to change/create their bio
- Actors: User creating their bio
- Pre-conditions: User must be logged in their account 
- Trigger: Clicking on the "Edit Profile" button in the Main Page 
- Primary Sequence: 
1. User clicks on the text field under "bio"
2. User types out their introduction in the text field
3. User clicks the submit button
- Alternative Sequence:
User leaves the page without hitting submit, then the changes made in their bio won't be saved. 
OR
User clicks submit without anything inputted in the text field, program will prompt them to fill in the blank
- Post-Condtions: 
User's customized bio appears when a user or a friend views the profile
OR
User doesn't click submit, then their changes won't appear in their bio

### Name: Bookmarking messages (Kevin)
- Summary: The user can click on an icon to bookmark messages in their inbox 
- Actors: User that is bookmarking the message
- Pre-conditions: User must be logged in, and have a message in their inbox 
- Trigger: Clicking on the bookmark icon
- Primary Sequence:
1. User goes into their inbox
2. User clicks the bookmark icon on the message they want to bookmark
3. Message will appear on their bookmark folder
- Alternative Sequence:
User clicks the bookmark icon on a message that is already bookmarked, then message is removed from the bookmark folder 
- Post-Conditions:
Message appears in the bookmark folder, and the message will be marked
OR
Message will disappear from the folder when a user clicks on an already bookmarked message


### Name: Changing password (Kevin)
- Summary: The user can change their password through the settings page
- Actors: User that is changing their password
- Pre-Conditions: User must be logged in their account and in the settings page
- Trigger: Clicking on the change password button in settings
- Primary Sequence: 
1. User inputs their new password
2. Clicks on button to confirm their changes
3. User is taken back to their inbox
- Alternative Sequence: 
If the user enters the same password as their previous one, then error "Try new password" will appear
- Post-Conditon:
User will have a new password in their account, and won't be able to use their previous one to login or user failed to change their password


### Name: Composing messages (Trung)
- Summary: The user clicks on the "compose" button to create an email draft where they will enter text or files onto the textbox, and pick a recipient to send to 
- Actors: User creating the email
- Pre-conditions: User must be logged in, and in the inbox page
- Trigger: User clicks on the "compose" button
- Primary Sequence:
1. User enters message in draft
2. User types subject in subject line
3. User enters the name or email address of user they want to send to.
4. User clicks "Send"
- Alternative Sequence:
1. If user clicks "Send" without entering a recipient, then message prompts user to enter a recipient
2. If user clicks "Send" without sending a subject, then it will send a message with an empty subject line
3. If user clicks "Send" without entering a message in the draft, then an empty message will be sent to the recipient
- Post-Conditions:
1. Message will appear in the recipient's inbox
2. Message will appear in sent messages folder
	

### Name: Register an account (Trung)
- Summary: A user on the website can register for an account to use its application
- Actors: The user registering for the website
- Pre-conditions: The user must be on the website and not already logged in
- Trigger: Click the “Create account” button
- Primary Sequence: 
1. The user fills out the email, password, and username on the registration form
2. The user click “Register” to send in the registration
3. The system makes the account and automatically log the user in with their new account
- Alternative Sequence:
1. If the email already has an account, the system outputs an error message that prompts the user to enter a valid email address.
2. If the username is taken, the system outputs an error message that prompts the user to try a different username.
3. If either the email, username, or password is left empty, the system outputs an error message that prompts the user to fill out all the fields.
- Post Condition: 
The user made the new account and can log in, or the user fails to make the new account and can’t log in.
	


### Name: Sort emails by date
- Summary: The user can sort the emails from oldest to newest or newest to oldest based on the receive date
- Actors: The user that is trying to sort their email by date
- Pre-conditions: The user must be logged in and on the mainpage
- Trigger: Clicking a menu and selecting their desired sorting, then clicking the confirm button
- Primary Sequence: 
1. User opens the drop down menu
2. User selects desired type of sort
3. User clicks the confirm button
- Alternative Sequence:
1. There are no emails available to be sorted and nothing happens
- Post Condition: 
The emails are now sorted by whatever the user selected
				OR
			      There are no emails that were ever sent to the user so no emails will be sorted

	
